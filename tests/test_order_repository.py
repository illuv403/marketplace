import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DB.models.product import Product
from DB.database import Base
import datetime
from DB.repositories.product_repository import ProductRepository
from DB.models.order import Order
from DB.models.user import User

class TestOrderRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///test.db')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.repository = ProductRepository(session=self.session)

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

if __name__ == '__main__':
    unittest.main()
