#!/usr/bin/python3
# quickstart.py

import sys
sys.path.append("../")
import time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from flask_api.config import AZURE_COMPUTERVISION_SUBSCRIPTION_KEY


def get_gas_price(url):
    subscription_key = AZURE_COMPUTERVISION_SUBSCRIPTION_KEY
    endpoint = "https://eastus.api.cognitive.microsoft.com/"
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    # Get an image with printed text
    remote_image_printed_text_url = url

    # Call API with URL and raw response (allows you to get the operation location)
    recognize_printed_results = computervision_client.batch_read_file(remote_image_printed_text_url, raw=True)

    # Get the operation location (URL with an ID at the end) from the response
    operation_location_remote = recognize_printed_results.headers["Operation-Location"]

    # Grab the ID from the URL
    operation_id = operation_location_remote.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results
    while True:
        get_printed_text_results = computervision_client.get_read_operation_result(operation_id)
        if get_printed_text_results.status not in ['NotStarted', 'Running']:
            break
        time.sleep(1)

    # Print the detected text, line by line
    numbers_list = []
    strings_list = []
    newdict = {}

    if get_printed_text_results.status == TextOperationStatusCodes.succeeded:
        for text_result in get_printed_text_results.recognition_results:
            for line in text_result.lines:
                new_line = line.text.replace(" ", "")
                if (is_float(new_line)):
                    numbers_list.append(float(new_line))
                elif (is_string(new_line)):
                    strings_list.append(new_line)
                    newdict[new_line] = find_area(line.bounding_box)

    numbers_list = [x for x in numbers_list if (x > 0 and x < 6) or (check_three_digit((x)))]
    for x in range(len(numbers_list)):
        while (numbers_list[x] >= 10.0):
            numbers_list[x] /= 10.0

    max = 0
    gas_type = ""
    for x in range(len(strings_list)):
        if (newdict[strings_list[x]] > max):
            max = newdict[strings_list[x]]
            gas_type = strings_list[x]

    price = numbers_list[0] if len(numbers_list) > 0 else 0

    return {gas_type: price}


def is_float(s):
    try:
        float(s)
        return True
    except:
        return False


def check_three_digit(s):
    try:
        len(str(s))
        x = str(s)
        dot = x.index('.')
        if dot == 3 or dot == 4:
            x = x.replace(".", "")
            if x.isdigit():
                return True
        else:
            return False
    except:
        return False


def is_string(s):
    for x in range(len(s)):
        if s[x].isalpha() or s[x] == '-':
            None
        else:
            return False
    return True


def find_area(s):
    length = s[2] - s[0]
    width = s[5] - s[1]
    return length * width
