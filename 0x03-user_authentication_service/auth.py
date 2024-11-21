#!/usr/bin/env python3
"""Auth module
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generates a new UUID.

    Returns:
        str: The generated UUID as a string.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize a new Auth instance
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            User: The newly created user object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password.decode())
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user login credentials.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            bool: True if the credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            hashed_password = user.hashed_password.encode()
            return bcrypt.checkpw(password.encode(), hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Creates a new session for a user.

        Args:
            email (str): The user's email address.

        Returns:
            str: The session ID, or None if the user is not found.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Retrieves a user from the database based on session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            User: The user object if found, None otherwise.
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys a user's session.

        Args:
            user_id (int): The ID of the user
            whose session should be destroyed.
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generates a reset password token for a user.

        Args:
            email (str): The user's email address.

        Returns:
            str: The reset password token.

        Raises:
            ValueError: If no user with the given email is found.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError(f"No user found with email: {email}")

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a user's password.

        Args:
            reset_token (str): The reset password token.
            password (str): The new password.

        Raises:
            ValueError: If the reset token is invalid or no user is found.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(
                user.id,
                hashed_password=hashed_password.decode(),
                reset_token=None
            )
        except NoResultFound:
            raise ValueError("Invalid reset token")
