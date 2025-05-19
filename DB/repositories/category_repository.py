from DB.database import db_session
from DB.models.category import Category
from DB.models.product import Product


class CategoryRepository:
    """Repository class for managing Category table in a database.

    Handles CRUD (Create, Read, Update, Delete) operations for the Category model.
    """

    def __init__(self, session=None):
        """Initialize with optional custom database session."""
        self.session = session if session is not None else db_session

    def create_category(self, category_name):
        """Create a new category with the given name."""
        try:
            category_exists = self.session.query(Category).filter(
                Category.name == category_name.lower()
            ).first() is not None

            if category_exists:
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
        """Update an existing category's name."""
        try:
            category = self.session.query(Category).filter(
                Category.id == category_id
            ).first()

            if category is None:
                print(f"Category with id {category_id} does not exist.")
                return None

            category.name = category_name
            self.session.commit()
            return category

        except Exception as e:
            print(f'Error: {e}')
            self.session.rollback()
            return None

    def get_category_by_id(self, category_id):
        """Retrieve a category by its ID."""
        try:
            category = self.session.query(Category).filter_by(id=category_id).first()

            if category is None:
                print(f"Category with id {category_id} does not exist.")
                return None

            return category

        except Exception as e:
            print(f'Error: {e}')
            self.session.rollback()
            return None

    def get_category_by_name(self, category_name):
        """Retrieve a category by its name."""
        try:
            category = self.session.query(Category).filter_by(name=category_name).first()

            if category is None:
                print(f"Category with name {category_name} does not exist.")
                return None

            return category

        except Exception as e:
            print(f'Error: {e}')
            self.session.rollback()
            return None

    def get_all_categories(self):
        """Retrieve all categories from the database."""
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
        """Delete a category by its ID."""
        try:
            category = self.session.query(Category).filter_by(id=category_id).first()

            if category is None:
                print(f"Category with id {category_id} does not exist.")
                return None

            self.session.delete(category)
            self.session.commit()
            return category

        except Exception as e:
            print(f'Error: {e}')
            self.session.rollback()
            return None

    def delete_category_by_name(self, category_name):
        """Delete a category by its name."""
        try:
            category = self.session.query(Category).filter_by(name=category_name).first()

            if category is None:
                print(f"Category with name {category_name} does not exist.")
                return None

            self.session.delete(category)
            self.session.commit()
            return category

        except Exception as e:
            print(f'Error: {e}')
            self.session.rollback()
            return None