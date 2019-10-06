from flask import Flask

app = Flask(__name__)
import os
from flask_sqlalchemy import SQLAlchemy



if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///images.db"    
    app.config["SQLALCHEMY_ECHO"] = True

app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(os.path.realpath(__file__)), "files")

db = SQLAlchemy(app)


from app import routes, models
db.create_all()