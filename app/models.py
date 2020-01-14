from app import db

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(64), index=True, unique=True)
    created_utc = db.Column(db.DateTime, default=db.func.current_timestamp())
    longitude = db.Column(db.String(12), nullable=True)
    latitude = db.Column(db.String(12), nullable=True)


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