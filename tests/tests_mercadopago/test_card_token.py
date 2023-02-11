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

from datetime import datetime

from flask import current_app

import pytest


# =====================================================================
# TESTS
# =====================================================================


@pytest.mark.usefixtures("client")
class TestCardToken:
    """
    Test Module: Card Token
    """

    def test_all(self, mercadopago, app):
        """
        Test Function: Card Token
        """
        with app.app_context():
            current_app.config[
                "APP_ACCESS_TOKEN"
            ] = "APP_USR-1148860861802028-072017-b6355e068517038cb6cb45e7eafe4ec5-1162652745"

        card_token_object = {
            "card_number": "4074090000000004",
            "security_code": "123",
            "expiration_year": datetime.now().strftime("%Y"),
            "expiration_month": "12",
            "cardholder": {
                "name": "APRO",
                "identification": {"CPF": "19119119100"},
            },
        }

        card_token_created = mercadopago.card_token().create(card_token_object)

        assert card_token_created["status"] == 201
        assert (
            mercadopago.card_token().get(card_token_created["response"]["id"])[
                "status"
            ]
            == 200
        )
