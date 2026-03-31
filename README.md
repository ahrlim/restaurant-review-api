# Restaurant Review API

A simple single-user REST API for tracking restaurants, visits, and reviews.

## Overview

This project is a backend API built with **FastAPI** and **SQLAlchemy**. It stores data in a local **SQLite** database and supports:

- Managing saved restaurants.
- Tracking visits to restaurants.
- Adding one review per visit.

## Features

- CRUD operations for restaurants.
- CRUD operations for visits.
- CRUD operations for reviews.
- Validation with Pydantic schemas (for example, review ratings are constrained to `0..10`).
- One-to-many relationship: `Restaurant -> Visits`.
- One-to-one relationship: `Visit -> Review`.

## Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy (ORM)
- Pydantic
- SQLite

## Required Packages

Based on the source code imports, these are the required third-party packages:

- `fastapi[standard]`
- `sqlalchemy`
- `pydantic`

`fastapi[standard]` installs the recommended server/runtime extras (including `uvicorn`) for local development.

### Example install

```bash
pip install "fastapi[standard]" sqlalchemy pydantic
```

## Project Structure

```text
.
├── main.py
├── database.py
├── models.py
├── schemas.py
├── routers/
│   ├── restaurants.py
│   ├── visits.py
│   └── reviews.py
└── README.md
```

## Data Model

- **Restaurant**
  - `id`, `restaurant_name`, `neighborhood`, `date_added`
  - has many `visits`
- **Visit**
  - `id`, `date_visited`, `restaurant_id`
  - belongs to one `restaurant`
  - has one `review`
- **Review**
  - `id`, `rating`, `notes`, `visit_id`
  - belongs to one `visit`
  - `visit_id` is unique (one review per visit)

## API Routes

Base route health/test endpoint:

- `GET /`

Restaurants:

- `POST /api/restaurants`
- `GET /api/restaurants`
- `GET /api/restaurants/{restaurant_id}`
- `PATCH /api/restaurants/{restaurant_id}`
- `DELETE /api/restaurants/{restaurant_id}`

Visits:

- `POST /api/restaurants/{restaurant_id}/visits`
- `GET /api/restaurants/{restaurant_id}/visits`
- `GET /api/visits/{visit_id}`
- `PATCH /api/visits/{visit_id}`
- `DELETE /api/visits/{visit_id}`

Reviews:

- `POST /api/visits/{visit_id}/review`
- `GET /api/visits/{visit_id}/review`
- `PATCH /api/visits/{visit_id}/review`
- `DELETE /api/visits/{visit_id}/review`

## Running Locally

1. Install dependencies:

   ```bash
   pip install "fastapi[standard]" sqlalchemy pydantic
   ```

2. Start the server:

   ```bash
   uvicorn main:app --reload
   ```

3. Open:

- API root: `http://localhost:8000/`
- Swagger UI: `http://localhost:8000/docs`

## Notes

- The app automatically creates tables on startup.
- SQLite database file is created at `./restaurant-review-api.db`.
