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
class TestUser:
    def test_get_user(self, mercadopago, app) -> str:
        with app.app_context():
            current_app.config[
                "APP_ACCESS_TOKEN"
            ] = "APP_USR-1148860861802028-072017-b6355e068517038cb6cb45e7eafe4ec5-1162652745"  # noqa: E501

        assert mercadopago.user().get()["status"] == 200
