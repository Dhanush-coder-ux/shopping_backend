from sqlalchemy import Column,String,Integer,ForeignKey,ARRAY
from database.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ ='users'
    id =Column(Integer,primary_key=True,unique=True,autoincrement=True)
    username   = Column(String,index=True,unique=True)
    email=Column(String,index=True,unique=True)
    password =Column(String)
    role =Column(String,default='user',index=True)

    cart=relationship("Cart",back_populates="user",cascade="delete-orphan, all")
    orders = relationship("Orders", back_populates="user")

 
class Cart(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    product_id = Column(String, ForeignKey("products.id",ondelete="CASCADE"))
    size = Column(String)
    quantity = Column(Integer, default=1)

    user = relationship("User", back_populates="cart")
    product = relationship("Product")


     
