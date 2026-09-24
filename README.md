# Restaurant Review API

A local restaurant review app built with **FastAPI, SQLAlchemy, Pydantic, SQLite, and Jinja2**.

## Features

- Create, read, update, and delete users and reviews.
- Allow one review per restaurant name per user.
- Show reviews and reviewer usernames on HTML pages.


## Running Locally

Requires **Python 3.11+**. Activate your Python environment and run these commands from the project root:

Install dependencies:

```bash
python -m pip install "fastapi[standard]" sqlalchemy pydantic jinja2
```

Start the server:

```bash
fastapi dev main.py
```

- [Review list](http://127.0.0.1:8000/reviews)
- [Swagger UI](http://127.0.0.1:8000/docs) — explore and test the API

Press **Ctrl+C** to stop the server.

## Routes

| Path | Purpose |
| --- | --- |
| `/api/users` | Create users |
| `/api/users/{user_id}` | Read, update, or delete a user |
| `/api/users/{user_id}/reviews` | List a user's reviews |
| `/api/reviews` | Create or list reviews |
| `/api/reviews/{review_id}` | Read, update, or delete a review |
| `/` or `/reviews` | HTML review list |
| `/reviews/{review_id}` | HTML review detail |

Create a user first, then use their ID when creating a review. HTML pages are read-only; use the API or Swagger UI to manage records.

## Notes

- Visit dates default to the current time on creation; omitting them in PATCH preserves the existing date.
- Local data is stored in `restaurant-review-api.db`, which is excluded from Git.
- Startup creates missing tables but does not modify existing tables. Model changes require a separate database migration.
- Login and ownership-based authorization are not implemented.
