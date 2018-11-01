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
import pandas as pd
from flask import Flask, render_template
import csv
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from models.DomainObjects import BusinessInfo

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

# Initiate Google Maps
GoogleMaps(app, key="AIzaSyDxbiiwUGoMt8g91FANvlRC80wc3Ox0XOA")


def createMarkers(data):
    businesses = []
    for index, row in data.iterrows():
        business = BusinessInfo()
        												
        business.name = row['Name']
        business.address = row['Address']
        business.city = row['City']
        business.province = row['Province']
        business.latitude = row['Latitude']
        business.longitude = row['Longitude']
        business.website = row['Website']
        business.emailAddress = row['Email']
        business.phoneNumber = row['Phone']
        business.classification = row['Class']
        business.benefit = row['Benefit']
        business.imageUrl = row['Image URL']
        business.memberSince = row['Member Since']

        businesses.append(business)
        
    markers = []
    for business in businesses:
        markers.append(createMarker(business))

    return markers


def createMarker(business):
    marker = {
        'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
        'lat': business.latitude,
        'lng': business.longitude,
        'infobox': createInfoBox(business)
    }
    return marker

def createInfoBox(business):
    # infoBox = "<b>Yo! %s</b><br></br>" % (business.name)

    #infoBox = '<div class="container">'
    # infoBox = '<div class="col-xs-12 col-sm-12 col-md-12">'
    infoBox = '<div class="well well-sm">'
    infoBox += '<div class="row">'
    # infoBox += '<div class="col-xs-6 col-sm-6 col-md-6">'
    # infoBox += '<img src="%s" alt="" class="info-box-img img-rounded img-responsive">' % (business.imageUrl)
    # infoBox += '</div>'
    infoBox += '<div class="col-xs-12 col-sm-12 col-md-12">'
    if business.name != "":
        infoBox += '<h4>%s</h4>' % (business.name)
    if business.address != "":
        infoBox += '<small>%s, %s, %s <i class="glyphicon glyphicon-map-marker"></i></small>' % (business.address, business.city, business.province)
    infoBox += '<p>'
    if business.emailAddress != "":
        infoBox += '<i class="glyphicon glyphicon-envelope"></i><a href="mailto:%s">%s</a>' % (business.emailAddress, business.emailAddress)
        infoBox += '<br>'
    if business.website != "":
        infoBox += '<i class="glyphicon glyphicon-globe"></i><a href="http://%s" target="_blank">%s</a>' % (business.website, business.website)
        infoBox += '<br>'
    if business.phoneNumber != "":
        infoBox += '<i class="glyphicon glyphicon-phone"></i>%s' % (business.phoneNumber)
        infoBox += '<br>'
    if business.memberSince != "":
        infoBox += '<i class="glyphicon glyphicon-calendar"></i>Member since:%s' % (business.memberSince)
        infoBox += '<br>'
    if business.benefit != "":
        infoBox += '<i class="glyphicon glyphicon-tags"></i>Benefits:'
        infoBox += '<br>'
        infoBox += business.benefit
    infoBox += '</p></div>'
    infoBox += '</div>'
    infoBox += '</div>'
    #infoBox += '</div>' 

    return infoBox

@app.route('/')
def hello():

    data = pd.read_excel("data.xlsx", sheet_name='data', header=0)
    print(data.head())

    """ businesses = []
    dataFile = open('data.csv', 'r')

    with open('data.csv', newline='') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',')
        # Skip the first row
        next(csvReader, None)
        for row in csvReader:
            print(row)

            business = BusinessInfo()
            business.name = row[0]
            business.address = row[1]
            business.city = row[2]
            business.province = row[3]
            business.latitude = row[4]
            business.longitude = row[5]
            business.website = row[6]
            business.emailAddress = row[7]
            business.phoneNumber = row[8]
            business.classification = row[9]
            business.benefit = row[10]
            business.imageUrl = row[11]
            business.memberSince = row[12]

            businesses.append(business)

    dataFile.close """

    # print(businesses)
    markers = createMarkers(data)
    # print(markers)

    fullMap = Map(
        zoom=12,
        identifier="fullMap",
        lat=44.3872894,
        lng=-79.6943205,
        markers=markers
    )
    return render_template('map.html', fullMap=fullMap)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
