### /Telegram-bot/api-server/main.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from typing import List, Optional



from models import Restaurant
from db.session import async_session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/restaurants")
async def get_restaurants(
    place_type: Optional[str] = None,
    district: Optional[str] = None,
    price_category: Optional[str] = None,
    cuisine: Optional[str] = None,
    ai_ids: Optional[str] = Query(None)
):
    async with async_session() as session:
        print("🔍 Отримано фільтри:")
        print("  - place_type:", place_type)
        print("  - district:", district)
        print("  - price_category:", price_category)
        print("  - cuisine:", cuisine)
        stmt = select(Restaurant)

        if ai_ids:
            id_list = list(map(int, ai_ids.split(",")))
            stmt = stmt.where(Restaurant.id.in_(id_list))
        else:
            if place_type:
                stmt = stmt.where(Restaurant.type == place_type)
            if district:
                stmt = stmt.where(Restaurant.district == district)
            if price_category and price_category != "Пропустити":
                stmt = stmt.where(Restaurant.price_category == price_category)
            if cuisine:
                stmt = stmt.where(Restaurant.cuisine == cuisine)

        result = await session.execute(stmt)
        restaurants = result.scalars().all()

        data = [
            {
                "id": r.id,
                "name": r.name,
                "type": r.type,
                "district": r.district,
                "price_category": r.price_category,
                "cuisine": r.cuisine,
                "description": getattr(r, "description", None),
                "lat": r.latitude,
                "lon": r.longitude,
                "phone": r.phone,
            }
            for r in restaurants
        ]
        return JSONResponse(content=data)
