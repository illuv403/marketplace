import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DB.database import Base
from DB.models.user import User
from DB.models.order import Order, order_products
from DB.models.product import Product
from DB.repositories.user_repository import UserRepository
import bcrypt

class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///test')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.repo = UserRepository(session=self.session)

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_create_user(self):
        self.repo.create_user(
            name='John',
            surname='Doe',
            login='johndoe',
            email='johndoe@gmail.com',
            password='123Yo!'
        )

        user_from_db = self.session.query(User).filter_by(login='johndoe').first()
        self.assertIsNotNone(user_from_db)
        self.assertEqual(user_from_db.name, 'John')
        self.assertEqual(user_from_db.surname, 'Doe')
        self.assertEqual(user_from_db.login, 'johndoe')
        self.assertEqual(user_from_db.email, 'johndoe@gmail.com')
        self.assertTrue(bcrypt.checkpw('123Yo!'.encode('utf-8'), user_from_db.password.encode('utf-8')))

    def test_update_user(self):
        self.repo.create_user(
            name='John',
            surname='Doe',
            login='johndoe',
            email='johndoe@gmail.com',
            password='123Yo!'
        )

        self.repo.update_user(
            user_id=1,
            name='Johnny',
            surname='Doe',
            login='johndoe',
            email='johndoe@gmail.com',
            password='123Yo!'
        )

        user_from_db = self.session.query(User).filter_by(login='johndoe').first()
        self.assertEqual(user_from_db.name, 'Johnny')

    def test_get_user_by_id(self):
        self.repo.create_user(
            name='John',
            surname='Doe',
            login='johndoe',
            email='johndoe@gmail.com',
            password='123Yo!'
        )

        user_from_db = self.repo.get_user_by_id(1)
        self.assertIsNotNone(user_from_db)
        self.assertEqual(user_from_db.name, 'John')

    def test_get_user_by_login(self):
        self.repo.create_user(
            name='John',
            surname='Doe',
            login='johndoe',
            email='johndoe@gmail.com',
            password='123Yo!'
        )

        user_from_db = self.repo.get_user_by_login('johndoe')
        self.assertIsNotNone(user_from_db)
        self.assertEqual(user_from_db.name, 'John')

    def test_get_user_by_email(self):
        self.repo.create_user(
            name='John',
            surname='Doe',
            login='johndoe',
            email='johndoe@gmail.com',
            password='123Yo!'
        )

        user_from_db = self.repo.get_user_by_email('johndoe@gmail.com')
        self.assertIsNotNone(user_from_db)
        self.assertEqual(user_from_db.name, 'John')

    def test_delete_user(self):
        self.repo.create_user(
            name='John',
            surname='Doe',
            login='johndoe',
            email='johndoe@gmail.com',
            password='123Yo!'
        )

        user_deleted = self.repo.delete_user(1)
        user_from_db = self.session.query(User).filter_by(login='johndoe').first()
        self.assertTrue(user_deleted)
        self.assertIsNone(user_from_db)

    def test_check_user_password(self):
        self.repo.create_user(
            name='John',
            surname='Doe',
            login='johndoe',
            email='johndoe@gmail.com',
            password='123Yo!'
        )

        user = self.session.query(User).filter_by(login='johndoe').first()
        self.assertTrue(self.repo.check_user_password(user, '123Yo!'))
        self.assertFalse(self.repo.check_user_password(user, '123Yo2!'))

if __name__ == '__main__':
    unittest.main()
