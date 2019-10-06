from app import db

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    image_name = db.Column(db.String(64), index=True, unique=True)



    def __init__(self, username, image_name):
        self.username = username
        self.image_name = image_name