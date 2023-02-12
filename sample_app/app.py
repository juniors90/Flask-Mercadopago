#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the Flask-Mercadopago Project
#    (https://github.com/juniors90/Flask-Mercadopago/).
# Copyright (c) 2022, Ferreira Juan David
# License: MIT
# Full Text:
#    https://github.com/juniors90/Flask-Mercadopago/blob/master/LICENSE

# =============================================================================
# DOCS
# =============================================================================

"""Flask-Mercadopago

Implementation of Mercadopago OAuth in Flask.
"""

# =============================================================================
# IMPORTS
# =============================================================================

import datetime
import json
import logging
import os
import pathlib
import sys

from dotenv import load_dotenv

from flask import (
    Flask,
    current_app,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

import requests

load_dotenv()  # take environment variables from .env.

# Code of your application, which uses environment variables
# (e.g. from `os.environ` or `os.getenv`) as if they came from
# the actual environment.

# this path is pointing to project/docs/source
CURRENT_PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
FLASK_MERCADOPAGO_PATH = CURRENT_PATH.parent

sys.path.insert(0, str(FLASK_MERCADOPAGO_PATH))

from flask_mercadopago import Mercadopago, get_headers  # noqa

app = Flask(__name__)
app.secret_key = "super-secret"
mercadopago = Mercadopago(app)

SERVER_URL = "http://localhost:5000"

app.config["CLIENT_ID"] = os.environ.get("CLIENT_ID")
app.config["CLIENT_SECRET"] = os.environ.get("CLIENT_SECRET")
app.config["APP_ACCESS_TOKEN"] = os.environ.get("APP_ACCESS_TOKEN")
app.config["CALLBACK_URL"] = f"{SERVER_URL}/callback"
app.config["ORG_CONNECTION_COMPLETED_URL"] = SERVER_URL
app.config["MERCADOPAGO_SERVE_LOCAL"] = True

# Leave the line below as-is. This line of code verifies
# that you've modified the APP_ACCESS_TOKEN, CALLBACK_URL,
# CLIENT_ID, CLIENT_SECRET, CLIENT_REDIRECT_URI to the
# values above so that your application can complete OAuth.
assert (
    app.config["APP_ACCESS_TOKEN"] != "place_app_access_token_here"
), "You need to update your config key APP_ACCESS_TOKEN in this line"
assert (
    app.config["CALLBACK_URL"] != "place_client_redirect_uri_here"
), "You need to update your config key CALLBACK_URL in this line"
assert (
    app.config["CLIENT_ID"] != "place_client_id_here"
), "You need to update your config key CLIENT_ID in this line"
assert (
    app.config["CLIENT_SECRET"] != "place_client_secret_here"
), "You need to update your config key CLIENT_SECRET in this line"
assert (
    app.config["ORG_CONNECTION_COMPLETED_URL"] != "place_org_url_here"
), "You need to update your config key ORG_CONNECTION_COMPLETED_URL in this line"  # noqa: E501


def update_token_info(res):
    json_response = res.json()
    seconds = json_response["expires_in"]
    expire_in = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
    session["access_token"] = json_response["access_token"]
    session["expires_in"] = expire_in
    session["token_type"] = json_response["token_type"]
    session["refresh_token"] = json_response["refresh_token"]
    session["scope"] = json_response["scope"]
    session["user_id"] = json_response["user_id"]
    session["refresh_token"] = json_response["refresh_token"]
    session["public_key"] = json_response["public_key"]
    session["live_mode"] = json_response["live_mode"]
    access_token_details = {
        "access_token": json_response["access_token"],
        "token_type": json_response["token_type"],
        "scope": json_response["scope"],
        "user_id": json_response["user_id"],
        "refresh_token": json_response["refresh_token"],
        "public_key": json_response["public_key"],
        "live_mode": json_response["live_mode"],
    }
    session["access_token_details"] = json.dumps(
        access_token_details, indent=4
    )
    session["base_url"] = current_app.config.get("BASE_URL")


with app.app_context():
    settings = {
        "title": "Mercadopago API with Python",
        "response_type": current_app.config["RESPONSE_TYPE"],
        "client_id": current_app.config["CLIENT_ID"],
        "callback_url": current_app.config["CALLBACK_URL"],
        "state": current_app.config["STATE"],
        "base_url": current_app.config["BASE_URL"],
    }


def update_settings_info(api_response=None):
    settings["access_token"] = session["access_token"]
    settings["token_type"] = session["token_type"]
    settings["expires_in"] = session["expires_in"]
    settings["scope"] = session["scope"]
    settings["user_id"] = session["user_id"]
    settings["refresh_token"] = session["refresh_token"]
    settings["public_key"] = session["public_key"]
    settings["live_mode"] = session["live_mode"]
    settings["access_token_details"] = session["access_token_details"]
    settings["base_url"] = session["base_url"]
    settings["api_response"] = "" if api_response is None else api_response


def delete_settings_info():
    settings.pop("access_token")
    settings.pop("token_type")
    settings.pop("expires_in")
    settings.pop("scope")
    settings.pop("user_id")
    settings.pop("refresh_token")
    settings.pop("public_key")
    settings.pop("live_mode")
    settings.pop("access_token_details")
    settings.pop("base_url")
    settings.pop("api_response")


def render_error(message, title=None):
    _title = "Mercadopago API error with Python" if title is None else title
    ctx = {
        "title": _title,
        "error": message,
    }
    return render_template("error.html", **ctx)


@app.route("/", methods=["POST"])
def start_oidc():
    session["response_type"] = request.form["response_type"]
    session["client_id"] = request.form["client_id"]
    session["state"] = request.form["state"]
    session["callback_url"] = request.form["callback_url"]
    authorization_url = mercadopago.get_authorization_url(
        "authorization_endpoint"
    )
    return redirect(authorization_url, code=302)


@app.route("/callback")
def process_callback():
    try:
        authorization_code = request.args["code"]
        token_endpoint = mercadopago.get_location("token_endpoint")
        access_token = current_app.config["APP_ACCESS_TOKEN"]
        res = mercadopago.process_callback_or_refresh_token(
            endpoint=token_endpoint,
            authorization_code=authorization_code,
            access_token=access_token,
        )
        update_token_info(res)
        update_settings_info()
        organization_access_url = current_app.config[
            "ORG_CONNECTION_COMPLETED_URL"
        ]
        if organization_access_url is not None:
            return redirect(organization_access_url, code=302)
        return redirect(url_for("index"))
    except Exception as e:
        logging.exception(e)
        return render_error("Error getting token!")


@app.route("/call-api", methods=["POST"])
def call_the_api():
    try:
        url = request.form["url"]
        app_access_token = session["access_token"]
        headers = {
            "Authorization": "Bearer " + app_access_token,
            "Content-Type": "application/json",
        }
        res = requests.get(url, headers=headers)
        # res = mercadopago.api_get_identification_types(
        #     app_access_token=app_access_token
        # )

        res_json = res.json()
        session["api_response"] = json.dumps(res_json, indent=4)
        update_settings_info(api_response=session["api_response"])
        return redirect(url_for("index"))
    except Exception as e:
        logging.exception(e)
        return render_error("Error calling API!")


@app.route("/refresh-access-token")
def refresh_access_token():
    try:
        access_token = current_app.config["APP_ACCESS_TOKEN"]
        refresh_token = session["refresh_token"]
        token_endpoint = mercadopago.get_location("token_endpoint")
        res = mercadopago.process_callback_or_refresh_token(
            endpoint=token_endpoint,
            refresh_token=refresh_token,
            access_token=access_token,
        )
        update_token_info(res)
        update_settings_info()
        return redirect(url_for("index"))
    except Exception as e:
        logging.exception(e)
        return render_error("Error getting refresh token!")


@app.route("/preferences")
def preferences():
    try:
        url = "https://api.mercadopago.com/checkout/preferences"
        params = {
            "items": [
                {
                    "title": "Dummy Title",
                    "description": "Dummy description",
                    "picture_url": "http://www.myapp.com/myimage.jpg",
                    "category_id": "car_electronics",
                    "quantity": 1,
                    "currency_id": "ARS",
                    "unit_price": 10,
                }
            ],
            "payer": {
                "name": "",
                "surname": "",
                "email": "",
                "phone": {},
                "identification": {},
            },
            "back_urls": {
                "failure": "http://localhost:5000/failure",
                "pending": "http://localhost:5000/pending",
                "success": "http://localhost:5000/success",
            },
        }
        # access_token = session["access_token"]
        # headers = get_headers(access_token=access_token)
        headers = {
            "Authorization": "Bearer "
            + current_app.config["APP_ACCESS_TOKEN"],
            "Content-Type": "application/json",
        }
        res = requests.post(url, headers=headers, json=params)
        res_json = res.json()
        session["api_response"] = json.dumps(res_json, indent=4)
        update_settings_info(api_response=session["api_response"])
        return redirect(url_for("index"))
    except Exception as e:
        logging.exception(e)
        return render_error("Error calling API!")


@app.route("/")
def index():
    if session.get("live_mode") and settings["api_response"] == "":
        update_settings_info()
    return render_template("main.html", **settings)


@app.route("/logout")
def logout():
    session.clear()
    delete_settings_info()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
