from DB.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

"""
User model that stores basic information about a user.
"""
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    login = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)

    orders = relationship('Order', back_populates='user')

