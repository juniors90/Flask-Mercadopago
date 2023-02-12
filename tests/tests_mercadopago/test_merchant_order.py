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

from flask import current_app

import pytest

# =====================================================================
# TESTS
# =====================================================================


@pytest.mark.usefixtures("client")
class TestMerchantOrder:
    """
    Test Module: Merchant Order
    """

    def test_all(self, mercadopago, app) -> str:
        """
        Test Function: Merchant Order
        """
        with app.app_context():
            current_app.config[
                "APP_ACCESS_TOKEN"
            ] = "APP_USR-558881221729581-091712-44fdc612e60e3e638775d8b4003edd51-471763966"  # noqa: E501

        preference_object = {
            "items": [
                {
                    "description": "Test Update Success",
                    "id": "5678",
                    "picture_url": "http://product1.image.png",
                    "quantity": 1,
                    "title": "Item 1",
                    "currency_id": "R$",
                    "unit_price": 20.5,
                }
            ]
        }

        preference_saved = mercadopago.preference().create(preference_object)

        merchant_order_object = {
            "preference_id": preference_saved["response"]["id"],
            "site_id": "MLB",
            "notification_url": "https://seller/notification",
            "additional_info": "Aditional info",
            "external_reference": str(uuid.uuid4().int),
            "marketplace": "NONE",
            "items": [
                {
                    "description": "Test Update Success",
                    "id": "5678",
                    "picture_url": "http://product1.image.png",
                    "quantity": 1,
                    "title": "Item 1",
                    "currency_id": "BRL",
                    "unit_price": 20.5,
                }
            ],
        }

        merchant_order_created = mercadopago.merchant_order().create(
            merchant_order_object
        )
        assert merchant_order_created["status"] == 201

        merchant_order_updated = mercadopago.merchant_order().update(
            merchant_order_created["response"]["id"],
            {"additional_info": "Info 2"},
        )
        assert merchant_order_updated["status"] == 200

        merchant_order_finded = mercadopago.merchant_order().get(
            merchant_order_created["response"]["id"]
        )
        assert merchant_order_finded["status"] == 200
        assert merchant_order_finded["response"]["additional_info"] == "Info 2"
