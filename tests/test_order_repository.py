import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DB.models.product import Product
from DB.database import Base
import datetime
import bcrypt
from DB.repositories.category_repository import CategoryRepository
from DB.repositories.order_repository import OrderRepository
from DB.repositories.product_repository import ProductRepository
from DB.models.order import Order, order_products
from DB.models.user import User

from DB.repositories.user_repository import UserRepository


class TestOrderRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///test.db')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.product_repository = ProductRepository(session=self.session)
        self.user_repository = UserRepository(session=self.session)
        self.order_repository = OrderRepository(session=self.session)
        self.category_repository = CategoryRepository(session=self.session)

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def init_test_objects(self):
        self.category_repository.create_category('Top-clothing')
        self.category_repository.create_category('Bottom-clothing')

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


    def test_create_order(self):
        self.init_test_objects()

        order = self.order_repository.create_order(1, [1, 2, 3])
        self.assertIsNotNone(order)

        user = (self.session.query(User)
                .join(Order, Order.user_id == User.id)
                .filter(Order.id == order.id).first())

        product = (
            self.session.query(Product)
            .join(order_products, Product.id == order_products.c.product_id)
            .filter(Order.id == order_products.c.order_id)
            .first()
        )
        self.assertEqual(user.name, 'John')
        self.assertEqual(user.surname, 'Doe')
        self.assertEqual(user.login, 'johndoe')
        self.assertEqual(user.email, 'johndoe@gmail.com')
        self.assertTrue(bcrypt.checkpw('123Yo!'.encode('utf-8'), user.password.encode('utf-8')))

        self.assertEqual(product.name, 'T-shirt')
        self.assertEqual(product.category.name, 'top-clothing')
        self.assertEqual(product.price, 100.5)
        self.assertEqual(product.quantity, 5)
        self.assertEqual(product.exp_date, datetime.date(2026, 1, 1))
        self.assertEqual(product.img_link, self.product_repository.get_product_by_name(product.name).img_link)



    def test_delete_order(self):
        self.init_test_objects()
        order = self.order_repository.create_order(1, [1, 2, 3])
        self.assertIsNotNone(order)
        self.order_repository.delete_order(order.id)
        order = self.session.query(Order).filter_by(id=order.id).first()
        self.assertIsNone(order)

    def test_remove_product_from_order(self):
        self.init_test_objects()
        order = self.order_repository.create_order(1, [1, 2, 3])
        self.assertIsNotNone(order)

        product_to_remove = (
            self.session.query(Product)
            .join(order_products, Product.id == order_products.c.product_id)
            .filter(Order.id == order_products.c.order_id)
            .first()
        )

        self.order_repository.remove_product_from_order(order.id, product_to_remove.id)

        order = self.session.query(Order).filter_by(id=order.id).first()

        product_ids = [p.id for p in order.products]
        self.assertNotIn(product_to_remove.id, product_ids)

    def test_clear_order_products(self):
        self.init_test_objects()
        order = self.order_repository.create_order(1, [1, 2, 3])
        self.assertIsNotNone(order)
        self.order_repository.clear_order_products(order.id)
        products = (
            self.session.query(Product)
            .join(order_products, Product.id == order_products.c.product_id)
            .filter(Order.id == order_products.c.order_id)
            .all()
        )
        self.assertListEqual(products, [])

    def test_add_product_to_order(self):
        self.init_test_objects()
        order = self.order_repository.create_order(1, [1, 2, 3])
        self.assertIsNotNone(order)

        product = self.product_repository.create_product(name='Sneakers',
                                                         category_id= 1,
                                                         price=250.0,
                                                         quantity=8,
                                                         exp_date=datetime.date(2026, 12, 31))
        products = (
            self.session.query(Product)
            .join(order_products, Product.id == order_products.c.product_id)
            .filter(Order.id == order_products.c.order_id)
            .all()
        )
        self.assertListEqual(products, order.products)
        self.order_repository.add_product_to_order(order.id, product.id)
        products = (
            self.session.query(Product)
            .join(order_products, Product.id == order_products.c.product_id)
            .filter(Order.id == order_products.c.order_id)
            .all()
        )
        self.assertListEqual(products, order.products)

    def test_get_all_orders(self):
        self.init_test_objects()
        order1 = self.order_repository.create_order(1, [1, 2, 3])
        order2 = self.order_repository.create_order(2, [1, 2])
        self.assertIsNotNone(order1)
        self.assertIsNotNone(order2)

        orders = self.order_repository.get_all_orders()

        self.assertListEqual(orders, [order1, order2])

    def test_get_orders_by_user_id(self):
        self.init_test_objects()
        order1 = self.order_repository.create_order(1, [1, 2, 3])
        order2 = self.order_repository.create_order(1, [1, 2])
        order3 = self.order_repository.create_order(2, [1, 3])
        self.assertIsNotNone(order1)
        self.assertIsNotNone(order2)
        self.assertIsNotNone(order3)
        orders1 = self.order_repository.get_orders_by_user_id(1)
        self.assertListEqual(orders1, [order1, order2])
        orders2 = self.order_repository.get_orders_by_user_id(2)
        self.assertListEqual(orders2, [order3])

    def test_update_order(self):
        self.init_test_objects()
        order = self.order_repository.create_order(1, [1, 2, 3])
        self.assertIsNotNone(order)
        self.order_repository.update_order(order.id, new_user_id=2)
        user = (self.session.query(User)
                .join(Order, Order.user_id == User.id)
                .filter(Order.id == order.id).first())
        self.assertEqual(user.id, 2)
        self.order_repository.update_order(order.id, [1,2])
        products = (
            self.session.query(Product)
            .join(order_products, Product.id == order_products.c.product_id)
            .filter(Order.id == order_products.c.order_id)
            .all()
        )
        self.assertListEqual(products, order.products)


if __name__ == '__main__':
    unittest.main()
