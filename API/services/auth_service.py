from flask import session

from DB.repositories.user_repository import UserRepository

import re

class AuthService:
    def __init__(self, session):
        """
        Initialize AuthService with a database session.
        """
        self.user_repository = UserRepository(session)

    def register_user(self, name, surname, login, email, password):
        """
        Create a new user and store in the database.
        """
        return self.user_repository.create_user(name, surname, login, email, password)

    def login_user(self, email, password):
        """
        Validate user credentials and return user object if successful.
        """
        user = self.user_repository.get_user_by_email(email)
        if not user or not self.user_repository.check_user_password(user, password):
            return None
        return user

    @staticmethod
    def new_session(user):
        """
        Start a new session for the given user.
        """
        session['user_id'] = user.id
        session['email'] = user.email
        session['logged_in'] = True

    @staticmethod
    def end_session():
        """
        End the current user session.
        """
        session.pop('user_id', None)
        session.pop('email', None)
        session.pop('logged_in', None)

    @staticmethod
    def is_logged_in():
        """
        Check whether a user is currently logged in.
        """
        return session.get('logged_in', False)

    @staticmethod
    def password_check(password):
        """
        Verify the strength of the password.

        Criteria:
        - Minimum 8 characters
        - At least one digit
        - At least one lowercase letter
        - At least one uppercase letter
        - At least one symbol

        """
        length_ok = len(password) >= 8
        has_digit = re.search(r"\d", password) is not None
        has_upper = re.search(r"[A-Z]", password) is not None
        has_lower = re.search(r"[a-z]", password) is not None
        has_symbol = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~\"]", password) is not None

        return all([length_ok, has_digit, has_upper, has_lower, has_symbol])