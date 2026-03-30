from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session


import models
from database import Base, engine, get_db
from routers import restaurants, visits, reviews


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    restaurants.router,
    prefix="/api/restaurants",
    tags=["restaurants"],
)
app.include_router(
    visits.router,
    prefix="/api",
    tags=["visits"],
)
app.include_router(
    reviews.router,
    prefix="/api/visits",
    tags=["reviews"],
)

@app.get("/")
def home():
    return "Single user restaurant review project!"
