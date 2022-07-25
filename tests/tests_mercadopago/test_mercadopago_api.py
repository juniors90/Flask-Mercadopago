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

"""Flask-Mercadopago.

Implementation of Mercadopago API OAuth in Flask.
"""

# =====================================================================
# IMPORTS
# =====================================================================


from flask import current_app, redirect, request

from flask_mercadopago import scripts_with_sri, simple_scripts_js

from markupsafe import Markup

import pytest

# =====================================================================
# TESTS
# =====================================================================

@pytest.mark.usefixtures("client")
class TestMercadopago:
    def test_extension_init(self, app):
        with app.app_context():
            extensions = current_app.extensions
        assert "mercadopago" in extensions
        assert "mercadopago_api" not in extensions

    def test_get_endpoint(self, mercadopago):
        authorization_endpoint = mercadopago.get_location(
            "authorization_endpoint"
        )
        assert (
            authorization_endpoint
            == "https://auth.mercadopago.com.ar/authorization"
        )
        token_endpoint = mercadopago.get_location("token_endpoint")
        assert token_endpoint == "https://api.mercadopago.com/oauth/token"

    def test_get_payload(self, mercadopago):
        expected = {
            "client_id": None,
            "client_secret": None,
            "redirect_uri": None,
        }
        assert mercadopago.get_payload() == expected

    def test_get_oidc_query_string(self, mercadopago, app) -> str:
        with app.app_context():
            client_id = current_app.config["CLIENT_ID"]
            response_type = current_app.config["RESPONSE_TYPE"]
            redirect_uri = current_app.config["CALLBACK_URL"]
            state = current_app.config["STATE"]
        assert (
            mercadopago.get_oidc_query_string()
            == f"response_type={response_type}&client_id="
            + f"{client_id}&state={state}&redirect_uri={redirect_uri}"
        )

    def test_get_redirect_url(self, mercadopago, app) -> str:
        with app.app_context():
            client_id = current_app.config["CLIENT_ID"]
            response_type = current_app.config["RESPONSE_TYPE"]
            redirect_uri = current_app.config["CALLBACK_URL"]
            state = current_app.config["STATE"]
            authorization_endpoint = current_app.config[
                "AUTHORIZATION_ENDPOINT"
            ]
            token_endpoint = current_app.config["TOKEN_ENDPOINT"]

        assert (
            mercadopago.get_authorization_url("authorization_endpoint")
            == f"{authorization_endpoint}?response_type={response_type}"
            + f"&client_id={client_id}&state={state}&"
            + f"redirect_uri={redirect_uri}"
        )
        assert (
            mercadopago.get_authorization_url("token_endpoint")
            == f"{token_endpoint}?response_type={response_type}"
            + f"&client_id={client_id}&state={state}&"
            + f"redirect_uri={redirect_uri}"
        )

    def test_callback(self, app, client, mercadopago):
        @app.route("/", methods=["POST"])
        def start_oidc():
            response_type = request.form["response_type"]
            client_id = request.form["client_id"]
            state = request.form["state"]
            callback_url = request.form["callback_url"]
            redirect_url = mercadopago.get_authorization_url(
                "authorization_endpoint",
                response_type,
                client_id,
                state,
                callback_url,
            )
            return redirect(redirect_url, code=302)

        payload = {
            "response_type": "code",
            "client_id": "1148860861802028",
            "callback_url": "http://localhost:5000/callback",
            "state": "04c9ab49-09fd-11ed-9e3f-e00af63ae0de",
        }
        r = client.post("/", data=payload)
        assert r.status_code == 302

    def test_process_callback_or_refresh_token(self, app, client, mercadopago):
        @app.route("/callback")
        def process_callback():
            authorization_code = request.args["code"]
            return authorization_code

        r = client.post(
            "/callback",
            query_string={"code": "TG-62daef20bf5e710014f0454f-1162641655"},
        )
        authorization_code = str(r.data)
        token_endpoint = mercadopago.get_location("token_endpoint")
        access_token = "APP_USR-1148860861802028-072017-"
        res = mercadopago.process_callback_or_refresh_token(
            endpoint=token_endpoint,
            authorization_code=authorization_code,
            access_token=access_token,
        )
        assert res.status_code == 400
        refresh_token = "TG-62db3cbc92e2cb001328e927-1162641655"
        token_endpoint = mercadopago.get_location("token_endpoint")
        res = mercadopago.process_callback_or_refresh_token(
            endpoint=token_endpoint,
            refresh_token=refresh_token,
            access_token=access_token,
        )
        assert res.status_code == 400

    def test_mercadopago_find_local_resource(self, app, mercadopago):
        with app.app_context(), app.test_request_context():
            app.config["MERCADOPAGO_SERVE_LOCAL"] = True
            app.config["SERVER_NAME"] = "localhost"
            url_js = mercadopago.load_js()
        js = '<script src="/static/js/mercadopago/v2.js"></script>'
        assert js in url_js
        assert isinstance(url_js, Markup)

    def test_mercadopago_find_cdn_resource(self, mercadopago):
        url_js = mercadopago.load_js()
        js = '<script src="https://sdk.mercadopago.com/js/v2"></script>'
        assert js in url_js
        assert isinstance(url_js, Markup)

    def test_simple_link_js(self):
        js_html_sri = (
            "<script "
            + 'src="https://cdn.jsdelivr.net/npm/fake@2.0/dist/fake.min.js" '
            + 'integrity="sha256-VxL9ZXOItJ0i4nJLm39HIoX8u3cCRPRkDjMSXZ/RiQQ="'
            + ' crossorigin="anonymous"></script>'
        )  # noqa: E501
        js_sri = "sha256-VxL9ZXOItJ0i4nJLm39HIoX8u3cCRPRkDjMSXZ/RiQQ="
        js_url = "https://cdn.jsdelivr.net/npm/fake@2.0/dist/fake.min.js"
        js = (
            '<script src="https://cdn.jsdelivr.net/'
            + 'npm/fake@2.0/dist/fake.min.js"></script>'
        )
        assert js == simple_scripts_js(js_url)
        assert js_sri in scripts_with_sri(js_url, js_sri)
        assert js_url in scripts_with_sri(js_url, js_sri)
        assert js_html_sri == scripts_with_sri(js_url, js_sri)

    def test_get_js_script(self, mercadopago) -> str:
        js_script = mercadopago._get_js_script()
        assert (
            js_script
            == '<script src="https://sdk.mercadopago.com/js/v2"></script>'
        )
        fake_js_script = mercadopago._get_js_script(sri="fake_integrity")
        assert (
            fake_js_script
            == '<script src="https://sdk.mercadopago.com/js/v2"'
            + ' integrity="fake_integrity" '
            + 'crossorigin="anonymous"></script>'
        )

    def test_get_sri(self, mercadopago) -> str:
        js_script = mercadopago._get_sri(version="mercadopago_js")
        assert js_script is None
        js_script = mercadopago._get_sri(sri="fake_sri")
        assert js_script == "fake_sri"

    def api_get_identification_types(self):
        pass
