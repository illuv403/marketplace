import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DB.database import Base
from DB.repositories.category_repository import CategoryRepository
from DB.models.category import Category

class TestCategoryRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///test.db')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.category_repository = CategoryRepository(self.session)

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)


    def test_create_category(self):
        self.category_repository.create_category(category_name='top_clothing')
        category = self.session.query(Category).filter_by(name='top_clothing').first()
        self.assertIsNotNone(category)

    def test_update_category(self):
        self.category_repository.create_category(category_name='top_clothing')
        category2 = self.category_repository.create_category(category_name='botom_clothing')
        self.assertEqual(category2.name, 'botom_clothing')
        self.category_repository.update_category(category_id=2, category_name='bottom_clothing')
        category2 = self.session.query(Category).filter_by(id = 2).first()
        self.assertEqual(category2.name, 'bottom_clothing')

    def test_delete_category_by_id(self):
        category = self.category_repository.create_category(category_name='top_clothing')
        self.assertIsNotNone(category)
        self.category_repository.delete_category_by_id(category_id=1)
        category = self.session.query(Category).filter_by(id = category.id).first()
        self.assertIsNone(category)

    def test_delete_category_by_name(self):
        category = self.category_repository.create_category(category_name='top_clothing')
        self.assertIsNotNone(category)
        self.category_repository.delete_category_by_name(category_name='top_clothing')
        category = self.session.query(Category).filter_by(name = category.name).first()
        self.assertIsNone(category)

    def test_get_category_by_name(self):
        self.category_repository.create_category(category_name='top_clothing')
        category = self.category_repository.get_category_by_name(category_name='top_clothing')
        self.assertEqual(category.name, 'top_clothing')

    def test_get_category_by_id(self):
        self.category_repository.create_category(category_name='top_clothing')
        category = self.category_repository.get_category_by_id(category_id=1)
        self.assertEqual(category.name, 'top_clothing')

    def test_get_all_categories(self):
        self.category_repository.create_category(category_name='top_clothing')
        self.category_repository.create_category(category_name='botom_clothing')
        self.category_repository.create_category(category_name='shoes')
        categories = self.category_repository.get_all_categories()
        self.assertEqual(len(categories), 3)


if __name__ == '__main__':
    unittest.main()
