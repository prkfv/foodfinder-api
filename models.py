# models.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    district = Column(String, nullable=False)
    price = Column(String, nullable=False)
    cuisine = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    description = Column(String, nullable=True)
    address = Column(String, nullable=True)
