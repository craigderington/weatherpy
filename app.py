from flask import Flask
from flask import render_template, redirect, url_for, request, flash
import config
import requests
import json
import datetime
import os

app = Flask(__name__)

# WU Base URIs
WU_BASE_URI = "http://api.wunderground.com/api/"
WU_AUTOCOMPLETE_BASE_URI = "http://autocomplete.wunderground.com/aq?query="

app.debug = config.DEBUG
app.secret_key = config.SECRET_KEY
app.api_key = config.API_KEY


wu_cats = {
    "geolookup": "geolookup/",
    "satellite": "satellite/",
    "webcams": "webcams/",
    "conditions": "conditions/",
    "forecast": "forecast/",
    "forecast10day": "forecast10day/"
}


@app.route('/', methods=['GET'])
def index():
    welcome = "Welcome to weatherpy"
    return render_template(
        'index.html',
        welcome=welcome
    )


@app.route('/geolookup', methods=['GET', 'POST'])
def geolookup():
    return render_template(
        'geolookup.html',
        context=context
    )


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5555))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )
