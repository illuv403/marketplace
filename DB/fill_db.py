from DB.database import db_session
from DB.repositories.category_repository import CategoryRepository
from DB.repositories.order_repository import OrderRepository
from DB.repositories.product_repository import ProductRepository
import datetime

from DB.repositories.user_repository import UserRepository


class FillProducts:
    def __init__(self, session=None):
        self.session = session or db_session
        self.product_repository = ProductRepository(self.session)
        self.user_repository = UserRepository(self.session)
        self.order_repository = OrderRepository(self.session)
        self.category_repository = CategoryRepository(self.session)

    def fill_categories(self):
        self.category_repository.create_category('top_clothing')
        self.category_repository.create_category('bottom_clothing')
        self.category_repository.create_category('shoes')

    def fill_products(self):
        self.product_repository.create_product(name='T-shirt',
                          category_id=1,
                          price=100.5,
                          quantity=5,
                          exp_date=datetime.date(2026, 1, 1))

        self.product_repository.create_product(name='Jeans',
                          category_id=2,
                          price=150.0,
                          quantity=10,
                          exp_date=datetime.date(2026, 6, 1))

        self.product_repository.create_product(name='Hoodie',
                          category_id=1,
                          price=200.0,
                          quantity=7,
                          exp_date=datetime.date(2026, 3, 15))

        self.product_repository.create_product(name='Jacket',
                          category_id=1,
                          price=300.0,
                          quantity=3,
                          exp_date=datetime.date(2027, 1, 1))

        self.product_repository.create_product(name='Sneakers',
                          category_id=3,
                          price=250.0,
                          quantity=8,
                          exp_date=datetime.date(2026, 12, 31))

        self.product_repository.create_product(name='Socks',
                          category_id=2,
                          price=20.0,
                          quantity=50,
                          exp_date=datetime.date(2026, 5, 5))

        self.product_repository.create_product(name='Dress',
                          category_id=1,
                          price=180.0,
                          quantity=6,
                          exp_date=datetime.date(2026, 8, 20))


    def fill_users(self):
        self.user_repository.create_user(
            name='John',
            surname='Doe',
            login='johndoe',
            email='johndoe@gmail.com',
            password='123Yo!'
        )

        self.user_repository.create_user(
            name='Johnny',
            surname='Doet',
            login='johndoet',
            email='johndoet@gmail.com',
            password='1234Yo!'
        )

    def fill_orders(self):
        self.order_repository.create_order(1, [1,4,5])
        self.order_repository.create_order(2, [3,6,8])
        self.order_repository.create_order(3, [4,7,2])

    def fill_all(self):
        self.fill_categories()
        self.fill_products()
        self.fill_users()
        self.fill_orders()