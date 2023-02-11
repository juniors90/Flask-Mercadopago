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


from flask import current_app

import pytest

# =====================================================================
# TESTS
# =====================================================================


@pytest.mark.usefixtures("client")
class TestPreference:
    def test_create_preference(self, mercadopago, app) -> str:
        with app.app_context():
            current_app.config[
                "APP_ACCESS_TOKEN"
            ] = "APP_USR-1148860861802028-072017-b6355e068517038cb6cb45e7eafe4ec5-1162652745"

        preference_object = {
            "items": [
                {
                    "description": "Test Update Success",
                    "id": "456",
                    "picture_url": "http://product1.image.png",
                    "quantity": 1,
                    "title": "Item 1",
                    "currency_id": "ARS",
                    "unit_price": 205,
                }
            ]
        }
        preference_saved = mercadopago.preference().create(preference_object)
        assert preference_saved["status"] == 201

        preference_object["items"][0]["title"] = "Testing 1 2 3"

        preference_update = mercadopago.preference().update(
            preference_saved["response"]["id"], preference_object
        )
        assert preference_update["status"] == 200

        preference_saved = mercadopago.preference().get(
            preference_saved["response"]["id"]
        )

        assert (
            preference_saved["response"]["items"][0]["title"]
            == preference_object["items"][0]["title"]
        )
