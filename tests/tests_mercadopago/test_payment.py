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
class TestPayment:
    """
    Test Module: Payment
    """

    def test_create_and_find(self, mercadopago, app) -> str:
        """
        Test Function: Payment
        """
        with app.app_context():
            current_app.config[
                "APP_ACCESS_TOKEN"
            ] = "APP_USR-558881221729581-091712-44fdc612e60e3e638775d8b4003edd51-471763966"  # noqa: E501

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

        payment_object = {
            "token": card_token_created["response"]["id"],
            "installments": 1,
            "transaction_amount": 58.80,
            "description": "Point Mini a maquininha que dá o dinheiro de suas vendas na hora",  # noqa: E501
            "payment_method_id": "visa",
            "payer": {
                "email": "test_user_123456@testuser.com",
                "identification": {"number": "19119119100", "type": "CPF"},
            },
            "notification_url": "https://www.suaurl.com/notificacoes/",
            "sponsor_id": None,
            "binary_mode": False,
            "external_reference": "MP0001",
            "statement_descriptor": "MercadoPago",
            "additional_info": {
                "items": [
                    {
                        "id": "PR0001",
                        "title": "Point Mini",
                        "description": "Producto Point para cobros con tarjetas mediante bluetooth",  # noqa: E501
                        "picture_url": "https://http2.mlstatic.com/resources/frontend/statics/growth-sellers-landings/device-mlb-point-i_medium@2x.png",  # noqa: E501
                        "category_id": "electronics",
                        "quantity": 1,
                        "unit_price": 58.80,
                    }
                ],
                "payer": {
                    "first_name": "Nome",
                    "last_name": "Sobrenome",
                    "address": {
                        "zip_code": "06233-200",
                        "street_name": "Av das Nacoes Unidas",
                        "street_number": 3003,
                    },
                    "registration_date": "2019-01-01T12:01:01.000-03:00",
                    "phone": {"area_code": "011", "number": "987654321"},
                },
                "shipments": {
                    "receiver_address": {
                        "street_name": "Av das Nacoes Unidas",
                        "street_number": 3003,
                        "zip_code": "06233200",
                        "city_name": "Buzios",
                        "state_name": "Rio de Janeiro",
                    }
                },
            },
        }

        payment_created = mercadopago.payment().create(payment_object)
        assert payment_created["status"] == 201

        payment_found = mercadopago.payment().get(
            payment_created["response"]["id"]
        )
        assert payment_found["status"] == 200
