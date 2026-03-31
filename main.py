from fastapi import FastAPI

from database import Base, engine
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
