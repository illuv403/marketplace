from DB.database import db_session
from DB.models.category import Category
from DB.models.product import Product


"""
Repository class for managing Category table in a database,
so CRUD operations
"""
class CategoryRepository:
    def __init__(self, session=None):
        if session is None:
            self.session = db_session
        else:
            self.session = session

    def create_category(self, category_name):
        try:
            if self.session.query(Category).filter(Category.name == category_name.lower()).first() is not None:
                print(f"Category with name {category_name} already exists.")
                return None

            category = Category(name=category_name.lower())

            self.session.add(category)
            self.session.commit()
            return category
        except Exception as e:
            print(f'Error: {e}')
            self.session.rollback()
            return None

    def update_category(self, category_id, category_name):
        try:
            if self.session.query(Category).filter(Category.id == category_id).first() is None:
                print(f"Category with name {category_name} does not exist.")
                return None

            category = self.session.query(Category).filter(Category.id == category_id).first()
            category.name = category_name
            self.session.commit()
            return category
        except Exception as e:
            print(f'Error: {e}')
            self.session.rollback()
            return None

    def get_category_by_id(self, category_id):
        try:
            if self.session.query(Category).filter(Category.id == category_id).first() is None:
                print(f"Category with id {category_id} does not exist.")
                return None

            category = self.session.query(Category).filter_by(id=category_id).first()
            return category
        except Exception as e:
            print(f'Error: {e}')
            self.session.rollback()
            return None

    def get_category_by_name(self, category_name):
        try:
            if self.session.query(Category).filter(Category.name == category_name).first() is None:
                print(f"Category with name {category_name} does not exist.")
                return None

            category = self.session.query(Category).filter_by(name=category_name).first()
            return category
        except Exception as e:
            print(f'Error: {e}')
            self.session.rollback()
            return None

    def get_all_categories(self):
        try:
            categories = self.session.query(Category).all()
            if not categories:
                return None
            return categories
        except Exception as e:
            print(f'Error: {e}')
            self.session.rollback()
            return None

    def delete_category_by_id(self, category_id):
        try:

            if self.session.query(Category).filter(Category.id == category_id).first() is None:
                print(f"Category with id {category_id} does not exist.")
                return None
            category = self.session.query(Category).filter_by(id=category_id).first()

            self.session.delete(category)
            self.session.commit()
            return category
        except Exception as e:
            print(f'Error: {e}')
            self.session.rollback()
            return None

    def delete_category_by_name(self, category_name):
        try:
            if self.session.query(Category).filter(Category.name == category_name).first() is None:
                print(f"Category with name {category_name} does not exist.")
                return None
            category = self.session.query(Category).filter_by(name=category_name).first()

            self.session.delete(category)
            self.session.commit()
            return category
        except Exception as e:
            print(f'Error: {e}')
            self.session.rollback()
            return None
