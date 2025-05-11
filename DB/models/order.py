from DB.database import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime

"""
Association table for the many-to-many relationship between Orders and Products.
Each row links a product to a specific order.
"""
order_products = Table(
    'order_products',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True)
)

"""
Order model that represents an order made by user.
"""
class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date_created = Column(DateTime, default=datetime.now().replace(microsecond=0))

    user = relationship('User', back_populates='orders')
    products = relationship('Product', secondary=order_products, back_populates='orders')