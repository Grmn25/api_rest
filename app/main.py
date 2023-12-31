from fastapi import FastAPI
from app.routes import users, categorys, products, product_image, clients, reviews, purchases, offers
from app.database import database
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router)
app.include_router(clients.router)
app.include_router(categorys.router)
app.include_router(products.router)
app.include_router(product_image.router)
app.include_router(reviews.router)
app.include_router(purchases.router)
app.include_router(offers.router)


@app.on_event('startup')
async def startup_db_client():
    await database.connect()


@app.on_event('shutdown')
async def shutdown_db_client():
    await database.disconnect()
