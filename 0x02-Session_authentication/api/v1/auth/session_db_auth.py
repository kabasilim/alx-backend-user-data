#!/usr/bin/env python3
"""
Define class SessionDButh
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    Definition of SessionDBAuth class that persists session data
    in a database
    """

    def create_session(self, user_id=None):
        """
        Create a Session ID for a user_id
        Args:
           user_id (str): user id
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        kw = {
            "user_id": user_id,
            "session_id": session_id
        }
        user = UserSession(**kw)
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns a user ID based on a session ID
        Args:
            session_id (str): session ID
        Return:
            user id or None if session_id is None or not a string
        """
        user_session = UserSession().search({"session_id": session_id})
        if len(user_session) > 0:
            created_at = user_session[0].created_at
            duration = created_at + timedelta(seconds=self.session_duration)

            if duration < datetime.now():
                return None
            return user_session[0].to_json().get('user_id')
        return None

    def destroy_session(self, request=None):
        """
        Destroy a UserSession instance based on a
        Session ID from a request cookie
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_session = UserSession().search({"session_id": session_id})
        if len(user_session) > 0:
            user_session[0].remove()
            return True
        return False
