from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas import VisitCreate, VisitResponse, VisitUpdate

router = APIRouter()


@router.post(
    "/restaurants/{restaurant_id}/visits",
    response_model=VisitResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_visit(restaurant_id: int, visit: VisitCreate, db: Annotated[Session, Depends(get_db)]):
    # Check if the restaurant exists
    result = db.execute(select(models.Restaurant).where(
        models.Restaurant.id == restaurant_id,
    ))
    restaurant = result.scalars().first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )

    new_visit = models.Visit(
        restaurant_id=restaurant_id,
        date_visited=visit.date_visited,
    )
    db.add(new_visit)
    db.commit()
    db.refresh(new_visit)
    return new_visit


@router.get(
    "/restaurants/{restaurant_id}/visits",
    response_model=list[VisitResponse],
)
def get_restaurant_visits(restaurant_id: int, db: Annotated[Session, Depends(get_db)]):
    # Check if the restaurant exists
    result = db.execute(select(models.Restaurant).where(
        models.Restaurant.id == restaurant_id,
    ))
    restaurant = result.scalars().first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )

    result = db.execute(select(models.Visit).where(models.Visit.restaurant_id == restaurant_id))
    visits = result.scalars().all()
    return visits


@router.get("/visits/{visit_id}", response_model=VisitResponse)
def get_visit(visit_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Visit).where(models.Visit.id == visit_id))
    visit = result.scalars().first()
    if not visit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visit_id not exists"
        )
    return visit


@router.patch("/visits/{visit_id}", response_model=VisitResponse)
def update_visit(
    visit_id: int,
    visit_data: VisitUpdate,
    db: Annotated[Session, Depends(get_db)]
):
    result = db.execute(select(models.Visit).where(models.Visit.id == visit_id))
    visit = result.scalars().first()

    if not visit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visit_id not exists"
        )
    
    update_data = visit_data.model_dump(exclude_unset=True)
    
    if len(update_data) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data is given to update"
        )
    
    # Check if the given restaurant_id exists in our database
    restaurant_id = update_data.get("restaurant_id", visit.restaurant_id)
    result = db.execute(select(models.Restaurant).where(models.Restaurant.id == restaurant_id))
    if not result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )

    no_changes = all(
        getattr(visit, field) == value
        for field, value in update_data.items()
    )
    if no_changes:
        return visit
    
    for field, value in update_data.items():
        setattr(visit, field, value)

    db.commit()
    db.refresh(visit)
    return visit


@router.delete(
    "/visits/{visit_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_visit(visit_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Visit).where(models.Visit.id == visit_id))
    visit = result.scalars().first()
    if not visit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visit not found",
        )

    db.delete(visit)
    db.commit()

    