import math
import random
from DB.database import db_session
from DB.repositories.category_repository import CategoryRepository
from DB.repositories.order_repository import OrderRepository
from DB.repositories.product_repository import ProductRepository


class PageService:
    def __init__(self, session=None):
        """
        Initialize the PageService with session and repositories.
        """
        self.session = session or db_session
        self.product_repository = ProductRepository(self.session)
        self.category_repository = CategoryRepository(self.session)
        self.order_repository = OrderRepository(self.session)

        # Load all product IDs initially
        total_products = self.product_repository.get_product_amount()
        self.product_ids = list(range(1, total_products + 1))

        # Pagination configuration
        self.product_per_page = 5
        self.total_pages = math.ceil(total_products / self.product_per_page)

        # Caching and state
        self.categories_list = []
        self.user_cart = []
        self.product_list = []
        self.page_products = {}

    def get_random_products(self, page):
        """
        Return a random list of products for the specified page.
        Ensures products are not repeated across pages.
        """
        # Return cached page if it exists
        if self.page_products.get(page) is not None:
            return self.page_products[page]

        products = []
        # Select random products until the page is filled or pool is empty
        while len(products) < self.product_per_page and self.product_ids:
            rand_id = random.choice(self.product_ids)
            product = self.product_repository.get_product_by_id(rand_id)
            if product:
                products.append(product)
                self.product_ids.remove(rand_id)

        # Cache the products for this page
        self.remember_page_products(page, products)
        return products

    def get_user_cart(self, user_id):
        """
        Retrieve products in the user's current cart (order).
        """
        order = self.order_repository.get_orders_by_user_id(user_id)
        if order and order.products:
            return order.products
        return []

    def get_products_from_cart_by_id(self, product_id):
        """
        Retrieve a product by its ID from the repository.
        """
        return self.product_repository.get_product_by_id(product_id)

    def get_categories(self):
        """
        Retrieve all available product categories.
        """
        return self.category_repository.get_all_categories()

    def remember_page_products(self, page_index, products):
        """
        Cache the list of products shown on a specific page.
        """
        self.page_products[page_index] = products
