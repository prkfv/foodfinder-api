from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    cuisine = Column(String, nullable=True)
    address = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    google_maps_link = Column(String, nullable=True)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    image_url = Column(String, nullable=True)  # ← чисто
    work_hours = Column(String, nullable=True)
    district = Column(String, nullable=False)
    status = Column(String, default="approved")
    price_category = Column(String, nullable=False)
    popularity = Column(Integer, default=50)
    user_id = Column(Integer, default=0)
    description = Column(String, nullable=True)  # ← для WebApp

