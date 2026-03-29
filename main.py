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


################################################################################
# Restaurant
################################################################################
# @app.get("/api/restaurants", response_model=list[RestaurantResponse])
# def get_restaurants(db: Annotated[Session, Depends(get_db)]):
#     result = db.execute(select(models.Restaurant))
#     restaurants = result.scalars().all()
#     return restaurants


# @app.get("/api/restaurants/{restaurant_id}", response_model=RestaurantResponse)
# def get_restaurant(restaurant_id: int, db: Annotated[Session, Depends(get_db)]):
#     result = db.execute(select(models.Restaurant).where(models.Restaurant.id == restaurant_id))
#     restaurant = result.scalars().one_or_none()
#     if restaurant:
#         return restaurant
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")


# @app.post(
#     "/api/restaurants",
#     response_model=RestaurantResponse,
#     status_code=status.HTTP_201_CREATED,
# )
# def add_restaurant(restaurant: RestaurantCreate, db: Annotated[Session, Depends(get_db)]):
#     result = db.execute(
#         select(models.Restaurant).where(and_(
#             models.Restaurant.restaurant_name == restaurant.restaurant_name,
#             models.Restaurant.neighborhood == restaurant.neighborhood,
#             )
#         )
#     )
#     same_restaurant = result.scalars().first()

#     if same_restaurant:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Restaurant already exists in the database"
#         )

#     new_restaurant = models.Restaurant(
#     restaurant_name=restaurant.restaurant_name,
#     neighborhood=restaurant.neighborhood,
#     date_added=restaurant.date_added,
#     )

#     db.add(new_restaurant)
#     db.commit()
#     db.refresh(new_restaurant)

#     return new_restaurant


# @app.patch("/api/restaurants/{restaurant_id}", response_model=RestaurantResponse)
# def update_restaurant(
#     restaurant_id: int,
#     restaurant_data: RestaurantUpdate,
#     db: Annotated[Session, Depends(get_db)],
# ):
#     result = db.execute(select(models.Restaurant).where(models.Restaurant.id == restaurant_id))
#     restaurant = result.scalars().one_or_none()

#     if not restaurant:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Restaurant not found",
#         )
    
#     update_data = restaurant_data.model_dump(exclude_unset=True)
    
#     if len(update_data) == 0:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="No data is given to update"
#         )

#     no_changes = all(
#     getattr(restaurant, field) == value
#     for field, value in update_data.items()
#     )

#     if no_changes:
#         return restaurant

#     # need to check if this updated restaurant already exists
#     same_restaurant = db.execute(
#         select(models.Restaurant).where(and_(
#             models.Restaurant.restaurant_name == update_data.get("restaurant_name", restaurant.restaurant_name),
#             models.Restaurant.neighborhood == update_data.get("neighborhood", restaurant.neighborhood),
#             models.Restaurant.id != restaurant_id,
#         ))
#     ).scalars().first()

#     if same_restaurant:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Restaurant already exists in the database"
#         )

#     for field, value in update_data.items():
#         setattr(restaurant, field, value)

#     db.commit()
#     db.refresh(restaurant)
#     return restaurant


# @app.delete(
#     "/api/restaurants/{restaurant_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# def delete_restaurant(restaurant_id: int, db: Annotated[Session, Depends(get_db)]):
#     result = db.execute(select(models.Restaurant).where(models.Restaurant.id == restaurant_id))
#     restaurant = result.scalars().first()
#     if not restaurant:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Restaurant not found",
#         )

#     db.delete(restaurant)
#     db.commit()


################################################################################
# Visit
################################################################################

# @app.post(
#     "/api/restaurants/{restaurant_id}/visits",
#     response_model=VisitResponse,
#     status_code=status.HTTP_201_CREATED,
# )
# def add_visit(restaurant_id: int, visit: VisitCreate, db: Annotated[Session, Depends(get_db)]):
#     # Check if the restaurant exists
#     result = db.execute(select(models.Restaurant).where(
#         models.Restaurant.id == restaurant_id,
#     ))
#     restaurant = result.scalars().first()
#     if not restaurant:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Restaurant not found",
#         )

#     new_visit = models.Visit(
#         restaurant_id=restaurant_id,
#         date_visited=visit.date_visited,
#     )
#     db.add(new_visit)
#     db.commit()
#     db.refresh(new_visit)
#     return new_visit


# @app.get(
#     "/api/restaurants/{restaurant_id}/visits",
#     response_model=list[VisitResponse],
# )
# def get_restaurant_visits(restaurant_id: int, db: Annotated[Session, Depends(get_db)]):
#     # Check if the restaurant exists
#     result = db.execute(select(models.Restaurant).where(
#         models.Restaurant.id == restaurant_id,
#     ))
#     restaurant = result.scalars().first()
#     if not restaurant:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Restaurant not found",
#         )

