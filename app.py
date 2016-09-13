from flask import Flask
from flask import render_template, redirect, url_for, request, flash
import config
import requests
import json
import datetime
import os
import urllib.parse

app = Flask(__name__)

# config
app.debug = config.DEBUG
app.secret_key = config.SECRET_KEY
app.api_key = config.API_KEY

# base search URIs
app.base_uri = config.WU_BASE_URI
app.base_ac_uri = config.WU_AUTOCOMPLETE_URI

# search params
doc_format = '.json'

wu_cats = {
    "geolookup": "/geolookup/",
    "satellite": "/satellite/",
    "webcams": "/webcams/",
    "conditions": "/conditions/",
    "forecast": "/forecast/",
    "forecast10day": "/forecast10day/"
}

hdr = {
    'user-agent': 'superbot by gravity'
}


@app.route('/', methods=['GET', 'POST'])
def index():
    welcome = 'Hello weatherpy!'

    if request.method == 'POST':
        try:
            query = request.form['search']
            data = get_search_data(query)
            context = {
                'data': data,
            }

            return render_template(
                'index.html',
                context=context
            )

        except (ValueError, TypeError):
            return "The input was not in a recognized format.  Please try again..."

    else:

        return render_template(
            'index.html',
            context=welcome
        )


@app.route('/geolookup', methods=['GET', 'POST'])
def geolookup():
    return render_template(
        'geolookup.html',
        context=context
    )


def get_search_data(query):
    url = build_ac_url(app.base_ac_uri, query)
    r = requests.get(url, headers=hdr)
    status = str(r.status_code)
    decoded = r.json()
    return decoded, status


def get_location_data(location):
    pass


def build_url(base, key, cat, query, format):
    return base + key + cat + urllib.parse.quote(query) + format


def build_ac_url(base, query):
    return base + urllib.parse.quote(query)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5555))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )
