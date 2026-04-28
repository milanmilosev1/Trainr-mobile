from app.meals.models import MealType, MealDifficulty


class CreateMealDTO:
    name: str
    meal_type: MealType
    calories: int
    protein_g: int
    carbs_g: int
    fat_g: int
    cook_time_minutes: int
    difficulty: MealDifficulty
    tags: str