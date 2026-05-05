# Trainr Mobile API

A RESTful backend API for the Trainr fitness tracking mobile application, built with **FastAPI** and **SQLAlchemy**.

## Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
- **Database:** PostgreSQL (via [Supabase](https://supabase.com/))
- **Schema Validation:** [Pydantic v2](https://docs.pydantic.dev/)
- **Environment Config:** [python-dotenv](https://github.com/theskumar/python-dotenv)

## Project Structure

<!-- PROJECT_STRUCTURE_START -->

```
app/
├── db/
│   └── db_connection.py   # Database engine, session factory, and Base
├── exercises/
│   ├── models.py   # Exercise SQLAlchemy model
│   ├── repository.py   # Data access layer
│   ├── router.py   # FastAPI route handlers
│   ├── schemas.py   # Pydantic DTOs
│   └── service.py   # Business logic
├── foods/
│   ├── models.py   # Food SQLAlchemy model
│   ├── repository.py   # Data access layer
│   ├── router.py   # FastAPI route handlers
│   ├── schemas.py   # Pydantic DTOs
│   └── service.py   # Business logic
├── meals/
│   ├── models.py   # Meal SQLAlchemy model
│   ├── repository.py   # Data access layer
│   ├── router.py   # FastAPI route handlers
│   ├── schemas.py   # Pydantic DTOs
│   └── service.py   # Business logic
├── user_shopping_list/
│   ├── models.py   # UserShoppingList SQLAlchemy model
│   ├── repository.py   # Data access layer
│   ├── router.py   # FastAPI route handlers
│   ├── schemas.py   # Pydantic DTOs
│   └── service.py   # Business logic
├── users/
│   ├── models.py   # User SQLAlchemy model
│   ├── repository.py   # Data access layer
│   ├── router.py   # FastAPI route handlers
│   ├── schemas.py   # Pydantic DTOs
│   └── service.py   # Business logic
├── workouts/
│   ├── models.py   # Workout SQLAlchemy model
│   ├── repository.py   # Data access layer
│   ├── router.py   # FastAPI route handlers
│   ├── schemas.py   # Pydantic DTOs
│   └── service.py   # Business logic
└── main.py   # FastAPI app entry point; registers all routers
```

<!-- PROJECT_STRUCTURE_END -->

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

### Foods

**Base path:** `/foods`

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/foods/` | Get all foods |
| `GET` | `/foods/id` | Get food by id |
| `POST` | `/foods/` | Add food |
| `PATCH` | `/foods/update` | Update food |
| `DELETE` | `/foods/delete` | Delete food |

### User Shopping Lists

**Base path:** `/user_shopping_list`

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/user_shopping_list/all` | Get all shopping lists |
| `GET` | `/user_shopping_list/id` | Get shopping list by id |
| `POST` | `/user_shopping_list/` | Add shopping list |
| `PATCH` | `/user_shopping_list/update` | Update shopping list info |
| `DELETE` | `/user_shopping_list/delete` | Delete shopping list |

<!-- ROUTERS_END -->

## Data Models

<!-- DATA_MODELS_START -->

### Exercise

| Field | Type | Notes |
|-------|------|-------|
| `id` | UUID | Primary key |
| `name` | string |  |
| `description` | string |  |
| `muscle_group` | string |  |
| `equipment_type` | string |  |

### Food

| Field | Type | Notes |
|-------|------|-------|
| `id` | UUID | Primary key |
| `name` | string | Required |
| `calories_per_serving` | int | Required |
| `protein_g` | int | Required |
| `carbs_g` | int | Required |
| `fat_g` | int | Required |
| `serving_size` | string | Required |

### Meal

| Field | Type | Notes |
|-------|------|-------|
| `id` | UUID | Primary key |
| `name` | string |  |
| `meal_type` | enum (`breakfast`, `lunch`, `dinner`, `snack`) |  |
| `calories` | int |  |
| `protein_g` | int |  |
| `carbs_g` | int |  |
| `fat_g` | int |  |
| `cook_time_minutes` | int |  |
| `difficulty` | enum (`easy`, `medium`, `hard`) |  |
| `tags` | list[string] | Stored as JSONB |
| `created_at` | datetime | Auto-set on creation |
| `updated_at` | datetime | Auto-set on update |

### UserShoppingList

| Field | Type | Notes |
|-------|------|-------|
| `id` | UUID | Primary key |
| `user_id` | UUID |  |
| `start_date` | datetime |  |
| `end_date` | datetime |  |
| `created_at` | datetime | Auto-set on creation |

### User

| Field | Type | Notes |
|-------|------|-------|
| `id` | UUID | Primary key, auto-generated |
| `email` | string(30) | Unique, required |
| `password_hash` | string | Required |
| `name` | string(30) | Required |
| `age` | int |  |
| `weight` | int |  |
| `height` | int |  |
| `created_at` | datetime | Auto-set on creation |
| `updated_at` | datetime | Auto-set on update |

### Workout

| Field | Type | Notes |
|-------|------|-------|
| `id` | UUID | Primary key, auto-generated |
| `user_id` | UUID |  |
| `date` | datetime | Auto-set on creation |
| `name` | string |  |
| `notes` | string |  |
| `is_completed` | bool | Default: `false` |
| `created_at` | datetime | Auto-set on creation |

<!-- DATA_MODELS_END -->

## Contributing

When adding a new feature module (router), follow these steps:

1. Create the module directory under `app/` with `models.py`, `schemas.py`, `repository.py`, `service.py`, and `router.py`.
2. Register the router in `app/main.py` using `app.include_router(...)`.
3. Push to `main` — the [Update README workflow](.github/workflows/update-readme.yml) will automatically update the **API Endpoints**, **Project Structure**, and **Data Models** sections of this file.
