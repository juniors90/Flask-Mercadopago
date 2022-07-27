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

import uuid
import warnings

from flask import Blueprint, Markup, current_app, url_for

import markupsafe

import requests

from .utils import get_headers, get_payload


# docstr-coverage:excused `no one is reading this anyways`
def raise_helper(message):  # pragma: no cover
    raise RuntimeError(message)


def scripts_with_sri(url: str, sri: str) -> str:
    """Create a <script> element.

    Parameters
    ----------
    url : ``str``
        Specifies the URL of an external script file.
    sri : ``str``
        The Subresource Integrity value.


    Return
    ------
    script : ``str``
        The string with form to <script> tag is used to
        embed a client-side script.
    """
    script = f'<script src="{url}" integrity="{sri}" crossorigin="anonymous"></script>'  # noqa: E501
    return script


def simple_scripts_js(url: str) -> str:
    """Create a <script> element.

    Parameters
    ----------
    url: ``str``
        Specifies the URL of an external script file.

    Return
    ------
    script : str
        The sctring with form to <script> tag is used to
        embed a client-side script.
    """
    script = f'<script src="{url}"></script>'
    return script


class Mercadopago(object):
    """Base extension class for different of Mercadopago versions.

    Initilize the extension::

        from flask import Flask
        from flask_mercadopago import Mercadopago
        app = Flask(__name__)
        mercadopago = Mercadopago(app)

    Or with the application factory::

        from flask import Flask
        from flask_mercadopago import Mercadopago
        mercadopago = Mercadopago()
        def create_app():
            app = Flask(__name__)
            mercadopago.init_app(app)
            return app
    """

    mercadopago_js_version = None
    mercadopago_js_integrity = None
    cdk_base = "https://sdk.mercadopago.com"
    mercadopago_js_filename = "v2"
    static_folder = "mercadopago"

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Application factory."""

        # default current_app.config
        app.config.setdefault("APP_ACCESS_TOKEN", None)
        app.config.setdefault(
            "AUTHORIZATION_ENDPOINT",
            "https://auth.mercadopago.com.ar/authorization",
        )
        app.config.setdefault("BASE_URL", "https://api.mercadopago.com/v1")
        app.config.setdefault("CALLBACK_URL", None)
        app.config.setdefault("CLIENT_ID", None)
        app.config.setdefault("CLIENT_SECRET", None)
        app.config.setdefault("ORG_CONNECTION_COMPLETED_URL", None)
        app.config.setdefault("STATE", uuid.uuid1())
        app.config.setdefault(
            "TOKEN_ENDPOINT", "https://api.mercadopago.com/oauth/token"
        )
        app.config.setdefault("RESPONSE_TYPE", "code")
        app.config.setdefault("MERCADOPAGO_SERVE_LOCAL", False)

        if not hasattr(app, "extensions"):  # pragma: no cover
            app.extensions = {}

        app.extensions["mercadopago"] = self

        blueprint = Blueprint(
            "mercadopago",
            __name__,
            static_folder=f"static/{self.static_folder}",
            static_url_path=f"{app.static_url_path}",
            template_folder="templates",
        )

        app.register_blueprint(blueprint)
        app.jinja_env.globals["mercadopago"] = self
        app.jinja_env.globals["warn"] = warnings.warn
        app.jinja_env.globals["raise"] = raise_helper
        app.jinja_env.add_extension("jinja2.ext.do")

    def get_oidc_query_string(
        self,
        response_type: str = None,
        client_id: str = None,
        state: str = None,
        redirect_uri: str = None,
    ) -> str:
        """Generate oidc query string resources with given version.

        Parameters
        ----------
        response_type : ``str`` or ``None`` (optional)
            The response type. The config key ``RESPONSE_TYPE`` is ``"code"``.
        client_id : ``str`` or ``None`` (optional)
            The Unique CLIENT_ID that identifies your application given
            by Mercadopago.
        state : ``str`` or ``None`` (optional)
            A ramdom ID value.
        redirect_uri : ``str`` or ``None`` (optional)
            The URL reported in the Redirect URL field of your application.

        Return
        ------
        query_params_str : ``str``
            The query string.

        Examples
        --------
        >>> import uuid
        >>> from flask import Flask
        >>> from flask_mercadopago import Mercadopago
        >>> app = Flask("app")
        >>> mercadopago = Mercadopago(app)
        >>> # The config keys currently understood by the extension:
        >>> app.config["CLIENT_ID"] = "1314151617108901"
        >>> app.config["RESPONSE_TYPE"] = "code"
        >>> app.config["STATE"] = uuid.uuid1()
        >>> app.config["CALLBACK_URL"]="http://localhost:5000/callback"
        >>> with app.app_context():
        ...     mercadopago.get_oidc_query_string()
        ...
        'response_type=code&client_id=1314151617108901&
        state=5e092018-0ab8-11ed-8e81-e00af63ae0de
        &redirect_uri=http://localhost:5000/callback'
        >>>
        """
        _client_id = (
            current_app.config["CLIENT_ID"] if client_id is None else client_id
        )
        _response_type = (
            current_app.config["RESPONSE_TYPE"]
            if response_type is None
            else response_type
        )
        _redirect_uri = (
            current_app.config["CALLBACK_URL"]
            if redirect_uri is None
            else redirect_uri
        )
        _state = current_app.config["STATE"] if state is None else state
        query_params = {
            "response_type": _response_type,
            "client_id": _client_id,
            "state": _state,
            "redirect_uri": _redirect_uri,
        }
        params = [f"{key}={value}" for key, value in query_params.items()]
        query_params_str = "&".join(params)
        return query_params_str

    def get_payload(self) -> dict:
        """Generate a basic payload (or data).

        Return
        ------
        payload : ``dict``
            The payload for the connection.

        Examples
        --------
        >>> from flask import Flask
        >>> from flask_mercadopago import Mercadopago
        >>> app = Flask("app")
        >>> mercadopago = Mercadopago(app)
        >>> # The config keys currently understood by the extension:
        >>> app.config["CLIENT_ID"] = "1314151617108901"
        >>> app.config["CLIENT_SECRET"] = "C8HUg6ErZF"
        >>> app.config["CALLBACK_URL"]="http://localhost:5000/callback"
        >>> with app.app_context():
        ...     mercadopago.get_payload()
        ...
        {'client_id': '1314151617108901', 'client_secret': 'C8HUg6ErZF',
        'redirect_uri': 'http://localhost:5000/callback'}
        >>>
        """
        payload = get_payload(
            client_id=current_app.config["CLIENT_ID"],
            client_secret=current_app.config["CLIENT_SECRET"],
            redirect_uri=current_app.config["CALLBACK_URL"],
        )
        return payload

    def process_callback_or_refresh_token(
        self,
        endpoint: str,
        access_token: str,
        authorization_code: str = None,
        refresh_token: str = None,
    ) -> requests.Response:
        """Sends a POST request.

        Parameters
        ----------
        access_token : ``str`` or ``None`` (optional)
            An access token.
        authorization_code : ``str`` or ``None`` (optional)
            The code provided by the Mercadopago authentication server.
        endpoint : ``str``
            The endopoint for process callback or refresh token.
        refresh_token : ``str`` or ``None`` (optional)
            A value received when the access token is created.

        Return
        ------
        res : ``requests.Response``
            ``Response.Response`` object.
        """
        headers = get_headers(access_token=access_token)
        payload = self.get_payload()
        if authorization_code:
            payload["grant_type"] = "authorization_code"
            payload["code"] = authorization_code
        if refresh_token:
            payload["grant_type"] = "refresh_token"
            payload["refresh_token"] = refresh_token
        res = requests.post(endpoint, headers=headers, params=payload)
        return res

    def api_get_identification_types(
        self, access_token: str
    ) -> requests.Request:
        """Consult all the types of documents available by country.

        Get a list with the ID and details of each one.

        Parameters
        ----------
        access_token : ``str``
            An access token.

        Return
        ------
        res : requests.Response
            ``Response.Response`` object.
        """
        url = current_app.config["BASE_URL"] + "/identification_types"
        headers = get_headers(access_token=access_token)
        res = requests.get(url, headers=headers)
        return res

    def get_location(self, endpoint: str) -> str:
        """Generate the authorization or token endpoint resources.

        Parameters
        ----------
        endpoint : ``str``
            The query string given by for the authorization or token endpoint.

        Return
        ------
        location : str
            The location from metadata for the application connection.

        Examples
        --------
        >>> from flask import Flask
        >>> from flask_mercadopago import Mercadopago
        >>> app = Flask("app")
        >>> mercadopago = Mercadopago(app)
        >>> # call the method with "authorization_endpoint" value.
        >>> with app.app_context():
        ...     mercadopago.get_location("authorization_endpoint")
        ...
        'https://auth.mercadopago.com.ar/authorization'
        >>> # call the method with "token_endpoint" value.
        >>> with app.app_context():
        ...     mercadopago.get_location("token_endpoint")
        ...
        'https://api.mercadopago.com/oauth/token'
        >>>
        """
        endpoint_dic = {
            "authorization_endpoint": current_app.config[
                "AUTHORIZATION_ENDPOINT"
            ],
            "token_endpoint": current_app.config["TOKEN_ENDPOINT"],
        }
        return endpoint_dic[endpoint]

    def get_authorization_url(
        self,
        endpoint: str,
        response_type: str = None,
        client_id: str = None,
        state: str = None,
        redirect_uri: str = None,
    ) -> str:
        """Create the necessary authorization URL to operate your application.

        Parameters
        ----------
        endpoint : ``str``
            The query string given by for the authorization endpoint.
        response_type : ``str`` or ``None`` (optional)
            The response type. The config key ``RESPONSE_TYPE`` is ``"code"``.
        client_id : ``str`` or ``None`` (optional)
            The Unique CLIENT_ID that identifies your application given
            by Mercadopago.
        state : ``str`` or ``None`` (optional)
            A ramdom ID value.
        redirect_uri : ``str`` or ``None`` (optional)
            The URL reported in the Redirect URL field of your application.

        Return
        ------
        authorization_url : ``dict``
            The authorization URL the connection.

        Examples
        --------
        >>> import uuid
        >>> from flask import Flask
        >>> from flask_mercadopago import Mercadopago
        >>> app = Flask("app")
        >>> mercadopago = Mercadopago(app)
        >>> # The config keys currently understood by the extension:
        >>> app.config["CLIENT_ID"] = "1314151617108901"
        >>> app.config["RESPONSE_TYPE"] = "code"
        >>> app.config["STATE"] = uuid.uuid1()
        >>> app.config["CALLBACK_URL"] = "http://localhost:5000/callback"
        >>> # call the method with "authorization_endpoint" value.
        >>> with app.app_context():
        ...     mercadopago.get_authorization_url("authorization_endpoint")
        ...
        'https://auth.mercadopago.com.ar/authorization?response_type=code
        &client_id=1314151617108901&state=5e092018-0ab8-11ed-8e81-e00af63ae0de
        &redirect_uri=http://localhost:5000/callback'
        """
        query_string = self.get_oidc_query_string(
            response_type, client_id, state, redirect_uri
        )
        authorization_endpoint = self.get_location(endpoint)
        authorization_url = f"{authorization_endpoint}?{query_string}"
        return authorization_url

    def load_js(
        self,
        version: str = None,
        mercadopago_sri: str = None,
    ) -> markupsafe.Markup:
        """Load Mercadopago SDK client side given for this version.

        Parameters
        ----------
        version : ``str`` or ``None`` (optional)
            The version of Mercadopago SDK client side.
        mercadopago_sri : ``str`` or ``None`` (optional)
            Subresource integrity for Mercadopago SDK client side.

        Return
        ------
        scripts : ``markupsafe.Markup``
            The <script> tag for JavaScipt Mercadopago SDK in client side file.
        """
        mp_version = (
            self.mercadopago_js_version if version is None else version
        )
        mp_sri = self._get_sri("mercadopago_js", mp_version, mercadopago_sri)
        fui_js = self._get_js_script("mercadopago", mp_sri)
        script = Markup(f"{fui_js}")
        return script

    def _get_sri(
        self, name: str = None, version: str = None, sri: str = None
    ) -> str:
        """Get subresource integrity for Mercadopago SDK client side."""
        serve_local = current_app.config["MERCADOPAGO_SERVE_LOCAL"]

        sris = {
            "mercadopago_js": self.mercadopago_js_integrity,
        }

        versions = {
            "mercadopago_js": self.mercadopago_js_version,
        }
        _name = "mercadopago_js" if name is None else name
        if sri is not None:
            return sri
        if version == versions[_name] and serve_local is False:
            return sris[_name]
        return None

    def _get_js_script(self, name: str = None, sri: str = None) -> str:
        """Get <script> tag for JavaScipt resources."""
        serve_local = current_app.config["MERCADOPAGO_SERVE_LOCAL"]
        paths = {
            "mercadopago": f"{self.mercadopago_js_filename}",
        }
        _name = "mercadopago" if name is None else name
        if serve_local:
            path = "js/mercadopago"
            url = url_for(
                "mercadopago.static", filename=f"{path}/{paths[_name]}.js"
            )
        else:
            url = self.cdk_base + f"/js/{paths[_name]}"

        if sri:
            script_html = scripts_with_sri(url, sri)
        else:
            script_html = simple_scripts_js(url)
        return script_html
