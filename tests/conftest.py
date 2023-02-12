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

import typing as t

import flask

import pytest as pt

if t.TYPE_CHECKING:
    from flask.testing import FlaskClient


@pt.fixture(autouse=True)
def app() -> "flask.Flask":
    app = flask.Flask(__name__)
    app.testing = True
    app.secret_key = "for test"
    app.debug = False
    yield app


@pt.fixture
def client(app: "flask.Flask") -> "FlaskClient":
    context = app.test_request_context()
    context.push()

    with app.test_client() as client:
        yield client

    context.pop()
