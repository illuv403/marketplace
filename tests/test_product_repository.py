import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DB.models.user import User
from DB.models.order import Order, order_products
from DB.models.product import Product
from DB.models.category import Category
from DB.database import Base
import datetime
from DB.repositories.product_repository import ProductRepository

class TestProductRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///test.db')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.repository = ProductRepository(session=self.session)
        category1 = Category(name='Top-clothing')
        category2 = Category(name='Bottom-clothing')
        category3 = Category(name='Outerwear')
        self.session.add_all([category1, category2, category3])
        self.session.commit()
        self.category1 = category1
        self.category2 = category2
        self.category3 = category3

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_create_product(self):
        self.repository.create_product(
            name='T-shirt',
            category_id=self.category1.id,
            price=100.5,
            quantity=5,
            exp_date=datetime.date(2026, 1, 1)
        )
        product_from_db = self.session.query(Product).filter_by(name='T-shirt').first()
        self.assertIsNotNone(product_from_db)
        self.assertEqual(product_from_db.name, 'T-shirt')
        self.assertEqual(product_from_db.price, 100.5)
        self.assertEqual(product_from_db.quantity, 5)
        self.assertEqual(product_from_db.exp_date, datetime.date(2026, 1, 1))
        self.assertEqual(product_from_db.img_link, self.repository.get_product_by_name(product_from_db.name).img_link)

    def test_delete_product(self):
        self.repository.create_product(
            name='T-shirt',
            category_id=self.category1.id,
            price=100.5,
            quantity=5,
            exp_date=datetime.date(2026, 1, 1)
        )
        self.repository.delete_product(1)
        product_from_db = self.session.query(Product).filter_by(name='T-shirt').first()
        self.assertIsNone(product_from_db)

    def test_update_product(self):
        self.repository.create_product(
            name='T-shirt',
            category_id=self.category1.id,
            price=100.5,
            quantity=5,
            exp_date=datetime.date(2026, 1, 1)
        )
        self.repository.update_product(
            id=1,
            name='T-shirt',
            category_id=self.category2.id,
            price=120.5,
            quantity=7,
            exp_date=datetime.date(2026, 1, 1)
        )
        product_from_db = self.session.query(Product).filter_by(name='T-shirt').first()
        self.assertEqual(product_from_db.price, 120.5)
        self.assertEqual(product_from_db.quantity, 7)
        self.assertEqual(product_from_db.category_id, self.category2.id)

    def test_get_all(self):
        self.repository.create_product(
            name='T-shirt',
            category_id=self.category1.id,
            price=100.5,
            quantity=5,
            exp_date=datetime.date(2026, 1, 1)
        )
        self.repository.create_product(
            name='Jeans',
            category_id=self.category2.id,
            price=150.0,
            quantity=8,
            exp_date=datetime.date(2026, 7, 15)
        )
        self.repository.create_product(
            name='Jacket',
            category_id=self.category3.id,
            price=200.0,
            quantity=6,
            exp_date=datetime.date(2027, 1, 1)
        )
        products_list = self.repository.get_all_products()
        self.assertIsNotNone(products_list)
        self.assertEqual(len(products_list), 3)

    def test_get_by_id(self):
        self.repository.create_product(
            name='T-shirt',
            category_id=self.category1.id,
            price=100.5,
            quantity=5,
            exp_date=datetime.date(2026, 1, 1)
        )
        self.repository.create_product(
            name='Jeans',
            category_id=self.category2.id,
            price=150.0,
            quantity=8,
            exp_date=datetime.date(2026, 7, 15)
        )
        self.repository.create_product(
            name='Jacket',
            category_id=self.category3.id,
            price=200.0,
            quantity=6,
            exp_date=datetime.date(2027, 1, 1)
        )
        product2 = self.repository.get_product_by_id(2)
        self.assertEqual(product2.name, 'Jeans')
        product1 = self.repository.get_product_by_id(1)
        self.assertEqual(product1.name, 'T-shirt')
        product3 = self.repository.get_product_by_id(3)
        self.assertEqual(product3.name, 'Jacket')

    def test_get_by_name(self):
        self.repository.create_product(
            name='T-shirt',
            category_id=self.category1.id,
            price=100.5,
            quantity=5,
            exp_date=datetime.date(2026, 1, 1)
        )
        self.repository.create_product(
            name='Jeans',
            category_id=self.category2.id,
            price=150.0,
            quantity=8,
            exp_date=datetime.date(2026, 7, 15)
        )
        product2 = self.repository.get_product_by_name('T-shirt')
        self.assertEqual(product2.name, 'T-shirt')
        product1 = self.repository.get_product_by_name('Jeans')
        self.assertEqual(product1.name, 'Jeans')

    def test_get_by_quantity(self):
        self.repository.create_product(
            name='T-shirt',
            category_id=self.category1.id,
            price=100.5,
            quantity=5,
            exp_date=datetime.date(2026, 1, 1)
        )
        self.repository.create_product(
            name='Hoodie',
            category_id=self.category2.id,
            price=120.0,
            quantity=5,
            exp_date=datetime.date(2026, 5, 1)
        )
        self.repository.create_product(
            name='Jeans',
            category_id=self.category3.id,
            price=150.0,
            quantity=8,
            exp_date=datetime.date(2026, 7, 15)
        )
        products = self.repository.get_product_by_quantity(5)
        self.assertIsNotNone(products)
        self.assertEqual(len(products), 2)
        for product in products:
            self.assertEqual(product.quantity, 5)
        products1 = self.repository.get_product_by_quantity(8)
        self.assertIsNotNone(products1)
        self.assertEqual(len(products1), 1)
        for product in products1:
            self.assertEqual(product.quantity, 8)

    def test_get_by_price(self):
        self.repository.create_product(
            name='T-shirt',
            category_id=self.category1.id,
            price=100.5,
            quantity=5,
            exp_date=datetime.date(2026, 1, 1)
        )
        self.repository.create_product(
            name='Sweater',
            category_id=self.category2.id,
            price=100.5,
            quantity=9,
            exp_date=datetime.date(2026, 9, 10)
        )
        self.repository.create_product(
            name='Jeans',
            category_id=self.category3.id,
            price=150.0,
            quantity=8,
            exp_date=datetime.date(2026, 7, 15)
        )
        products = self.repository.get_product_by_price(100.5)
        self.assertIsNotNone(products)
        self.assertEqual(len(products), 2)
        for product in products:
            self.assertEqual(product.price, 100.5)
        products1 = self.repository.get_product_by_price(150.0)
        self.assertIsNotNone(products1)
        self.assertEqual(len(products1), 1)
        for product in products1:
            self.assertEqual(product.price, 150.0)

    def test_get_by_category(self):
        self.repository.create_product(
            name='T-shirt',
            category_id=self.category1.id,
            price=100.5,
            quantity=5,
            exp_date=datetime.date(2026, 1, 1)
        )
        self.repository.create_product(
            name='Sweater',
            category_id=self.category1.id,
            price=100.5,
            quantity=9,
            exp_date=datetime.date(2026, 9, 10)
        )
        self.repository.create_product(
            name='Jeans',
            category_id=self.category2.id,
            price=150.0,
            quantity=8,
            exp_date=datetime.date(2026, 7, 15)
        )
        products = self.repository.get_product_by_category('Top-clothing')
        self.assertIsNotNone(products)
        self.assertEqual(len(products), 2)
        for product in products:
            self.assertEqual(product.category.name.lower(), 'top-clothing')
        products1 = self.repository.get_product_by_category('Bottom-clothing')
        self.assertIsNotNone(products1)
        self.assertEqual(len(products1), 1)
        for product in products1:
            self.assertEqual(product.category.name.lower(), 'bottom-clothing')

if __name__ == '__main__':
    unittest.main()