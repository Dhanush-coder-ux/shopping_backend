from sqlalchemy import String, Column, Integer, ForeignKey, ARRAY, Boolean, DateTime, func, Enum as SQLenum
from database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from enum import Enum

class OrderStatus(str, Enum): 
    ORDER_PENDING="Pending" 
    CANCELED="Canceled"
    ORDER_PLACED = "Order Placed"
    PACKING = "Packing"
    SHIPPING = "Shipped"
    OUT_FOR_DELIVERY = "Out for delivery"
    DELIVERED = "Delivered"

class Orders(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    products = Column(JSONB)
    amount = Column(Integer)
    address = Column(ARRAY(String))
    status = Column(String, default=OrderStatus.ORDER_PENDING.value)
    paymentmethod = Column(String)
    payment = Column(Boolean, default=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="orders")
