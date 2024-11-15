#!/usr/bin/env python3
"""
Session Authentication Module
"""

from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """
    Session Authentication Class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id.

        Args:
            user_id (str): The user ID for which to create a session.

        Returns:
            str: The created Session ID or None if the input is invalid.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a User ID based on a Session ID.

        Args:
            session_id (str): The Session ID for which to retrieve the User ID.

        Returns:
            str: The User ID or None if the input is invalid.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Returns a User instance based on a cookie value.

        Args:
            request: The request object containing the session cookie.

        Returns:
            User: The User instance or None if no user is found.
        """
        if request is None:
            return None

        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return None

        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return None

        return User.get(user_id)
