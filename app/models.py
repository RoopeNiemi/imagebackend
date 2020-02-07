from app import db
from sqlalchemy.ext.hybrid import hybrid_property
import bcrypt

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(64), index=True, unique=True)
    created_utc = db.Column(db.DateTime, default=db.func.current_timestamp())
    longitude = db.Column(db.Float, nullable=True)
    latitude = db.Column(db.Float, nullable=True)


    def __init__(self, image_name, latitude, longitude):
        self.image_name = image_name
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return "Image: " + self.image_name + "\nLatitude: " + self.latitude + "\nLongitude: " + self.longitude + "\n"

    def serialize(self):
        return {
            'image_name': "/static/" + self.image_name,
            'latitude': self.latitude,
            'longitude': self.longitude
        }

class Account(db.Model):
    __tablename__ = "accounts"
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(144), nullable=False, unique=True)
    _password=db.Column(db.String(144), nullable=False)

    admin=db.Column(db.Boolean, default=False,  nullable=False)
    
    def __init__(self, username, password):
        self.username = username
        self._password = password
    def get_id(self):
        return self.id
    
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    @hybrid_property
    def password(self):
        return self._password

    
    def is_correct_password(self, plaintext):
        return bcrypt.checkpw(plaintext.encode('utf8'), self._password.encode('utf8')) 