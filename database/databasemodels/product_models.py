from sqlalchemy import Column,Integer,String,Boolean,ARRAY,LargeBinary,ForeignKey
from sqlalchemy.orm  import relationship
from database.database import Base



class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    category = Column(String, nullable=False)
    subcategory = Column(String, nullable=False)
    sizes = Column(ARRAY(String), nullable=False)  
    bestseller = Column(Boolean, default=False)
    

    product_image =relationship('ProductImages',back_populates='product',cascade="all, delete-orphan")
   


class ProductImages(Base):
     __tablename__ ='productimages'
     id = Column(String,primary_key=True)
     image = Column(LargeBinary, nullable=True)
     image_url =Column(String,nullable=False)
     product_id =Column(ForeignKey('products.id',ondelete="CASCADE")) 
     product = relationship('Product' , back_populates="product_image")



     