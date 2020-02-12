# imagebackend

Backend code for [full stack project](https://github.com/RoopeNiemi/imageprfront)

Images are saved to a local folder and uploaded to an S3 bucket as well. Image name and GPS info (latitude, longitude) are stored in a database. When the container is started downloads all images that are in S3 but not in a local folder and saves them to a local folder. Images can be uploaded up to 1GB, if the limit is reached uploading will be disabled. 
