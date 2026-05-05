from fastapi import FastAPI
from app.users.router import router as users_router
from app.meals.router import router as meals_router
from app.workouts.router import router as workouts_router
from app.exercises.router import router as exercises_router
from app.foods.router import router as foods_router
from app.user_shopping_list.router import router as user_shopping_lists_router

app = FastAPI()

app.include_router(users_router)
app.include_router(meals_router)
app.include_router(workouts_router)
app.include_router(exercises_router)
app.include_router(foods_router)
app.include_router(user_shopping_lists_router)