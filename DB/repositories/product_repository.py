from flask import session
from sqlalchemy.sql.functions import concat

from DB.models.category import Category
from DB.models.product import Product
from DB.database import db_session


class ProductRepository:
    """Repository class for managing Product table in a database.

    Handles CRUD (Create, Read, Update, Delete) operations for the Product model.
    """

    def __init__(self, session=None):
        """Initialize with optional custom database session."""
        self.session = session or db_session

    def create_product(self, name, category_id, price, quantity, exp_date):
        """Create a new product with specified attributes."""
        try:
            if self.session.query(Product).filter(Product.name == name).first() is not None:
                print(f"Product with name {name} already exists.")
                return None
            img_link = "".join(["img/products/", name.lower() , ".png"])
            product = Product(name=name, category_id=category_id, price=price, quantity=quantity, exp_date=exp_date,
                              img_link = img_link)
            self.session.add(product)
            self.session.commit()
            return product
        except Exception as e:
            return None

    def update_product(self, id, name, category_id, price, quantity, exp_date):
        """Update an existing product with new attributes."""
        try:
            product = self.session.query(Product).filter_by(id=id).first()
            if not product:
                print(f"No product found with id={id}")
                return None

            if name is not None:
                product.name = name
            if category_id is not None:
                product.category_id = category_id
            if price is not None:
                product.price = price
            if quantity is not None:
                product.quantity = quantity
            if exp_date is not None:
                product.exp_date = exp_date

            self.session.flush()
            self.session.commit()
            return product
        except Exception as e:
            self.session.rollback()
            return None

    def get_all_products(self):
        """Retrieve all products from the database."""
        try:
            product_list = []
            for product in self.session.query(Product).all():
                product_list.append(product)
            return product_list
        except Exception as e:
            return None

    def get_product_by_id(self, id):
        """Retrieve a product by its ID."""
        try:
            product = self.session.query(Product).filter_by(id=id).first()
            if not product:
                print(f"No such product with id={id}")
                return None
            return product
        except Exception as e:
            return None

    def get_product_by_name(self, name):
        """Retrieve a product by its name."""
        try:
            product = self.session.query(Product).filter_by(name=name).first()
            if not product:
                print(f"No such product with name={name}")
                return None
            return product
        except Exception as e:
            return None

    def get_product_by_quantity(self, quantity):
        """Retrieve products by their quantity."""
        try:
            product_by_quantity = self.session.query(Product).filter_by(quantity=quantity).all()
            if len(product_by_quantity) == 0:
                print(f"No such products with quantity={quantity}")
                return None
            return product_by_quantity
        except Exception as e:
            return None

    def get_product_by_price(self, price):
        """Retrieve products by their price."""
        try:
            products_by_price = self.session.query(Product).filter_by(price=price).all()
            if len(products_by_price) == 0:
                print(f"No such products with price={price}")
                return None
            return products_by_price
        except Exception as e:
            return None

    def get_product_by_category(self, category_name):
        """Retrieve products by their category name."""
        try:
            products_by_cat = (
                self.session.query(Product).join(Category, Product.category_id == Category.id)
                .filter(Category.name.ilike(f'%{category_name}%')).all()
            )
            if not products_by_cat:
                print(f"No such products with category={category_name}")
                return None
            return products_by_cat
        except Exception as e:
            print(f"Error: {e}")
            return None

    def delete_product(self, id):
        """Delete a product by its ID."""
        try:
            product = self.session.query(Product).filter(Product.id == id).first()
            if not product:
                print("No such product")
                return False
            self.session.delete(product)
            self.session.commit()
            return True
        except Exception as e:
            return False

    def get_product_amount(self):
        """Retrieve the total count of products in the database."""
        try:
            product_amount = self.session.query(Product).count()
            return product_amount
        except Exception as e:
            print("Impossible to get amount of products")
            return None