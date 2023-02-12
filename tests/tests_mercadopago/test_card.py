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

import random
from datetime import datetime

from flask import current_app

import pytest


# =====================================================================
# TESTS
# =====================================================================


@pytest.mark.usefixtures("client")
class TestCard:
    """
    Test Module: Card
    """

    _customer_id = None

    def test_all(self, mercadopago, app):
        """
        Test Function: Card
        """
        with app.app_context():
            current_app.config[
                "APP_ACCESS_TOKEN"
            ] = "APP_USR-558881221729581-091712-44fdc612e60e3e638775d8b4003edd51-471763966"  # noqa: E501

        random_email_id = random.randint(100000, 999999)
        customer_object = {
            "email": f"test_payer_{random_email_id}@testuser.com",
            "first_name": "Rafa",
            "last_name": "Williner",
            "phone": {"area_code": "03492", "number": "432334"},
            "identification": {"type": "DNI", "number": "29804555"},
            "description": "customer description",
        }

        customer_data = mercadopago.customer().create(customer_object)
        self._customer_id = customer_data["response"]["id"]

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

        card_object = {
            "customer_id": self._customer_id,
            "token": card_token_created["response"]["id"],
        }

        card_created = mercadopago.card().create(
            self._customer_id, card_object
        )
        assert card_created["status"] in [200, 201]
        assert (
            mercadopago.card().get(
                self._customer_id, card_created["response"]["id"]
            )["status"]
            == 200
        )

        mercadopago.card().delete(
            self._customer_id, card_created["response"]["id"]
        )
