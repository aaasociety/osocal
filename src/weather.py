#!/bin/python3
# weather.py
# A wrapper for accessing weather data
#import src.lib as lib # Shared data across all modules
import json # For handling data
import requests # For sending API requests
import src.lib as lib

Err = lib.ErrType

# No I dont really care about exposing my API key.
apiKey="f45611b139c042d1af9204440221812"

# Returns an array containing the following:
# [
# Temperature in celsius,
# Weather condition,
# Wind (km per hour)
# Feels like (Celsius)
# ]
def getWeatherData(location):
    location = str(location)
    if location == "":
        return Err
    if location == "Hjem":
        location = lib.HomeAddress
    if location == "Odense, Danmark":
        location = "Odense, Denmark"
        
#    AssembledApiRequest = "https://api.weatherapi.com/v1/forecast.json?key=" + apiKey +"&q=" + location + "&days=1"
#    response = requests.get(AssembledApiRequest)
    response = open("DATA.txt","r")
    weatherdict = json.loads(str(response.read()))
    weatherresult = [
        str(weatherdict["current"]["temp_c"]),
        str(weatherdict["current"]["condition"]["text"]),
        str(weatherdict["current"]["wind_kph"]),
        str(weatherdict["current"]["feelslike_c"]),
    ]
    response.close()
    return weatherresult
