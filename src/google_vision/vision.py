#!/usr/bin/python3
# vision.py

import sys
sys.path.append("../")
import os
import math
import statistics
from time import sleep
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from spellchecker import SpellChecker
from google.cloud import vision
from google.protobuf.json_format import MessageToDict
from flask_api.config import GOOGLE_APPLICATION_CREDENTIALS_JSON_FILE

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS_JSON_FILE


def get_midpoint(quadrilateral_coordinates):
    return statistics.mean([x[0] for x in quadrilateral_coordinates]), statistics.mean([x[1] for x in quadrilateral_coordinates])


def get_text_element(strings, coordinates):
    for i in range(len(strings)):
        point = Point(coordinates)
        polygon = Polygon(strings[i]["bounds"])
        if polygon.contains(point):
            return strings[i]
    return False


def adaptive_keywords(keywords, strings):
    texts = [x["text"].lower() for x in strings]
    i = 0
    while i < len(keywords):
        if keywords[i] not in texts or texts.count(keywords[i]) > 1:
            keywords.pop(i)
            i -= 1
        i += 1
    return keywords


def get_gas_price(url):
    keywords = ['regular', 'reg', 'plus', 'premium', 'pre', 'prem', 'unleaded', 'super', 'v-power', 'special', 'super+', 'unlead', 'noethnl', 'diesel', 'extra', 'midgrade', 'mid-grade', 'mid', 'silver', 'ultimate', 'unleaded plus', 'unleaded premium']
    spell = SpellChecker()
    spell.word_frequency.load_words(keywords)
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = url

    texts = MessageToDict(client.text_detection(image=image))
    while "error" in texts.keys():
        texts = MessageToDict(client.text_detection(image=image))
        sleep(5)

    if len(texts.keys()) == 0:
        return {"ERROR": "No text found"}

    texts["textAnnotations"].pop(0)
    strings = [{"text": x["description"], "bounds": [(y["x"], y["y"]) if "y" in y.keys() else (y["x"], 0) for y in x["boundingPoly"]["vertices"]]} for x in texts["textAnnotations"]]

    # Get number prices
    numbers = []
    for i in range(len(strings)):
        if strings[i]["text"].replace(".", "").replace(" ", "").replace("$", "")[:3].isnumeric():
            string = strings[i]["text"].replace(".", "").replace(" ", "").replace("$", "")[:3]
            if len(string) >= 3:
                strings[i]["text"] = "$" + string[0] + "." + string[1:]
                numbers.append(strings[i])

    # Get adaptive keyword list
    keywords = adaptive_keywords(keywords, strings)

    # Get keyword
    keyword_indexes = [i for i in range(len(strings)) if strings[i]["text"].lower() in keywords]
    if len(keyword_indexes) == 0:
        return {str(i): numbers[i]["text"] for i in range(len(numbers))}
    keyword = strings[keyword_indexes[0]]
    keyword_midpoint = get_midpoint(keyword["bounds"])

    # Get vector
    vector = (10000, 10000)
    for i in range(len(numbers)):
        number_midpoint = get_midpoint(numbers[i]["bounds"])
        if math.sqrt((keyword_midpoint[0] - number_midpoint[0]) ** 2 + (keyword_midpoint[1] - number_midpoint[1]) ** 2) < math.sqrt(vector[0] ** 2 + vector[1] ** 2):
            vector = (keyword_midpoint[0] - number_midpoint[0], keyword_midpoint[1] - number_midpoint[1])

    # Get gas type and price association
    output = {}
    for i in range(len(numbers)):
        number_midpoint = get_midpoint(numbers[i]["bounds"])
        gas_type = get_text_element(strings, (vector[0] + number_midpoint[0], vector[1] + number_midpoint[1]))
        if gas_type:
            output[spell.correction(gas_type["text"]).capitalize()] = numbers[i]["text"]
        else:
            # Attempt to cast a wider net around the vector
            output[str(i)] = numbers[i]["text"]
            for n in range(-50, 51, 10):
                gas_type = get_text_element(strings, (vector[0] + number_midpoint[0] + n, vector[1] + number_midpoint[1]))
                if gas_type and gas_type["text"].lower() in keywords:
                    output.pop(str(i))
                    output[spell.correction(gas_type["text"]).capitalize()] = numbers[i]["text"]
                    break
                gas_type = get_text_element(strings, (vector[0] + number_midpoint[0], vector[1] + number_midpoint[1] + n))
                if gas_type and gas_type["text"].lower() in keywords:
                    output.pop(str(i))
                    output[spell.correction(gas_type["text"]).capitalize()] = numbers[i]["text"]
                    break
    for k in output.keys():
        if k.isnumeric():
            output["Unknown " + str(k)] = output.pop(k)
    return output

print(get_gas_price("https://headricks.com/sites/default/files/gallery/thumbnails/tc.jpg"))