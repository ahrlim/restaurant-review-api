from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas import ReviewCreate, ReviewResponse, ReviewUpdate

router = APIRouter()


@router.post(
    "/{visit_id}/review",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_review(visit_id: int, review: ReviewCreate, db: Annotated[Session, Depends(get_db)]):
    # Check if visit_id exists
    result = db.execute(select(models.Visit).where(models.Visit.id == visit_id))
    visit = result.scalars().first()
    if not visit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visit not found"
        )
    
    # Check if review already exists for this visit_id
    result = db.execute(select(models.Review).where(models.Review.visit_id == visit_id))
    existing_review = result.scalars().first()

    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Review already exists for this visit", 
        )

    new_review = models.Review(
        visit_id=visit_id,
        rating=review.rating,
        notes=review.notes,
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


@router.get("/{visit_id}/review",response_model=ReviewResponse)
def get_review(visit_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Review).where(models.Review.visit_id == visit_id))
    review = result.scalars().first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    return review


@router.patch("/{visit_id}/review", response_model=ReviewResponse)
def update_review(
    visit_id: int,
    review_data: ReviewUpdate,
    db: Annotated[Session, Depends(get_db)]
):
    result = db.execute(select(models.Review).where(models.Review.visit_id == visit_id))
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

    no_changes = all(
        getattr(review, field) == value
        for field, value in update_data.items()
    )
    if no_changes:
        return review
    
    for field, value in update_data.items():
        setattr(review, field, value)

    db.commit()
    db.refresh(review)
    return review


@router.delete("/{visit_id}/review", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(visit_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Review).where(models.Review.visit_id == visit_id))
    review = result.scalars().first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    db.delete(review)
    db.commit()