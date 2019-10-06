from app import app, db
from flask import request
from werkzeug.utils import secure_filename
from.models import Image
import os

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    print("HERE")
    if request.method == 'POST':
        file = request.files['file']
        print(request.form)
        username = request.form['user']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return "NO"
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img = Image(username = username, image_name=filename)
            db.session().add(img)
            db.session().commit()
            return filename
