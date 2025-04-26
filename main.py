# main.py
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.future import select
from fastapi.middleware.cors import CORSMiddleware
from config import DATABASE_URL
from models import Base, Restaurant

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
async def get_restaurants():
    async with async_session() as session:
        result = await session.execute(select(Restaurant))
        restaurants = result.scalars().all()
        return [
            {
                "id": r.id,
                "name": r.name,
                "type": r.type,
                "district": r.district,
                "price": r.price,
                "cuisine": r.cuisine,
                "image_url": r.image_url,
                "description": r.description,
                "address": r.address
            }
            for r in restaurants
        ]
