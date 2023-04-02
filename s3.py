import boto3
import os
from dotenv import load_dotenv

load_dotenv()

class S3Service:
    def __init__(self):
        self.key = os.environ["AWS_KEY_ID"]
        self.secret = os.environ["AWS_SECRET"]
        self.s3 = boto3.client(
            "s3", aws_access_key_id=self.key, aws_secret_access_key=self.secret
        )
        self.bucket = os.environ["AWS_BUCKET_NAME"]
        self.region = os.environ["AWS_REGION"]

    def upload(self, local_path, bucket_path):
        self.s3.upload_file(
            local_path,
            self.bucket,
            bucket_path,
            ExtraArgs={"ACL": "private", "ContentType": "text/csv"},
        )
        return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{bucket_path}"
    
    def download(self, bucket_path, local_file_path):
        self.s3.download_file(self.bucket, bucket_path, local_file_path)
        