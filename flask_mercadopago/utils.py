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

"""Flask-Mercadopago

Implementation of Mercadopago OAuth in Flask.
"""

# =============================================================================
# FUNCTIONS
# =============================================================================


def get_payload(
    client_id: str = None, client_secret: str = None, redirect_uri: str = None
) -> dict:
    """Generate a basic payload (or data).

    Parameters
    ----------
    client_id : str
        The client id for organization access.
    client_secret : str
        The client secret for organization access.
    redirect_uri: str
        The redirect uri for organization access.

    Return
    ------
    payload : dict
        The payload for the connection.
    """
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
    }
    return payload


def get_headers(access_token: str) -> dict:
    """Generate a basic authehntication header.

    Parameters
    ----------
    access_token : str
        An access token.

    Return
    ------
    headers : dict
        The headers for the connection.
    """
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
    }
    return headers
