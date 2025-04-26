# main.py

from fastapi import FastAPI
from typing import Optional
import os
import uvicorn

app = FastAPI()

# Тимчасова фейкова база закладів
restaurants = [
    {"name": "Український ресторан", "type": "Ресторан", "district": "Центр", "price": "₴₴₴", "cuisine": "Українська"},
    {"name": "Бар на Дніпрі", "type": "Бар", "district": "Правий берег", "price": "₴"},
    {"name": "Кавʼярня Aroma", "type": "Кавʼярня", "district": "Лівий берег", "price": "₴"},
    {"name": "Італійська Тратторія", "type": "Ресторан", "district": "Центр", "price": "₴₴₴", "cuisine": "Італійська"},
    {"name": "CoffeeLab", "type": "Кавʼярня", "district": "Правий берег", "price": "₴"},
]

@app.get("/restaurants")
async def get_restaurants(
    type: Optional[str] = None,
    district: Optional[str] = None,
    price: Optional[str] = None,
    cuisine: Optional[str] = None
):
    result = []
    for r in restaurants:
        if type and r.get("type") != type:
            continue
        if district and r.get("district") != district:
            continue
        if price and r.get("price") != price:
            continue
        if cuisine and r.get("cuisine") != cuisine:
            continue
        result.append(r)
    return result

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # <<< Ось важливий момент для Render
    uvicorn.run("main:app", host="0.0.0.0", port=port)
