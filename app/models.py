from app import db

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(64), index=True, unique=True)
    created_utc = db.Column(db.DateTime, default=db.func.current_timestamp())


    def __init__(self, image_name):
        self.image_name = image_name