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

from flask import current_app

import pytest

# =====================================================================
# TESTS
# =====================================================================

@pytest.mark.usefixtures("client")
class TestCustomer:
    """
    Test Module: Customer
    """

    def test_all(self, mercadopago, app) -> str:
        """
        Test Function: Customer
        """
        with app.app_context():
            current_app.config[
                "APP_ACCESS_TOKEN"
            ] = "APP_USR-558881221729581-091712-44fdc612e60e3e638775d8b4003edd51-471763966"
        random_email_id = random.randint(100000, 999999)
        customer_object = {
            "email": f"test_payer_{random_email_id}@testuser.com",
            "first_name": "Katniss",
            "last_name": "Everdeen",
            "phone": {
                "area_code": "03492",
                "number": "432334"
            },
            "identification": {
                "type": "DNI",
                "number": "29804555"
            },
            "description": "customer description"
        }

        customer_saved = mercadopago.customer().create(customer_object)
        assert customer_saved["status"] == 201

        customer_update = mercadopago.customer().update(
            customer_saved["response"]["id"], {"last_name": "Payer"})
        assert customer_update["status"] == 200

        customer_updated = mercadopago.customer().get(
            customer_saved["response"]["id"])
        assert customer_updated["response"]["last_name"] == "Payer"

        customer_deleted = mercadopago.customer().delete(
            customer_saved["response"]["id"])
        assert customer_deleted["status"] == 200

