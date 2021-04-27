from typing import Optional
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def home():
    return {"Hello": "Home"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
