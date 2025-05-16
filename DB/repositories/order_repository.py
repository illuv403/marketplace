from DB.database import db_session
from DB.models.order import Order
from DB.models.product import Product
from DB.models.user import User

"""
Repository class for managing Order table in a database,
so CRUD operations
"""


class OrderRepository:
    def __init__(self, session=None):
        if session is None:
            self.session = db_session
        else:
            self.session = session

    def create_order(self, user_id, product_ids):
        try:
            user = self.session.query(User).filter_by(id=user_id).first()
            if user is None:
                return None

            products = self.session.query(Product).filter(Product.id.in_(product_ids)).all()
            if not products or len(products) != len(product_ids):
                return None

            order = Order(user_id=user_id, products=products)
            self.session.add(order)
            self.session.commit()
            return order
        except Exception as e:
            print(f'Error: {e}')
            self.session.rollback()
            return None

    def update_order(self, order_id, new_product_ids=None, new_user_id=None):
        try:
            if new_product_ids is None and new_user_id is None:
                return None
            order = self.session.query(Order).filter_by(id=order_id).first()

            if new_product_ids is not None:
                new_products = self.session.query(Product).filter(Product.id.in_(new_product_ids)).all()
                order.products = new_products

            if new_user_id is not None:
                order.user = self.session.query(User).filter_by(id=new_user_id).first()

        except Exception as e:
            print(f'Error: {e}')
            self.session.rollback()
            return None

    def get_order_by_id(self, order_id):
        try:
            order = self.session.query(Order).filter_by(id=order_id).first()
            if order is None:
                return None
            return order
        except Exception as e:
            print(f'Error: {e}')
            self.session.rollback()
            return False

    def get_orders_by_user_id(self, user_id):
        try:
            orders = self.session.query(Order).filter_by(user_id=user_id).first()
            if not orders:
                return None
            return orders
        except Exception as e:
            print(f'Error: {e}')
            self.session.rollback()
            return False

    def get_all_orders(self):
        try:
            orders = self.session.query(Order).all()
            if not orders:
                return None
            return orders
        except Exception as e:
            print(f'Error: {e}')
            self.session.rollback()
            return False


    def delete_order(self, order_id):
        try:
            order = self.session.query(Order).filter_by(id=order_id).first()
            if order is None:
                return False

            self.session.delete(order)
            self.session.commit()
            return True
        except Exception as e:
            print(f'Error: {e}')
            self.session.rollback()
            return False


    def add_product_to_order(self, order_id, product_id):
        try:
            order = self.get_order_by_id(order_id)
            product = self.session.query(Product).filter_by(id=product_id).first()

            if order is None or product is None:
                return None

            if product not in order.products:
                order.products.append(product)
                self.session.commit()
            return order
        except Exception as e:
            print(f'Error: {e}')
            self.session.rollback()
            return None


    def remove_product_from_order(self, order_id, product_id):
        try:
            order = self.get_order_by_id(order_id)
            product = self.session.query(Product).filter_by(id=product_id).first()

            if order is None or product is None:
                return None

            if product in order.products:
                order.products.remove(product)
                self.session.commit()
            return order
        except Exception as e:
            print(f'Error: {e}')
            self.session.rollback()
            return None


    def clear_order_products(self, order_id):
        try:
            order = self.get_order_by_id(order_id)
            if order is None:
                return False

            order.products = []
            self.session.commit()
            return True
        except Exception as e:
            print(f'Error: {e}')
            self.session.rollback()
            return False
