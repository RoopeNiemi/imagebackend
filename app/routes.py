from app import app, db
from flask import request, Response, send_file
from sqlalchemy.sql import text
from werkzeug.utils import secure_filename
from.models import Image
import os
from .process_image import create_and_save_grayscale

_TYPES=['jpg', 'jpeg', 'png']
_FOLDER = app.config['UPLOAD_FOLDER']

@app.route('/')
@app.route('/index')
def index():
    stmt = text("SELECT image_name FROM image")
    names = db.engine.execute(stmt)
    res = [row['image_name'] for row in names]
    return Response(status=200, response=res)

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if not file or file.filename == '':
            flash('No selected file')
            return Response(status=400, response="No selected file")
        return save_file(file)
    return Response(status=200)

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
    save_to_database(filename)
    grayscale_loc, grayscale_name = create_and_save_grayscale(file_save_location)
    save_to_database(grayscale_name)
    return send_file(grayscale_loc, mimetype="image/{}".format(file_type))

def save_to_database(filename):
    img = Image(image_name=filename)
    db.session().add(img)
    db.session().commit()
