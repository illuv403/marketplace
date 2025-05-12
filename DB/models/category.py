from DB.database import Base
from sqlalchemy import Column, Integer, String, Numeric, Date
from sqlalchemy.orm import relationship

"""
User model that stores basic information about a user.
"""
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    products = relationship('Product', back_populates='category')