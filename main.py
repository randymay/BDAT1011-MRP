# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask, render_template
import csv
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from models.DomainObjects import BusinessAddress

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

# Initiate Google Maps
GoogleMaps(app, key="AIzaSyDxbiiwUGoMt8g91FANvlRC80wc3Ox0XOA")


def createMarkers(businesses):
    markers = []
    for business in businesses:
        markers.append(createMarker(business))

    return markers


def createMarker(business):
    marker = {
        'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
        'lat': business.latitude,
        'lng': business.longitude,
        'infobox': "<b>%s</b><br></br>" % (business.name)
    }
    return marker


@app.route('/')
def hello():

    businesses = []
    dataFile = open('data.csv', 'r')

    with open('data.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            print(row)

            business = BusinessAddress()
            business.name = row[0]
            business.streetAddress1 = row[1]
            business.latitude = row[7]
            business.longitude = row[8]

            businesses.append(business)

    dataFile.close

    # print(businesses)
    markers = createMarkers(businesses)
    # print(markers)

    fullMap = Map(
        zoom=11,
        identifier="fullMap",
        lat=44.3872894,
        lng=-79.6943205,
        markers=markers
        # markers=[
        #    {
        #        'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
        #        'lat': 37.4419,
        #        'lng': -122.1419,
        #        'infobox': "<b>Hello World</b>"
        #    },
        #    {
        #        'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
        #        'lat': 37.4300,
        #        'lng': -122.1400,
        #        'infobox': "<b>Hello World from other place</b>"
        #    }
        # ]
    )
    return render_template('map.html', fullMap=fullMap)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
