import boto3
import os
from os import path

_BUCKET = os.environ['S3_BUCKET']

class AwsHelper():
    
    def __init__(self, local_folder):
        self.s3 = boto3.resource('s3')
        self.local_folder = local_folder

    def upload_to_s3(self, filename):
        """ Upload file to S3. File is presumed to be in the static folder."""
        filepath = "{}/{}".format(self.local_folder, filename)
        self.s3.Bucket(_BUCKET).upload_file(filepath, filename)


    def populate_local_folder(self):
        """ Download every file from S3 that does not already exist locally and save them to local folder """
        response = self.s3.Bucket(_BUCKET).objects.all()
        objects_from_s3 = []
        for obj in response:
            filename = obj.key
            local_path = '{}/{}'.format(self.local_folder, filename)
            if not path.exists(local_path):
                self.get_from_s3(filename, local_path)
                objects_from_s3.append(local_path)
        return objects_from_s3


    def get_from_s3(self, filename, save_path):
        s3_client = boto3.client('s3')
        s3_client.download_file(_BUCKET, filename, save_path)

    