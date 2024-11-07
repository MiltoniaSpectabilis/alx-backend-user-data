#!/usr/bin/env python3
"""Module for password encryption and validation."""
import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a salted, hashed password."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if the provided password matches the hashed password."""
    return bcrypt.checkpw(password.encode(), hashed_password)
