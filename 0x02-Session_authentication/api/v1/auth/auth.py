#!/usr/bin/env python3
"""
Authentication module for the API
"""
from typing import List, TypeVar
import os as getenv


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines whether a given path requires authentication or not
        Args:
            path (str): Url path to be checked
            excluded_paths (List[str]): List of paths that don't need
            authentication
        Return:
            - True if path is not in excluded_paths, else False
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        if path[-1] != '/':
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path[-1] == '*':
                excluded_path = excluded_path[:-1]
            if excluded_path[-1] != '/':
                excluded_path += '/'

            if path.startswith(excluded_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header from a request object
        """
        if request is None or 'Authorization' not in request.headers:
            return None

        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns a User instance from information from a request object
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns a cookie value from a request
        """
        if request is None:
            return None

        session_name = getenv('SESSION_NAME', '_my_session_id')

        return request.cookies.get(session_name)
