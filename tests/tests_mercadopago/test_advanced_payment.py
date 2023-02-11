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

import uuid
from datetime import datetime, timedelta

from flask import current_app

import pytest


@pytest.mark.usefixtures("client")
class TestAdvancedPayment:
    """
    Test Module: Advanced Payment
    """

    @pytest.mark.skip(reason="Outdated API usage")
    def test_all(self, mercadopago, app):
        """
        Test Function: Advanced Payment
        """

        with app.app_context():
            current_app.config[
                "APP_ACCESS_TOKEN"
            ] = "APP_USR-558881221729581-091712-44fdc612e60e3e638775d8b4003edd51-471763966"

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

        advanced_payment_object = {
            "application_id": "59441713004005",
            "payments": [
                {
                    "payment_method_id": "master",
                    "payment_type_id": "credit_card",
                    "token": card_token_created["response"]["id"],
                    "date_of_expiration": (
                        datetime.now() + timedelta(days=10)
                    ).strftime("%Y-%m-%d %H:%M:%S.%f"),
                    "transaction_amount": 100.0,
                    "installments": 1,
                    "processing_mode": "aggregator",
                    "description": "description",
                    "external_reference": str(uuid.uuid4().int),
                    "statement_descriptor": "ADVPAY",
                }
            ],
            "disbursements": [
                {
                    "collector_id": "488656838",
                    "amount": 60.0,
                    "external_reference": "Seller2" + str(uuid.uuid4().int),
                    "application_fee": 0.5,
                }
            ],
            "payer": {
                "id": "649457098-FybpOkG6zH8QRm",
                "type": "customer",
                "email": "test_payer_9999988@testuser.com",
                "first_name": "Test",
                "last_name": "User",
                "address": {
                    "zip_code": "06233200",
                    "street_name": "Street",
                    "street_number": 123,
                },
                "identification": {"type": "CPF", "number": "19119119100"},
            },
            "external_reference": "Adv" + str(uuid.uuid4().int),
            "description": "description",
            "binary_mode": False,
            "capture": False,
            "additional_info": {
                "ip_address": "127.0.0.1",
                "payer": {
                    "first_name": "Test",
                    "last_name": "User",
                    "registration_date": (
                        datetime.now() - timedelta(days=10)
                    ).strftime("%Y-%m-%d %H:%M:%S.%f"),
                },
                "items": [
                    {
                        "id": "123",
                        "title": "title",
                        "picture_url": "https://www.mercadopago.com/logomp3.gif",
                        "description": "description",
                        "category_id": "category",
                        "quantity": 1,
                        "unit_price": 100.0,
                    }
                ],
                "shipments": {
                    "receiver_address": {
                        "zip_code": "06233200",
                        "street_name": "Street",
                        "street_number": 123,
                    }
                },
            },
        }

        advanced_payment_created = mercadopago.advanced_payment().create(
            advanced_payment_object
        )
        assert advanced_payment_created["status"] == 201

        advanced_payment_found = mercadopago.advanced_payment().get(
            advanced_payment_created["response"]["id"]
        )
        assert advanced_payment_found["status"] == 200
