#!/usr/bin/python3
# api.py

import sys
sys.path.append("../")
import os
from flask import Flask, jsonify, redirect, request
from werkzeug.utils import secure_filename
from s3.bucket import upload_file_object, empty_bucket
from google_vision.vision import get_gas_price

app = Flask(__name__)
app.config.from_object("config")


def authenticate(token):
    return token == app.config["MILESNAP_TOKEN"]


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


@app.route(app.config["HOME"], methods=["GET"])
def get_home():
    # return documentation of endpoints
    return "API Endpoints:<br><ul><li><a href=\"" + app.config["MILESNAP_ENDPOINT"] + "\">MileSnap</a></li></ul>"


@app.route(app.config["MILESNAP_ENDPOINT"], methods=["GET"])
def get_endpoint():
    # return documentation of endpoint
    return "Welcome to MileSnap!"


@app.route(os.path.join(app.config["MILESNAP_ENDPOINT"], "upload"), methods=["POST"])
def upload():
    if "token" not in request.args or not authenticate(request.args["token"]):
        # return "Please use a valid API authentication token."
        return {"ERROR": "Please use a valid API authentication token."}
    if "image" not in request.files:
        if len([x for x in request.files.values() if x.content_type.startswith("image/")]) == 0:
            return {"ERROR": "Image not found in HTTP request"}
        file = [x for x in request.files.values() if x.content_type.startswith("image/")][0]
    else:
        file = request.files["image"]
    if file.filename == "":
        return {"ERROR": "No selected image"}
    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        # Upload file successfully
        url = upload_file_object(file, app.config["S3_BUCKET"])
        # Call Google Cloud Vision API
        gas_price = get_gas_price(url)
        print(gas_price)
        # Empty bucket
        #empty_bucket()
        return jsonify(gas_price)
    return {"ERROR": "Invalid image filename"}


@app.route(os.path.join(app.config["MILESNAP_ENDPOINT"], "bucket", "empty"), methods=["GET", "POST"])
def empty_s3_bucket():
    empty_bucket()
    return "Success"


@app.errorhandler(404)
def page_not_found(e):
    return redirect(app.config["HOME"])


if __name__ == "__main__":
    app.run("0.0.0.0", 81)
