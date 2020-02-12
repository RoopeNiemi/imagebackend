from app import app, db
from .aws_helper import AwsHelper
from flask import request, Response, send_file, Flask, redirect, render_template, jsonify
from sqlalchemy.sql import text
from werkzeug.utils import secure_filename
from.models import Image as modelImage
from .models import Account
import bcrypt
import os
import json
from .process_image import extract_coordinates
from pathlib import Path

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

_ACCEPTABLE_IMAGE_FORMATS=['jpg', 'jpeg', 'png']
_FOLDER = app.config['UPLOAD_FOLDER']
_MIN_LON_LAT = -90.0
_MAX_LON_LAT = 90.0
_UPLOAD_THRESHOLD = 1000
_DISABLE_UPLOADS = False

aws = AwsHelper(_FOLDER)

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

def check_folder_size():
    """ Disables uploads to S3 if S3 bucket size limit reached, to prevent S3 from exploding in size """
    root_directory = Path(_FOLDER)
    to_mbs = 1024 * 1024
    size = 0
    for image_format in _ACCEPTABLE_IMAGE_FORMATS:
        pattern = '**/*.{}'.format(image_format)
        size += sum(f.stat().st_size for f in root_directory.glob(pattern) if f.is_file() )
    size /= to_mbs
    if size >= _UPLOAD_THRESHOLD:
        _DISABLE_UPLOADS = True

@app.route('/')
@app.route('/index')
def index():
    images = modelImage.query.filter(modelImage.latitude.isnot(None)).filter(modelImage.longitude.isnot(None))
    return Response(filenames_to_json(images))

@app.route('/upload', methods = ['POST'])
@jwt_required
def upload_file():
    if _DISABLE_UPLOADS:
        return Response(status=400, response="S3 size limit reached")
    file = request.files['file']
    if not file or file.filename == '':
        return Response(status=400, response="Request did not contain a file")
    file_save_location, filename = save_file(file)
    lat, lon = extract_coordinates(file_save_location)
    save_to_database(filename, lat, lon)
    aws.upload_to_s3(filename)
    check_folder_size()
    return Response(status=200, response="Image uploaded")

def save_file(file):
    """
    Saves file to local directory and filename to database
    """
    filename = secure_filename(file.filename)
    file_type = filename.split(".")[1]
    if file_type not in _ACCEPTABLE_IMAGE_FORMATS:
        return Response(status=403, response='Wrong type of image. Accepted formats: {}'.format(_ACCEPTABLE_IMAGE_FORMATS))
    file_save_location = os.path.join(_FOLDER, filename)
    file.save(file_save_location)
    return file_save_location, filename

def filenames_to_json(files):
    return json.dumps([f.serialize() for f in files])

def save_to_database(filename, lat, lon):
    img = modelImage(filename, lat, lon)
    db.session().add(img)
    db.session().commit()

@app.route("/search", methods=["GET"])
def find_between_coordinates():
    try:
        min_longitude, max_longitude, min_latitude, max_latitude = process_query_params(request.args)
        files = modelImage.query\
            .filter(modelImage.longitude.between(min_longitude, max_longitude))\
            .filter(modelImage.latitude.between(min_latitude, max_latitude))
        return Response(filenames_to_json(files))
    except Exception as e:
        logger.exception(e)
        return Response(json.dumps([]))

def process_query_params(args):
    min_longitude = args_value_or_default(args.get("min_lon"), _MIN_LON_LAT)
    max_longitude =  args_value_or_default(args.get("max_lon"), _MAX_LON_LAT)
    min_latitude = args_value_or_default(args.get("min_lat"), _MIN_LON_LAT)
    max_latitude =  args_value_or_default(args.get("max_lat"), _MAX_LON_LAT)
    return min_longitude, max_longitude, min_latitude, max_latitude

def args_value_or_default(value, default_value):
    if not value:
        return default_value
    return float(value)


def save_image_info_from_s3_to_database():
    """ Extracts GPS-data from images received from S3 and saves those and the filenames to database. This is only called when the application starts."""
    objects_from_s3 = aws.populate_local_folder()
    for f in objects_from_s3:
        lat, lon = extract_coordinates(f)
        filename = os.path.basename(f)
        save_to_database(filename, lat, lon)

@app.route('/login', methods=['POST'])
def login():
    data = json.loads(request.data)
    username = data['username']
    password = data['password']
    account = Account.query.filter_by(username=username).first()
    if not account or not account.is_correct_password(password):
        return Response(status=400, response="Wrong username or password")
    else:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token, user=username)

@app.route("/register", methods=["POST"])
def auth_register():
    data = json.loads(request.data)
    username = data['username']
    password = data['password']
    user_exists=Account.query.filter_by(username=username).first()
    if not user_exists:    
        user = Account(username=username, password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()).decode('utf8'))
        db.session().add(user)
        db.session().commit()
        return Response(status=200)
    else:
        return Response(status=400)     


@app.route("/delete", methods=["POST"])
def delete_user():
    data = json.loads(request.data)
    username = data['username']
    password = data['password']
    account = Account.query.filter_by(username=username).first()
    if not account or not account.is_correct_password(password):
        return Response(status=400, response="Wrong username or password")
    db.session().delete(account)
    return Response(status=200, response="User deleted")