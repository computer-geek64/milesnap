#!/usr/bin/python3
# bucket.py

import sys
sys.path.append("../")
import boto3
from flask_api.config import S3_KEY, S3_SECRET, S3_BUCKET, S3_LOCATION

s3_client = boto3.client("s3", aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET)
s3_resource = boto3.resource("s3", aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET)


def upload_file_object(file, bucket_name, acl="public-read"):
    try:
        s3_client.upload_fileobj(file, bucket_name, file.filename, ExtraArgs={"ACL": acl, "ContentType": file.content_type})
    except Exception as e:
        return "ERROR: " + str(e)
    return S3_LOCATION + file.filename


def empty_bucket():
    bucket = s3_resource.Bucket(S3_BUCKET)
    bucket.objects.all().delete()
