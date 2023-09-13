import os
from typing import Union

from fastapi import FastAPI
from fastapi.routing import APIRouter
from app.routes import users, categorys, products, product_image
from app.database import database

app = FastAPI()

app.include_router(users.router)
app.include_router(categorys.router)
app.include_router(products.router)
app.include_router(product_image.router)

@app.on_event('startup')
async def startup_db_client():
    await database.connect() 

@app.on_event('shutdown')
async def shutdown_db_client():
    await database.disconnect()

