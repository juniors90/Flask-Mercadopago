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
class TestPlan:
    """
    Test Module: Preference
    """

    def test_create_plan(self, mercadopago, app) -> str:
        """
        Test Module: Plan
        """
        with app.app_context():
            current_app.config[
                "APP_ACCESS_TOKEN"
            ] = "APP_USR-1148860861802028-072017-b6355e068517038cb6cb45e7eafe4ec5-1162652745"

        random_reason_number = random.randint(100000, 999999)

        plan_object_all_options_payload = {
            "auto_recurring": {
                "frequency": 1,
                "frequency_type": "months",
                "repetitions": 12,
                "billing_day": 5,
                "free_trial": {"frequency": 2, "frequency_type": "days"},
                "transaction_amount": 60,
                "currency_id": "ARS",
            },
            "back_url": "https://www.mercadopago.com.ar/subscriptions",
            "reason": f"Test Plan #{random_reason_number}",
        }
        plan_object_mandatory_options_payload = {
            "auto_recurring": {
                "frequency": 1,
                "frequency_type": "months",
                "transaction_amount": 60,
                "currency_id": "ARS",
            },
            "back_url": "https://www.mercadopago.com.ar/subscriptions",
            "reason": f"Test Plan (mandatory) #{random_reason_number}",
        }

        plan_response = mercadopago.plan().create(
            plan_object_all_options_payload
        )
        assert plan_response["status"] == 201

        plan_object = plan_response["response"]
        assert plan_object["status"] == "active"

        # Validate it works with minimal required options
        plan_mandatory_options = mercadopago.plan().create(
            plan_object_mandatory_options_payload
        )
        assert plan_mandatory_options["status"] == 201
        assert plan_mandatory_options["response"]["status"] == "active"

        plan_object["reason"] = "MercadoPago API Test"
        update_response = mercadopago.plan().update(
            plan_object["id"], plan_object
        )
        assert update_response["status"] == 200
        update_object = update_response["response"]
        assert update_object["reason"] == plan_object["reason"]
        assert update_object["status"] == "active"

        get_response = mercadopago.plan().get(plan_object["id"])
        assert get_response["status"] == 200
        get_object = get_response["response"]
        assert get_object["id"] == plan_object["id"]

        search_response = mercadopago.plan().search()
        assert search_response["status"] == 200
        search_object = search_response["response"]
        assert "results" in search_object
        assert isinstance(search_object["results"], list)
