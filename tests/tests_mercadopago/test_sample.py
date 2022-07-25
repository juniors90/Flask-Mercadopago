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
# TEST
# =============================================================================


def test_sample_request(app, client):
    @app.get("/sample")
    def sample():
        return "OK"

    r = client.get("/sample")
    assert r.status_code == 200
    assert r.data == b"OK"
