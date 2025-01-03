#!/usr/bin/env python3
"""
Authentication module for the API
"""
from typing import List, TypeVar


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
            if excluded_path[-1] != '/':
                excluded_path += '/'

            if excluded_path[-2:] == '*/':
                excluded_path = excluded_path[:-2]
                if path.startswith(excluded_path):
                    return False
            else:
                if path == excluded_path:
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
