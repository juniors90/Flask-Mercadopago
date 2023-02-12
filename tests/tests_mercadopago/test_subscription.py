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
class TestSubscription:
    """
    Test Module: Preference
    """

    _customer_id = None
    _customer_email = None
    _plan_id = None

    def test_all(self, mercadopago, app):
        """
        Test Module: Subscription
        """
        with app.app_context():
            current_app.config[
                "APP_ACCESS_TOKEN"
            ] = "APP_USR-558881221729581-091712-44fdc612e60e3e638775d8b4003edd51-471763966"  # noqa: E501

        random_email_id = random.randint(100000, 999999)

        customer_object = {
            "email": f"test_payer_{random_email_id}@testuser.com",
            "first_name": "Python",
            "last_name": "Mercado",
            "phone": {"area_code": "03492", "number": "432334"},
            "identification": {"type": "DNI", "number": "29804555"},
            "description": "customer description",
        }

        customer_data = mercadopago.customer().create(customer_object)

        self._customer_id = customer_data["response"]["id"]
        self._customer_email = customer_data["response"]["email"]

        plan_object = {
            "auto_recurring": {
                "frequency": 1,
                "frequency_type": "months",
                "transaction_amount": 60,
                "currency_id": "BRL",
            },
            "back_url": "https://www.mercadopago.com.co/subscriptions",
            "reason": f"Test Plan #{random.randint(100000, 999999)}",
        }

        plan_data = mercadopago.plan().create(plan_object)
        self._plan_id = plan_data["response"]["id"]

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
        card_token = mercadopago.card_token().create(card_token_object)
        card_token_id = card_token["response"]["id"]

        random_reason_number = random.randint(100000, 999999)
        subscription_payload = {
            "back_url": "https://www.mercadopago.com.co/subscriptions",
            "reason": f"MercadoPago API Subscription #{random_reason_number}",
            "external_reference": "CustomIdentifier",
            "payer_email": self._customer_email,
            "preapproval_plan_id": self._plan_id,
            "card_token_id": card_token_id,
            "status": "authorized",
        }

        subscription_response = mercadopago.subscription().create(
            subscription_payload
        )
        assert subscription_response["status"] == 201

        subscription_object = subscription_response["response"]
        assert "init_point" in subscription_object
        assert (
            subscription_object["external_reference"]
            == subscription_payload["external_reference"]
        )
        assert subscription_object["status"] == "authorized"

        update_payload = {
            "reason": f"MercadoPago API Subscription A #{random_reason_number}",  # noqa: E501
        }
        update_response = mercadopago.subscription().update(
            subscription_object["id"], update_payload
        )
        assert update_response["status"] == 200
        update_object = update_response["response"]
        assert update_object["reason"] == update_payload["reason"]

        get_response = mercadopago.subscription().get(
            subscription_object["id"]
        )
        assert get_response["status"] == 200
        get_object = get_response["response"]
        assert get_object["id"] == subscription_object["id"]

        search_response = mercadopago.subscription().search()
        assert search_response["status"] == 200
        search_object = search_response["response"]
        assert "results" in search_object
        assert isinstance(search_object["results"], list)
        mercadopago.customer().delete(self._customer_id)

    def test_create_subscriptions_without_a_plan(self, mercadopago, app):
        """
        Test Module: Subscription

        Test subscription creation without a plan
        """
        with app.app_context():
            current_app.config[
                "APP_ACCESS_TOKEN"
            ] = "APP_USR-558881221729581-091712-44fdc612e60e3e638775d8b4003edd51-471763966"  # noqa: E501

        random_email_id = random.randint(100000, 999999)

        customer_object = {
            "email": f"test_payer_{random_email_id}@testuser.com",
            "first_name": "Python",
            "last_name": "Mercado",
            "phone": {"area_code": "03492", "number": "432334"},
            "identification": {"type": "DNI", "number": "29804555"},
            "description": "customer description",
        }

        customer_data = mercadopago.customer().create(customer_object)

        self._customer_id = customer_data["response"]["id"]
        self._customer_email = customer_data["response"]["email"]

        plan_object = {
            "auto_recurring": {
                "frequency": 1,
                "frequency_type": "months",
                "transaction_amount": 60,
                "currency_id": "BRL",
            },
            "back_url": "https://www.mercadopago.com.co/subscriptions",
            "reason": f"Test Plan #{random.randint(100000, 999999)}",
        }

        plan_data = mercadopago.plan().create(plan_object)
        self._plan_id = plan_data["response"]["id"]

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
        card_token = mercadopago.card_token().create(card_token_object)
        card_token_id = card_token["response"]["id"]

        random_reason_number = random.randint(100000, 999999)
        subscription_payload = {
            "back_url": "https://www.mercadopago.com.co/subscriptions",
            "reason": f"MercadoPago API Subscription B #{random_reason_number}",  # noqa: E501
            "external_reference": "CustomIdentifier",
            "payer_email": self._customer_email,
            "card_token_id": card_token_id,
            "auto_recurring": {
                "frequency": 1,
                "frequency_type": "months",
                "transaction_amount": 60,
                "currency_id": "BRL",
            },
            "status": "authorized",
        }

        subscription_response = mercadopago.subscription().create(
            subscription_payload
        )
        assert subscription_response["status"] == 201

        subscription_object = subscription_response["response"]
        assert "init_point" in subscription_object
        assert (
            subscription_object["external_reference"]
            == subscription_payload["external_reference"]
        )
        assert subscription_object["status"] == "authorized"
        mercadopago.customer().delete(self._customer_id)
