from flask import session
from sqlalchemy.sql.functions import concat

from DB.models.product import Product
from DB.database import db_session

"""
Repository class for managing Product table in a database,
so CRUD operations
"""
class ProductRepository:

    def __init__(self, session=None):
        self.session = session or db_session

    def delete(self, id):
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

    def update(self, id, name, category, price, quantity, exp_date):
        try:
            product = self.session.query(Product).filter_by(id=id).first()
            if not product:
                print(f"No such product: {name}")
                return None

            if name is not None and product.name != name:
                product.name = name
            if category is not None and product.category != category:
                product.category = category
            if price is not None and product.price != price:
                product.price = price
            if quantity is not None and product.quantity != quantity:
                product.quantity = quantity
            if product.exp_date != exp_date:
                product.exp_date = exp_date

            self.session.commit()
            return product
        except Exception as e:
            return None

    def create(self, name, category, price, quantity, exp_date):
        try:

            if self.session.query(Product).filter(Product.name == name).first() is not None:
                print(f"Product with name {name} already exists.")
                return None
            img_link = "".join(["img/", name.lower() , ".png"])
            product = Product(name=name, category=category, price=price, quantity=quantity, exp_date=exp_date,
                              img_link = img_link)
            self.session.add(product)
            self.session.commit()
            return product
        except Exception as e:
            return None

    def get_all(self):
        try:
            product_list = []
            for product in self.session.query(Product).all():
                product_list.append(product)
            return product_list
        except Exception as e:
            return None

    def get_by_id(self, id):
        try:
            product = self.session.query(Product).filter_by(id=id).first()
            if not product:
                print(f"No such product with id={id}")
                return None
            return product
        except Exception as e:
            return None

    def get_by_name(self, name):
        try:
            product = self.session.query(Product).filter_by(name=name).first()
            if not product:
                print(f"No such product with name={name}")
                return None
            return product
        except Exception as e:
            return None

    def get_by_quantity(self, quantity):
        try:
            product_by_quantity = self.session.query(Product).filter_by(quantity=quantity).all()
            if len(product_by_quantity) == 0:
                print(f"No such products with quantity={quantity}")
                return None
            return product_by_quantity
        except Exception as e:
            return None

    def get_by_price(self, price):
        try:
            products_by_price = self.session.query(Product).filter_by(price=price).all()
            if len(products_by_price) == 0:
                print(f"No such products with price={price}")
                return None
            return products_by_price
        except Exception as e:
            return None

    def get_by_category(self, category):
        try:
            products_by_cat = self.session.query(Product).filter_by(category=category.lower()).all()
            if len(products_by_cat) == 0:
                print(f"No such products with category={category}")
                return None
            return products_by_cat
        except Exception as e:
            return None
