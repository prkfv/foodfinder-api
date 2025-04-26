from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from fastapi.middleware.cors import CORSMiddleware

from config import DATABASE_URL  # Імпорт DATABASE_URL із config.py

app = FastAPI(
    title="FoodFinderKyiv API",
    version="1.0.0"
)

# Дозволяємо CORS-запити для вебаппу
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # можна обмежити якщо потрібно буде
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Підключення до бази даних
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Модель для відповідей (поки без окремих pydantic-схем)
@app.get("/restaurants")
async def get_restaurants():
    async with async_session() as session:
        query = select(
            "name",
            "type",
            "district",
            "price",
            "cuisine"
        ).select_from("restaurants")
        result = await session.execute(query)
        rows = result.fetchall()
        restaurants = [
            {
                "name": row[0],
                "type": row[1],
                "district": row[2],
                "price": row[3],
                "cuisine": row[4],
            }
            for row in rows
        ]
        return restaurants
