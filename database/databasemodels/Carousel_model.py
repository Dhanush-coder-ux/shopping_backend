from sqlalchemy import Column,Integer,String,Boolean,ARRAY,LargeBinary
from database.database import Base
from  sqlalchemy.orm import relationship

class CarouselBanner(Base):
    __tablename__="carouselbanner"
    id=Column(Integer,primary_key=True)
    image=Column(LargeBinary)
    image_url=Column(String)
 