from app import app, db
from flask import request, Response, send_file, Flask, redirect, render_template, jsonify
from sqlalchemy.sql import text
from werkzeug.utils import secure_filename
from.models import Image as modelImage
import os
import json
from .process_image import *

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

_TYPES=['jpg', 'jpeg', 'png']
_FOLDER = app.config['UPLOAD_FOLDER']
_MIN_LON_LAT = -90.0
_MAX_LON_LAT = 90.0
@app.route('/')
@app.route('/index')
def index():
    images = modelImage.query.filter(modelImage.latitude.isnot(None)).filter(modelImage.longitude.isnot(None))
    return Response(filenames_to_json(images))

@app.route('/upload', methods = ['POST'])
def upload_file():
    file = request.files['file']
    if not file or file.filename == '':
        return Response(status=400, response="Request did not contain a file")
    file_save_location, filename = save_file(file)
    lat, lon = extract_coordinates(file_save_location)
    save_to_database(filename, lat, lon)
    return Response(status=200, response="Image uploaded")

def save_file(file):
    """
    Saves file to local directory and filename to database
    """
    filename = secure_filename(file.filename)
    file_type = filename.split(".")[1]
    if file_type not in _TYPES:
        return Response(status=403, response='Wrong type of image. Accepted formats: {}'.format(_TYPES))
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
    except:
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

