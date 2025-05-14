import random
from itertools import product

from DB.database import db_session
from DB.repositories.product_repository import ProductRepository



class PageService:
    def __init__(self, session):
        self.session = session or db_session
        self.product_repository = ProductRepository(self.session)
        self.product_ids = list(range(1, self.product_repository.get_product_amount()))

        self.categories_list = []
        self.user_cart = []
        self.product_list = []
        self.page_products = {}

    def get_random_products(self):
        products = []
        while len(products) != 5:
            rand_id = random.choice(self.product_ids)
            products.append(self.product_repository.get_product_by_id(rand_id))
            self.product_ids.pop(self.product_ids.index(rand_id))
        return products

    def get_user_cart(self):
        pass

    def get_categories(self):
        pass

    def search(self):
        pass