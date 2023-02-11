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

# =============================================================================
# TESTS
# =============================================================================


def test_can_import_package():
    import flask_mercadopago  # noqa


def test_can_initialize_app_and_extesion():
    from flask import Flask

    from flask_mercadopago import Mercadopago

    app = Flask(__name__)
    Mercadopago(app)


def test_can_initialize_app_and_extesion_with_factory_func():
    from flask import Flask

    from flask_mercadopago import Mercadopago

    app = Flask(__name__)
    mercadopago = Mercadopago()
    mercadopago.init_app(app)
