import random

from DB.database import db_session
from DB.repositories.product_repository import ProductRepository
from API.app import create_app


class PageService:
    def __init__(self, session):
        self.session = session or db_session
        self.product_repository = ProductRepository(self.session)
        self.categories_list = []
        self.user_cart = []
        self.product_list = []

    def get_random_products(self):
        product_amount = self.product_repository.get_product_amount()
        product_id_list = []
        while len(product_id_list) != 10 or len(product_id_list) != product_amount:
            rand_product_id = random.randint(1 , product_amount)
            if rand_product_id not in product_id_list:
                product_id_list.append(rand_product_id)

        products = [self.product_repository.get_product_by_id(prod_id) for prod_id in product_id_list]
        return products

    def get_user_cart(self):
        pass

    def get_categories(self):
        pass

    def search(self):
        pass