from functools import wraps

from flask import session, redirect

from DB.repositories.user_repository import UserRepository

import re

class AuthService:
    def __init__(self, session):
        self.user_repository = UserRepository(session)

    def register_user(self, name, surname, login, email, password):
        user = self.user_repository.create_user(name, surname, login, email, password)
        return user

    def login_user(self, email, password):
        user = self.user_repository.get_user_by_email(email)

        if user is None:
            return None

        if not self.user_repository.check_user_password(user, password):
            return None

        return user

    @staticmethod
    def new_session(user):
        session['user_id'] = user.id
        session['email'] = user.email
        session['logged_in'] = True

    @staticmethod
    def end_session():
        session.pop('user_id', None)
        session.pop('email', None)
        session.pop('logged_in', None)

    @staticmethod
    def is_logged_in():
        return 'logged_in' in session and session['logged_in']

    @staticmethod
    def password_check(password):
        """
        Verify the strength of 'password'
        Returns a dict indicating the wrong criteria
        A password is considered strong if:
            8 characters length or more
            1 digit or more
            1 symbol or more
            1 uppercase letter or more
            1 lowercase letter or more
        """


        length_error = len(password) < 8

        digit_error = re.search(r"\d", password) is None

        uppercase_error = re.search(r"[A-Z]", password) is None

        lowercase_error = re.search(r"[a-z]", password) is None

        symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password) is None

        password_ok = not (length_error or digit_error or uppercase_error or lowercase_error or symbol_error)

        return password_ok