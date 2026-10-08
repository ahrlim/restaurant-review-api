from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, selectinload

import models
from database import get_db
from schemas import ReviewCreate, ReviewResponse, ReviewUpdate

router = APIRouter()


@router.post(
    "",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_review(review: ReviewCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    # Check if the user exists
    result = await db.execute(select(models.User).where(models.User.id == review.user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Check if the user already wrote a review for the same restaurant
    result = await db.execute(
        select(models.Review)
        .where(
            models.Review.user_id == review.user_id,
            models.Review.restaurant_name == review.restaurant_name,
        )
    )
    existing_review = result.scalars().first()

    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You already have a review for this restaurant",
        )
    
    new_review = models.Review(
        restaurant_name=review.restaurant_name,
        review=review.review,
        user_id=review.user_id,
        date_visited=review.date_visited,
    )

    db.add(new_review)
    await db.commit()
    await db.refresh(new_review, attribute_names=["reviewer"])
    return new_review


@router.get("",response_model=list[ReviewResponse])
async def get_reviews(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Review)
        .options(selectinload(models.Review.reviewer))
        .order_by(models.Review.date_visited.desc()),
    )
    reviews = result.scalars().all()
    return reviews


@router.get("/{review_id}",response_model=ReviewResponse)
async def get_review(review_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
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
    return review


@router.patch("/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: int,
    review_data: ReviewUpdate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
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
    
    update_data = review_data.model_dump(exclude_unset=True)

    if len(update_data) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data is given to update"
        )

    if "restaurant_name" in update_data and update_data["restaurant_name"] is None:
        raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="restaurant_name cannot be null",
        )

    # Check if the user already wrote a review for the same restaurant
    new_name = update_data.get("restaurant_name")

    if new_name is not None and new_name != review.restaurant_name:
        result = await db.execute(
            select(models.Review)
            .where(
                models.Review.user_id == review.user_id,
                models.Review.restaurant_name == new_name,
                models.Review.id != review.id,
            ),
        )
        if result.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You already have a review for this restaurant",
            )

    no_changes = all(
        getattr(review, field) == value
        for field, value in update_data.items()
    )
    if no_changes:
        return review
    
    for field, value in update_data.items():
        setattr(review, field, value)

    await db.commit()
    await db.refresh(review)
    return review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(review_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.Review).where(models.Review.id == review_id))
    review = result.scalars().first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    await db.delete(review)
    await db.commit()

