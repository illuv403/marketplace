import math
import random
from itertools import product

from flask import request
from unicodedata import category

from DB.database import db_session
from DB.repositories.category_repository import CategoryRepository
from DB.repositories.order_repository import OrderRepository
from DB.repositories.product_repository import ProductRepository


class PageService:
    def __init__(self, session):
        self.session = session or db_session
        self.product_repository = ProductRepository(self.session)
        self.category_repository = CategoryRepository(self.session)
        self.order_repository = OrderRepository(self.session)
        self.product_ids = list(range(1, self.product_repository.get_product_amount()+1))
        self.product_per_page = 5
        self.total_pages = math.ceil(self.product_repository.get_product_amount() / self.product_per_page)

        self.categories_list = []
        self.user_cart = []
        self.product_list = []
        self.page_products = {}

    def get_random_products(self, page):
        products = []
        if self.page_products.get(page) is not None:
            return self.page_products.get(page)
        while len(products) < self.product_per_page and len(self.product_ids) > 0:
            rand_id = random.choice(self.product_ids)
            products.append(self.product_repository.get_product_by_id(rand_id))
            self.product_ids.pop(self.product_ids.index(rand_id))
            self.remember_page_products(page, products)
        return products

    def get_user_cart(self, user_id):
        order = self.order_repository.get_orders_by_user_id(user_id)
        if order and len(order.products) > 0:
            return order.products
        return []

    def get_products_from_cart_by_id(self , product_id):
        product = self.product_repository.get_product_by_id(product_id)
        if product:
            return product

    def add_product_to_cart(self, user_id, product_id):
        self.order_repository.add_product_to_order(user_id, product_id)

    def remove_product_from_cart(self, user_id, product_id):
        user_order = self.order_repository.get_orders_by_user_id(user_id)
        if user_order:
            self.order_repository.remove_product_from_order(user_order.id, product_id)

    def get_categories(self):
        return self.category_repository.get_all_categories()

    def search(self, query):
        pass

    def remember_page_products(self, page_index, products):
        self.page_products[page_index] = products