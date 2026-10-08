from contextlib import asynccontextmanager
from typing import Annotated

from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from starlette.exceptions import HTTPException as StarletteHTTPException

from database import Base, engine, get_db
from routers import  reviews, users

import models

@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(
    users.router,
    prefix="/api/users",
    tags=["users"],
)

app.include_router(
    reviews.router,
    prefix="/api/reviews",
    tags=["reviews"],
)

@app.get("/", name="home")
@app.get("/reviews", name="reviews")
async def home(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Review)
        .options(selectinload(models.Review.reviewer))
        .order_by(models.Review.date_visited.desc()),
    )
    reviews = result.scalars().all()
    return templates.TemplateResponse("home.html", {"request": request, "reviews": reviews})


@app.get("/reviews/{review_id}")
async def review_page(request: Request, review_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Review)
        .options(selectinload(models.Review.reviewer))
        .where(models.Review.id == review_id),
    )
    review = result.scalars().first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    return templates.TemplateResponse(
        "review.html",
        {"request": request, "review": review},
    )


@app.get("/users/{user_id}/reviews", name="user_reviews")
async def user_reviews_page(
    request: Request,
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    result = await db.execute(
        select(models.Review)
        .options(selectinload(models.Review.reviewer))
        .where(models.Review.user_id == user_id)
        .order_by(models.Review.date_visited.desc()),
    )
    reviews = result.scalars().all()
    return templates.TemplateResponse(
        "user_reviews.html",
        {"request": request, "reviews": reviews, "user_id": user_id, "user": user},
    )


@app.exception_handler(StarletteHTTPException)
async def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    if request.url.path.startswith("/api"):
        return await http_exception_handler(request, exception)

    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return await request_validation_exception_handler(request, exception)

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )