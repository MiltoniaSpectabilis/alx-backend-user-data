#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database.

        Args:
            email (str): The user's email address.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The newly created user object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Finds a user in the database based on given criteria.

        Args:
            **kwargs: Keyword arguments representing the search criteria.

        Returns:
            User: The user object if found.

        Raises:
            NoResultFound: If no user is found matching the criteria.
            InvalidRequestError: If the query arguments are invalid.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound
        except InvalidRequestError:
            raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates a user's attributes in the database.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Keyword arguments representing the attributes to update.

        Raises:
            ValueError: If an invalid attribute is passed for update.
            NoResultFound: If no user is found with the given ID.
        """
        user = self.find_user_by(id=user_id)
        if not user:
            raise NoResultFound

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError(f"Invalid attribute for User model: {key}")

        self._session.commit()

    def close_session(self):
        """
        closes the session
        """
        self.__session.close()
