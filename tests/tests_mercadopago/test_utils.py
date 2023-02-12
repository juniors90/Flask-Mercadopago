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

# =============================================================================
# IMPORTS
# =============================================================================

from flask_mercadopago.utils import get_headers, get_payload

import pytest

# =============================================================================
# TEST
# =============================================================================


@pytest.mark.parametrize(
    "access_token, expected",
    [
        (
            "YOUR_ACCESS_TOKEN",
            {
                "Authorization": "Bearer YOUR_ACCESS_TOKEN",
                "Content-Type": "application/json",
            },
        ),
        (
            "foo",
            {
                "Authorization": "Bearer foo",
                "Content-Type": "application/json",
            },
        ),
        (
            "bar",
            {
                "Authorization": "Bearer bar",
                "Content-Type": "application/json",
            },
        ),
    ],
)
def test_get_headers(access_token, expected):
    assert get_headers(access_token) == expected


@pytest.mark.parametrize(
    "client_id, client_secret, redirect_uri, expected",
    [
        (
            "123456",
            "098765",
            "https://www.mercadopago.com.ar/",
            {
                "client_id": "123456",
                "client_secret": "098765",
                "redirect_uri": "https://www.mercadopago.com.ar/",
            },
        ),
        (
            "client_id",
            "client_secret",
            "https://www.google.com.ar/",
            {
                "client_id": "client_id",
                "client_secret": "client_secret",
                "redirect_uri": "https://www.google.com.ar/",
            },
        ),
    ],
)
def test_get_payload(client_id, client_secret, redirect_uri, expected):
    assert get_payload(client_id, client_secret, redirect_uri) == expected


"""
@pytest.mark.parametrize("access_token, key, value, expected",
    []
)
def test_set_headers(access_token, key, value, expected):
    assert set_headers(access_token, key, value) == expected
"""
