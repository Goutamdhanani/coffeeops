from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI(title="CoffeeOps API", version="1.0")

MENU = [
    {"id": 1, "name": "Espresso", "price": 120},
    {"id": 2, "name": "Cappuccino", "price": 180},
    {"id": 3, "name": "Latte", "price": 200},
]

class Order(BaseModel):
    item_id: int
    qty: int = 1

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/menu")
def menu():
    return {"menu": MENU}

@app.post("/order")
def order(order: Order):
    env = os.getenv("ENV", "dev")
    item = next((x for x in MENU if x["id"] == order.item_id), None)
    if not item:
        return {"ok": False, "error": "Item not found"}
    total = item["price"] * order.qty
    return {"ok": True, "env": env, "item": item["name"], "qty": order.qty, "total": total}
