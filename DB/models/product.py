from DB.database import Base
from sqlalchemy import Column, Integer, String, Numeric, Date
from sqlalchemy.orm import relationship


"""
Product model, stores information about a products, their 
quantities and expiration date of the product (if applicable).
"""
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Numeric(10, 2), nullable=False)
    exp_date = Column(Date, nullable=True)
    img_link = Column(String(100), nullable=True)

    orders = relationship('Order', secondary='order_products', back_populates='products')