from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__, static_folder= os.path.join(os.path.dirname(os.path.realpath(__file__)), "static"))
cors = CORS(app)
import os
from flask_sqlalchemy import SQLAlchemy



if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///images.db"    
    app.config["SQLALCHEMY_ECHO"] = True

app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static")
app.config["SECRET_KEY"] = os.urandom(32)
db = SQLAlchemy(app)


from app import routes, models

try: 
    db.create_all()
    routes.save_image_info_from_s3_to_database()
except:
    pass