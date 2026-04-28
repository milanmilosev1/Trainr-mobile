from fastapi import FastAPI
from app.users.router import router as users_router
from app.meals.router import router as meals_router

app = FastAPI()

app.include_router(users_router)
app.include_router(meals_router)