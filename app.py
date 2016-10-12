from flask import Flask
from flask import render_template, redirect, url_for, request, flash, session
import config
import requests
import json
import datetime
import os
import urllib

app = Flask(__name__)

# config
app.debug = config.DEBUG
app.secret_key = config.SECRET_KEY
app.api_key = config.API_KEY

# base search URIs
app.base_uri = config.WU_BASE_URI
app.base_ac_uri = config.WU_AUTOCOMPLETE_URI

# search params
format = '.json'

wu_cats = {
    "geolookup": "/geolookup/q/",
    "satellite": "/satellite/q/",
    "webcams": "/webcams/q/",
    "conditions": "/conditions/q/",
    "forecast": "/forecast/q/",
    "forecast10day": "/forecast10day/q/"
}

hdr = {
    'user-agent': 'weatherpy_superbot'
}


@app.route('/', methods=['GET', 'POST'])
def index():
    welcome = 'Hello weatherpy!'

    if request.method == 'POST':
        query = request.form['search']
        data = get_search_data(str(query))

        if len(data) == 0:
            data = None
        else:
            data = data

        return render_template(
            'index2.html',
            data=data,
        )
    else:
        return render_template(
            'index.html',
            welcome=welcome,
        )


@app.route('/get_location', methods=['POST'])
def get_location():
    session['location'] = request.form['location']
    return redirect(url_for('location'))


@app.route('/geolookup', methods=['GET'])
def location():
    location = session['location']
    location = str.split(str(location), ' ')
    location = str(location[0] + ',' + location[1])

    geolookup = get_location_data(wu_cats.get('geolookup'), location)

    """
    conditions = get_location_data('conditions', location)
    forecast10day = get_location_data('forecast10day', location)
    webcams = get_location_data('webcams', location)
    satellite = get_location_data('satellite', location)
    """
    context = {
        'geolookup': geolookup
        #'forecast10day': forecast10day,
        #'webcams': webcams,
        #'satellite': satellite
    }

    return render_template(
        'location.html',
        context=context,
    )


def get_search_data(query):
    url = build_ac_url(app.base_ac_uri, query)
    r = requests.get(url, headers=hdr)
    decoded = r.json()
    return decoded


def get_location_data(category, query):
    url = build_url(app.base_uri, app.api_key, category, query, format)
    r = requests.get(url, headers=hdr)
    location_data = r.json()
    return location_data


def build_url(base, key, cat, query, format):
    return base + key + cat + query + format


def build_ac_url(base, query):
    return base + urllib.quote(query)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5580))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )
