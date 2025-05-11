from sqlite3 import IntegrityError

from DB.database import db_session
from DB.models.user import User

import bcrypt

"""
Repository class for managing Order table in a database,
so CRUD operations
"""
class UserRepository:
    def __init__(self, session=None):
        if session is None:
            self.session = db_session
        else:
            self.session = session

    def create_user(self, name, surname, login, email, password):
        try:
            if self.session.query(User).filter_by(login=login).first():
                print(f'User with login {login} already exists')
                return None

            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            user = User(
                name=name,
                surname=surname,
                login=login,
                email=email,
                password=hashed_password.decode('utf-8')
            )

            self.session.add(user)
            self.session.commit()

            return user
        except Exception as e:
            print(f'Error: {e}')
            self.session.rollback()
            return None

    def update_user(self, user_id, name, surname, login, email, password):
        try:
            user = self.session.query(User).filter_by(id=user_id).first()
            if user is None:
                return None

            if name is not None and user.name != name:
                user.name = name

            if surname is not None and user.surname != surname:
                user.surname = surname

            if login is not None and user.login != login:
                login_exists = self.session.query(User).filter_by(login=login).first()
                if login_exists is None:
                    user.login = login
                else:
                    print(f'User with login {login} already exists')
                    return None

            if email is not None and user.email != email:
                email_exists = self.session.query(User).filter_by(email=email).first()
                if email_exists is None:
                    user.email = email
                else:
                    print(f'User with email {email} already exists')
                    return None

            if password is not None:
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
                user.password = hashed_password.decode('utf-8')

            self.session.commit()
            return user
        except Exception as e:
            print(f'Error: {e}')
            self.session.rollback()
            return False

    def get_user_by_id(self, user_id):
        user = self.session.query(User).filter_by(id=user_id).first()
        if user is None:
            return None
        return user

    def get_user_by_login(self, login):
        user = self.session.query(User).filter_by(login=login).first()
        if user is None:
            return None
        return user

    def get_user_by_email(self, email):
        user = self.session.query(User).filter_by(email=email).first()
        if user is None:
            return None
        return user

    def delete_user(self, user_id):
        try:
            user = self.session.query(User).filter_by(id=user_id).first()
            if user is None:
                return False

            self.session.delete(user)
            self.session.commit()
            return True
        except Exception as e:
            print(f'Error: {e}')
            return False

    @staticmethod
    def check_user_password(user, password):
        try:
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return True
            return False
        except Exception as e:
            print(f'Error: {e}')
            return False