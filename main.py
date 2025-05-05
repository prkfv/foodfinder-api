# main.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import Base, Restaurant
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.future import select
from fastapi.middleware.cors import CORSMiddleware
from config import DATABASE_URL


app = FastAPI()

# Підключення до бази
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

# CORS (щоб фронт міг підтягувати дані без помилок)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/restaurants")
async def get_restaurants(place_type: str, district: str, price_category: str, cuisine: str = None):
    async with async_session() as session:
        stmt = select(Restaurant).where(
            Restaurant.type == place_type,
            Restaurant.district == district,
            Restaurant.price_category == price_category
        )
        if cuisine:
            stmt = stmt.where(Restaurant.cuisine == cuisine)

        result = await session.execute(stmt)
        restaurants = result.scalars().all()

        return [{
            "id": r.id,
            "name": r.name,
            "type": r.type,
            "district": r.district,
            "price_category": r.price_category,
            "cuisine": r.cuisine,
            "image_url": r.photo_url,
            "description": r.work_hours,
            "address": r.address,
            "phone": r.phone,
            "map_url": r.google_maps_link,
            "latitude": r.latitude,
            "longitude": r.longitude,
        } for r in restaurants]

