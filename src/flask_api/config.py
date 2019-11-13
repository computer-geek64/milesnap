#!/usr/bin/python3
# config.py

S3_BUCKET = ""  # S3 Bucket Name
S3_KEY = ""  # S3 Access Key
S3_SECRET = ""  # S3 Secret Access Key
S3_LOCATION = "http://" + S3_BUCKET + ".s3.amazonaws.com/"

MILESNAP_TOKEN = ""  # Randomly generated token for authentication with MileSnap API
HOME = "/"
MILESNAP_ENDPOINT = "/milesnap/api/v1.0"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}

AZURE_COMPUTER_VISION_SUBSCRIPTION_KEY = ""  # Microsoft Azure Computer Vision Subscription Key

GOOGLE_MAPS_API_KEY = ""  # Google Maps API Key
GOOGLE_APPLICATION_CREDENTIALS_JSON_FILE = ""  # Google Cloud Vision Application Credentials JSON File
