import pandas as pd
from flask import Flask, render_template, request
import csv
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from models.DomainObjects import BusinessInfo
import math

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
    infoBox = '<div class="well well-sm">'
    infoBox += '<div class="row">'
    infoBox += '<div class="col-xs-12 col-sm-12 col-md-12">'
    if business.name != "":
        infoBox += '<h4>%s</h4>' % (business.name)
    if business.address != "":
        infoBox += '<small>%s, %s, %s <i class="glyphicon glyphicon-map-marker"></i></small>' % (business.address, business.city, business.province)
    infoBox += '<p>'
    if business.emailAddress != "":
        infoBox += '<i class="glyphicon glyphicon-envelope"></i><a href="mailto:%s">%s</a>' % (business.emailAddress, business.emailAddress)
        infoBox += '<br>'
    if business.website != "" and math.isnan(business.website) == False:
        infoBox += '<i class="glyphicon glyphicon-globe"></i><a href="http://%s" target="_blank">%s</a>' % (business.website, business.website)
        infoBox += '<br>'
    if business.phoneNumber != "":
        infoBox += '<i class="glyphicon glyphicon-phone"></i>%s' % (business.phoneNumber)
        infoBox += '<br>'
    if business.memberSince != "":
        infoBox += '<i class="glyphicon glyphicon-calendar"></i>Member since:%s' % (business.memberSince)
        infoBox += '<br>'
    if business.benefit != "" and math.isnan(business.benefit) == False:
         infoBox += '<i class="glyphicon glyphicon-tags"></i>Benefits:'
         infoBox += '<br>'
         infoBox += business.benefit
    infoBox += '</p></div>'
    infoBox += '</div>'
    infoBox += '</div>'

    return infoBox

@app.route('/')
def hello():

    n = request.args.get('n')
    q = request.args.get('q')

    data = pd.read_excel("data.xlsx", sheet_name='data', header=0)

    if q:
        if q.strip():
            # Filter data frame for category search
            data = data.loc[data['Class'] == q]

    if n:
        if n.strip():
            # Filter data frame for business name search
            data = data.loc[data['Name'].str.contains(n, case=False)]

    markers = createMarkers(data)

    fullMap = Map(
        zoom=12,
        identifier="fullMap",
        lat=44.3872894,
        lng=-79.6943205,
        markers=markers
    )

    availableTagsData = pd.read_excel("categories.xlsx", sheet_name='Sheet1', header=0)

    return render_template('map.html', fullMap=fullMap, availableTags=availableTagsData['Category Name'].values.tolist())


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
