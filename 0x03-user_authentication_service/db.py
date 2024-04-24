#!/usr/bin/env python3
"""This file contains the DB class"""
from typing import Dict, List

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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
        """The Add User method"""
        newUser = User(email=email, hashed_password=hashed_password)
        self._session.add(newUser)
        self._session.commit()
        return newUser

    def find_user_by(self, **kw) -> User:
        """The find user by method"""
        try:
            user = self._session.query(User).filter_by(**kw).first()
            if user is None:
                raise NoResultFound
            return user
        except AttributeError:
            raise InvalidRequestError

    def update_user(self, user_id: int, **kw) -> None:
        """The update_user method"""
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError

        for k, v in kw.items():
            if hasattr(user, k):
                setattr(user, k, v)
            else:
                raise ValueError
        self._session.commit()
        return None
