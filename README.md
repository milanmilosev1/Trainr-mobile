# Trainr Mobile API

A RESTful backend API for the Trainr fitness tracking mobile application, built with **FastAPI** and **SQLAlchemy**.

## Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
- **Database:** PostgreSQL (via [Supabase](https://supabase.com/))
- **Schema Validation:** [Pydantic v2](https://docs.pydantic.dev/)
- **Environment Config:** [python-dotenv](https://github.com/theskumar/python-dotenv)

## Project Structure

```
app/
├── db/
│   └── db_connection.py   # Database engine, session factory, and Base
├── users/
│   ├── models.py          # User SQLAlchemy model
│   ├── schemas.py         # Pydantic DTOs (Create, Update, Response)
│   ├── repository.py      # Data access layer
│   ├── service.py         # Business logic
│   └── router.py          # FastAPI route handlers
├── meals/
│   ├── models.py          # Meal SQLAlchemy model (with MealType & MealDifficulty enums)
│   ├── schemas.py         # Pydantic DTOs
│   ├── repository.py      # Data access layer
│   ├── service.py         # Business logic
│   └── router.py          # FastAPI route handlers
├── workouts/
│   ├── models.py          # Workout SQLAlchemy model
│   ├── schemas.py         # Pydantic DTOs
│   ├── repository.py      # Data access layer
│   ├── service.py         # Business logic
│   └── router.py          # FastAPI route handlers
└── main.py                # FastAPI app entry point; registers all routers
```

## Setup

### Prerequisites

- Python 3.11+
- A PostgreSQL database (e.g. a [Supabase](https://supabase.com/) project)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/milanmilosev1/Trainr-mobile.git
cd Trainr-mobile

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env   # then fill in SUPABASE_URL
```

### Environment Variables

| Variable       | Description                                      |
|----------------|--------------------------------------------------|
| `SUPABASE_URL` | PostgreSQL connection string for your database   |

### Running the API

```bash
uvicorn app.main:app --reload
```

The interactive API docs are available at `http://localhost:8000/docs`.

## API Endpoints

The table below is automatically kept up-to-date by the [`scripts/update_readme.py`](scripts/update_readme.py) script whenever a router is added or changed.

<!-- ROUTERS_START -->

### Users

**Base path:** `/users`

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/users/all` | Get all users |
| `GET` | `/users/id` | Get user by id |
| `POST` | `/users/` | Add user |
| `PATCH` | `/users/update` | Update user info |
| `DELETE` | `/users/delete` | Delete user |

### Meals

**Base path:** `/meals`

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/meals/all` | Get all meals |
| `GET` | `/meals/id` | Get meal by id |
| `POST` | `/meals/` | Add meal |
| `PATCH` | `/meals/update` | Update meal |
| `DELETE` | `/meals/delete` | Remove meal |

### Workouts

**Base path:** `/workouts`

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/workouts/all` | Get all workouts |
| `GET` | `/workouts/id` | Get workout by id |
| `POST` | `/workouts/` | Add new workout |
| `PATCH` | `/workouts/update` | Update workout info |
| `DELETE` | `/workouts/id` | Remove workout |

### Exercises

**Base path:** `/exercises`

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/exercises/` | Get all exercises |
| `GET` | `/exercises/id` | Get exercise by id |
| `POST` | `/exercises/` | Add exercise |
| `PATCH` | `/exercises/update` | Update exercise |
| `DELETE` | `/exercises/delete` | Remove exercise |

<!-- ROUTERS_END -->

## Data Models

### User

| Field           | Type       | Notes                    |
|-----------------|------------|--------------------------|
| `id`            | UUID       | Primary key, auto-generated |
| `email`         | string(30) | Unique, required         |
| `password_hash` | string     | Required                 |
| `name`          | string(30) | Required                 |
| `age`           | int        |                          |
| `weight`        | int        |                          |
| `height`        | int        |                          |
| `created_at`    | datetime   | Auto-set on creation     |
| `updated_at`    | datetime   | Auto-set on update       |

### Meal

| Field               | Type                                        | Notes                  |
|---------------------|---------------------------------------------|------------------------|
| `id`                | UUID                                        | Primary key            |
| `name`              | string                                      | Required               |
| `meal_type`         | enum (`breakfast`, `lunch`, `dinner`, `snack`) | Required            |
| `calories`          | int                                         |                        |
| `protein_g`         | int                                         | Protein in grams       |
| `carbs_g`           | int                                         | Carbohydrates in grams |
| `fat_g`             | int                                         | Fat in grams           |
| `cook_time_minutes` | int                                         |                        |
| `difficulty`        | enum (`easy`, `medium`, `hard`)             |                        |
| `tags`              | list[string]                                | Stored as JSONB        |
| `created_at`        | datetime                                    | Auto-set on creation   |
| `updated_at`        | datetime                                    | Auto-set on update     |

### Workout

| Field          | Type     | Notes                       |
|----------------|----------|-----------------------------|
| `id`           | UUID     | Primary key, auto-generated |
| `user_id`      | UUID     | References a user           |
| `date`         | datetime |                             |
| `name`         | string   |                             |
| `notes`        | string   |                             |
| `is_completed` | bool     | Default: `false`            |
| `created_at`   | datetime | Auto-set on creation        |

## Contributing

When adding a new feature module (router), follow these steps:

1. Create the module directory under `app/` with `models.py`, `schemas.py`, `repository.py`, `service.py`, and `router.py`.
2. Register the router in `app/main.py` using `app.include_router(...)`.
3. Push to `main` — the [Update README workflow](.github/workflows/update-readme.yml) will automatically update the **API Endpoints** section of this file.
