from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, and_
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas import RestaurantCreate, RestaurantResponse, RestaurantUpdate

router = APIRouter()

@router.post(
    "",
    response_model=RestaurantResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_restaurant(restaurant: RestaurantCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.Restaurant).where(and_(
            models.Restaurant.restaurant_name == restaurant.restaurant_name,
            models.Restaurant.neighborhood == restaurant.neighborhood,
            )
        )
    )
    same_restaurant = result.scalars().first()

    if same_restaurant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Restaurant already exists in the database"
        )

    new_restaurant = models.Restaurant(
    restaurant_name=restaurant.restaurant_name,
    neighborhood=restaurant.neighborhood,
    date_added=restaurant.date_added,
    )

    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)

    return new_restaurant


@router.get("", response_model=list[RestaurantResponse])
def get_restaurants(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Restaurant))
    restaurants = result.scalars().all()
    return restaurants


@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(restaurant_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Restaurant).where(models.Restaurant.id == restaurant_id))
    restaurant = result.scalars().one_or_none()
    if restaurant:
        return restaurant
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")


@router.patch("/{restaurant_id}", response_model=RestaurantResponse)
def update_restaurant(
    restaurant_id: int,
    restaurant_data: RestaurantUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    result = db.execute(select(models.Restaurant).where(models.Restaurant.id == restaurant_id))
    restaurant = result.scalars().one_or_none()

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )
    
    update_data = restaurant_data.model_dump(exclude_unset=True)
    
    if len(update_data) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data is given to update"
        )

    no_changes = all(
    getattr(restaurant, field) == value
    for field, value in update_data.items()
    )

    if no_changes:
        return restaurant

    # need to check if this updated restaurant already exists
    same_restaurant = db.execute(
        select(models.Restaurant).where(and_(
            models.Restaurant.restaurant_name == update_data.get("restaurant_name", restaurant.restaurant_name),
            models.Restaurant.neighborhood == update_data.get("neighborhood", restaurant.neighborhood),
            models.Restaurant.id != restaurant_id,
        ))
    ).scalars().first()

    if same_restaurant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Restaurant already exists in the database"
        )

    for field, value in update_data.items():
        setattr(restaurant, field, value)

    db.commit()
    db.refresh(restaurant)
    return restaurant


@router.delete(
    "/{restaurant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_restaurant(restaurant_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Restaurant).where(models.Restaurant.id == restaurant_id))
    restaurant = result.scalars().first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )

    db.delete(restaurant)
    db.commit()