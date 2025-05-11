import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DB.models.product import Product
from DB.database import Base
import datetime
from DB.repositories.product_repository import ProductRepository
from DB.models.order import Order
from DB.models.user import User


class TestProductRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.repository = ProductRepository(session=self.session)

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_create_product(self):
        self.repository.create(name='T-shirt',
                               category='top-clothing',
                               price=100.5,
                               quantity=5,
                               exp_date=datetime.date(2026, 1, 1),
                               img_link='img\\5f0b501f875a062fa52691072aa2e844.jpg')

        product_from_db = self.session.query(Product).filter_by(name='T-shirt').first()
        self.assertIsNotNone(product_from_db)
        self.assertEqual(product_from_db.name, 'T-shirt')
        self.assertEqual(product_from_db.category, 'top-clothing')
        self.assertEqual(product_from_db.price, 100.5)
        self.assertEqual(product_from_db.quantity, 5)
        self.assertEqual(product_from_db.exp_date, datetime.date(2026, 1, 1))
        self.assertEqual(product_from_db.img_link, 'img\\5f0b501f875a062fa52691072aa2e844.jpg')

    def test_delete_product(self):
        self.repository.create(name='T-shirt',
                               category='top-clothing',
                               price=100.5,
                               quantity=5,
                               exp_date=datetime.date(2026, 1, 1),
                               img_link='img\\5f0b501f875a062fa52691072aa2e844.jpg')
        self.repository.delete(1)
        product_from_db = self.session.query(Product).filter_by(name='T-shirt').first()
        self.assertIsNone(product_from_db)

    def test_update_product(self):
        self.repository.create(name='T-shirt',
                               category='top-clothing',
                               price=100.5,
                               quantity=5,
                               exp_date=datetime.date(2026, 1, 1),
                               img_link='img\\5f0b501f875a062fa52691072aa2e844.jpg')

        self.repository.update(1, name='T-shirt',
                               category='top-clothing',
                               price=120.5,
                               quantity=7,
                               exp_date=datetime.date(2026, 1, 1),
                               img_link='img\\5f0b501f875a062fa52691072aa2e844.jpg')

        product_from_db = self.session.query(Product).filter_by(name='T-shirt').first()
        self.assertEqual(product_from_db.price, 120.5)
        self.assertEqual(product_from_db.quantity, 7)


    def test_get_all(self):
        self.repository.create(name='T-shirt',
                               category='top-clothing',
                               price=100.5,
                               quantity=5,
                               exp_date=datetime.date(2026, 1, 1),
                               img_link='img\\5f0b501f875a062fa52691072aa2e844.jpg')
        self.repository.create(name='Jeans',
                               category='bottom-clothing',
                               price=150.0,
                               quantity=8,
                               exp_date=datetime.date(2026, 7, 15),
                               img_link='img\\5f0b501f875a062fa52691072aa2e844.jpg')
        self.repository.create(name='Jacket',
                               category='outerwear',
                               price=200.0,
                               quantity=6,
                               exp_date=datetime.date(2027, 1, 1),
                               img_link='img\\5f0b501f875a062fa52691072aa2e844.jpg')
        products_list = self.repository.get_all()
        self.assertIsNotNone(products_list)


    def test_get_by_id(self):
        self.repository.create(name='T-shirt',
                               category='top-clothing',
                               price=100.5,
                               quantity=5,
                               exp_date=datetime.date(2026, 1, 1),
                               img_link='img\\5f0b501f875a062fa52691072aa2e844.jpg')
        self.repository.create(name='Jeans',
                               category='bottom-clothing',
                               price=150.0,
                               quantity=8,
                               exp_date=datetime.date(2026, 7, 15),
                               img_link='img\\5f0b501f875a062fa52691072aa2e844.jpg')

        self.repository.create(name='Jacket',
                               category='outerwear',
                               price=200.0,
                               quantity=6,
                               exp_date=datetime.date(2027, 1, 1),
                               img_link='img\\5f0b501f875a062fa52691072aa2e844.jpg')
        product2 = self.repository.get_by_id(2)
        self.assertEqual(product2.name, 'Jeans')
        product1 = self.repository.get_by_id(1)
        self.assertEqual(product1.name, 'T-shirt')
        product3 = self.repository.get_by_id(3)
        self.assertEqual(product3.name, 'Jacket')

    def test_get_by_name(self):
        self.repository.create(name='T-shirt',
                               category='top-clothing',
                               price=100.5,
                               quantity=5,
                               exp_date=datetime.date(2026, 1, 1),
                               img_link='img\\5f0b501f875a062fa52691072aa2e844.jpg')
        self.repository.create(name='Jeans',
                               category='bottom-clothing',
                               price=150.0,
                               quantity=8,
                               exp_date=datetime.date(2026, 7, 15),
                               img_link='img\\5f0b501f875a062fa52691072aa2e844.jpg')
        product2 = self.repository.get_by_name('T-shirt')
        self.assertEqual(product2.name, 'T-shirt')
        product1 = self.repository.get_by_name('Jeans')
        self.assertEqual(product1.name, 'Jeans')

    def test_get_by_quantity(self):
        self.repository.create(name='T-shirt',
                               category='top-clothing',
                               price=100.5,
                               quantity=5,
                               exp_date=datetime.date(2026, 1, 1),
                               img_link='img\\5f0b501f875a062fa52691072aa2e844.jpg')
        self.repository.create(name='Hoodie',
                               category='top-clothing',
                               price=120.0,
                               quantity=5,
                               exp_date=datetime.date(2026, 5, 1),
                               img_link='img\\hoodie1.jpg')
        self.repository.create(name='Jeans',
                               category='bottom-clothing',
                               price=150.0,
                               quantity=8,
                               exp_date=datetime.date(2026, 7, 15),
                               img_link='img\\5f0b501f875a062fa52691072aa2e844.jpg')
        products = self.repository.get_by_quantity(5)
        self.assertIsNotNone(products)
        for product in products:
            self.assertEqual(product.quantity, 5)
        products1 = self.repository.get_by_quantity(8)
        self.assertIsNotNone(products1)
        for product in products1:
            self.assertEqual(product.quantity, 8)

    def test_get_by_price(self):
        self.repository.create(name='T-shirt',
                               category='top-clothing',
                               price=100.5,
                               quantity=5,
                               exp_date=datetime.date(2026, 1, 1),
                               img_link='img\\5f0b501f875a062fa52691072aa2e844.jpg')
        self.repository.create(name='Sweater',
                               category='top-clothing',
                               price=100.5,
                               quantity=9,
                               exp_date=datetime.date(2026, 9, 10),
                               img_link='img\\sweater1.jpg')
        self.repository.create(name='Jeans',
                               category='bottom-clothing',
                               price=150.0,
                               quantity=8,
                               exp_date=datetime.date(2026, 7, 15),
                               img_link='img\\5f0b501f875a062fa52691072aa2e844.jpg')
        products = self.repository.get_by_price(100.5)
        self.assertIsNotNone(products)
        for product in products:
            self.assertEqual(product.price, 100.5)
        products1 = self.repository.get_by_price(150)
        self.assertIsNotNone(products1)
        for product in products1:
            self.assertEqual(product.price, 150)

    def test_get_by_category(self):
        self.repository.create(name='T-shirt',
                               category='top-clothing',
                               price=100.5,
                               quantity=5,
                               exp_date=datetime.date(2026, 1, 1),
                               img_link='img\\5f0b501f875a062fa52691072aa2e844.jpg')
        self.repository.create(name='Sweater',
                               category='top-clothing',
                               price=100.5,
                               quantity=9,
                               exp_date=datetime.date(2026, 9, 10),
                               img_link='img\\sweater1.jpg')
        self.repository.create(name='Jeans',
                               category='bottom-clothing',
                               price=150.0,
                               quantity=8,
                               exp_date=datetime.date(2026, 7, 15),
                               img_link='img\\5f0b501f875a062fa52691072aa2e844.jpg')
        products = self.repository.get_by_category('Top-clothing')
        self.assertIsNotNone(products)
        for product in products:
            self.assertEqual(product.category, 'top-clothing')
        products1 = self.repository.get_by_category('botTOm-clothing')
        self.assertIsNotNone(products1)
        for product in products1:
            self.assertEqual(product.category, 'bottom-clothing')


if __name__ == '__main__':
    unittest.main()