#     result = db.execute(select(models.Visit).where(models.Visit.restaurant_id == restaurant_id))
#     visits = result.scalars().all()
#     return visits


# @app.get("/api/visits/{visit_id}", response_model=VisitResponse)
# def get_visit(visit_id: int, db: Annotated[Session, Depends(get_db)]):
#     result = db.execute(select(models.Visit).where(models.Visit.id == visit_id))
#     visit = result.scalars().first()
#     if not visit:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Visit_id not exists"
#         )
#     return visit


# @app.patch("/api/visits/{visit_id}", response_model=VisitResponse)
# def update_visit(
#     visit_id: int,
#     visit_data: VisitUpdate,
#     db: Annotated[Session, Depends(get_db)]
# ):
#     result = db.execute(select(models.Visit).where(models.Visit.id == visit_id))
#     visit = result.scalars().first()

#     if not visit:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Visit_id not exists"
#         )
    
#     update_data = visit_data.model_dump(exclude_unset=True)
    
#     if len(update_data) == 0:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="No data is given to update"
#         )
    
#     # Check if the given restaurant_id exists in our database
#     restaurant_id = update_data.get("restaurant_id", visit.restaurant_id)
#     result = db.execute(select(models.Restaurant).where(models.Restaurant.id == restaurant_id))
#     if not result.scalars().first():
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Restaurant not found",
#         )

#     no_changes = all(
#         getattr(visit, field) == value
#         for field, value in update_data.items()
#     )
#     if no_changes:
#         return visit
    
#     for field, value in update_data.items():
#         setattr(visit, field, value)

#     db.commit()
#     db.refresh(visit)
#     return visit


# @app.delete(
#     "/api/visits/{visit_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# def delete_visit(visit_id: int, db: Annotated[Session, Depends(get_db)]):
#     result = db.execute(select(models.Visit).where(models.Visit.id == visit_id))
#     visit = result.scalars().first()
#     if not visit:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Visit not found",
#         )

#     db.delete(visit)
#     db.commit()


################################################################################
# Review
################################################################################

# @app.post(
#     "/api/visits/{visit_id}/review",
#     response_model=ReviewResponse,
#     status_code=status.HTTP_201_CREATED,
# )
# def add_review(visit_id: int, review: ReviewCreate, db: Annotated[Session, Depends(get_db)]):
#     # Check if visit_id exists
#     result = db.execute(select(models.Visit).where(models.Visit.id == visit_id))
#     visit = result.scalars().first()
#     if not visit:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Visit not found"
#         )
    
#     # Check if review already exists for this visit_id
#     result = db.execute(select(models.Review).where(models.Review.visit_id == visit_id))
#     existing_review = result.scalars().first()

#     if existing_review:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="Review already exists for this visit", 
#         )

#     new_review = models.Review(
#         visit_id=visit_id,
#         rating=review.rating,
#         notes=review.notes,
#     )

#     db.add(new_review)
#     db.commit()
#     db.refresh(new_review)
#     return new_review


# @app.get("/api/visits/{visit_id}/review",response_model=ReviewResponse)
# def get_review(visit_id: int, db: Annotated[Session, Depends(get_db)]):
#     result = db.execute(select(models.Review).where(models.Review.visit_id == visit_id))
#     review = result.scalars().first()
#     if not review:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Review not found"
#         )
#     return review


# @app.patch("/api/visits/{visit_id}/review", response_model=ReviewResponse)
# def update_review(
#     visit_id: int,
#     review_data: ReviewUpdate,
#     db: Annotated[Session, Depends(get_db)]
# ):
#     result = db.execute(select(models.Review).where(models.Review.visit_id == visit_id))
#     review = result.scalars().first()
#     if not review:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Review not found"
#         )
    
#     update_data = review_data.model_dump(exclude_unset=True)
    
#     if len(update_data) == 0:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="No data is given to update"
#         )

#     no_changes = all(
#         getattr(review, field) == value
#         for field, value in update_data.items()
#     )
#     if no_changes:
#         return review
    
#     for field, value in update_data.items():
#         setattr(review, field, value)

#     db.commit()
#     db.refresh(review)
#     return review


# @app.delete("/api/visits/{visit_id}/review", status_code=status.HTTP_204_NO_CONTENT)
# def delete_review(visit_id: int, db: Annotated[Session, Depends(get_db)]):
#     result = db.execute(select(models.Review).where(models.Review.visit_id == visit_id))
#     review = result.scalars().first()
#     if not review:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Review not found"
#         )

#     db.delete(review)
#     db.commit()

