#!/usr/bin/env python3
"""
Basic Authentication module
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Basic Authentication class
    """

    def __init__(self):
        super().__init__()