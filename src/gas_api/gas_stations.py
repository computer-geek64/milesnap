#!/usr/bin/python3
# gas_stations.py

import sys
sys.path.append("../")
import json
import requests
from flask_api.config import GOOGLE_MAPS_API_KEY


def find_places(lat, long, radius_in_miles):
    radius = 1609.34*radius_in_miles
    type = "gas_station"
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius={}&type={}&key={}".format(lat, long, radius, type, GOOGLE_MAPS_API_KEY)
    response = requests.get(url)
    res = json.loads(response.text)
    stationdict = {}
    for result in res["results"]:
        stationdict[result['name']] = result['geometry']['location']
    return stationdict


def find_nearest_n_places(lat, long, n):
    type = "gas_station"
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&type={}&key={}&rankby=distance".format(lat, long, type, GOOGLE_MAPS_API_KEY)
    response = requests.get(url)
    res = json.loads(response.text)
    stationdict = {}
    if n < len(res["results"]):
        count = 0
        for result in res["results"]:
            if count < n:
                stationdict[result['name']] = result['geometry']['location']
                count += 1
        return stationdict
    else:
        for result in res["results"]:
            stationdict[result['name']] = result['geometry']['location']
        return stationdict
