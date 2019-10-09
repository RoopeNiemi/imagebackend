from app import app, db
from flask import request, Response, send_file
from sqlalchemy.sql import text
from werkzeug.utils import secure_filename
from.models import Image
import os

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
        print("FILE::::", file)
        print("NAME::::", file.filename)
        if not file or file.filename == '':
            flash('No selected file')
            print("NO SELECTED FILE")
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
    img = Image(image_name=filename)
    db.session().add(img)
    db.session().commit()
    return send_file(file_save_location, mimetype="image/{}".format(file_type))
