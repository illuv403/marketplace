import math
import random
from itertools import product

from flask import request
from unicodedata import category

from DB.database import db_session
from DB.repositories.category_repository import CategoryRepository
from DB.repositories.product_repository import ProductRepository


class PageService:
    def __init__(self, session):
        self.session = session or db_session
        self.cur_user_id = self.session.get('user_id')
        self.product_repository = ProductRepository(self.session)
        self.category_repository = CategoryRepository(self.session)
        self.product_ids = list(range(1, self.product_repository.get_product_amount()))
        self.total_pages = math.ceil(self.product_repository.get_product_amount() / 5)

        self.categories_list = []
        self.user_cart = []
        self.product_list = []
        self.page_products = {}

    def get_random_products(self, page):
        products = []
        if self.page_products.get(page) is not None:
            return self.page_products.get(page)
        while len(products) < 5 and len(self.product_ids) > 0:
            rand_id = random.choice(self.product_ids)
            products.append(self.product_repository.get_product_by_id(rand_id))
            self.product_ids.pop(self.product_ids.index(rand_id))
            self.remember_page_products(page, products)
        return products

    def get_user_cart(self):
        pass

    def get_categories(self):
        return self.category_repository.get_all_categories()


    def search(self):
        pass

    def remember_page_products(self, page_index, products):
        self.page_products[page_index] = products