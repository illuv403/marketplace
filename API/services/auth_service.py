from functools import wraps

from flask import session, redirect

from DB.repositories.user_repository import UserRepository

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