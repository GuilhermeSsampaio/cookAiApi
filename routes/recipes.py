from sys import prefix
from models.user import User
from fastapi import APIRouter, Query, Body, Depends
from sqlmodel import Session, select
from models.recipe import Recipe
from services.scrap import scrap_recipe
from database.db import get_session

router = APIRouter(prefix="/recipes")

@router.post("/scrap")
def extract_scrap_recipe_post(url: str):
    scrap_result = scrap_recipe(url)
    return scrap_result


# @router.post("/edit_recipe")
# def edit_recipe_post(
#     recipe: str = Body(..., embed=True, example="Ingredientes: 2 ovos, 1 xícara de farinha. Modo de preparo: Misture tudo e asse."),
#     session: Session = Depends(get_session),
#     current_user: User = Depends(User.get_current_user)
# ):
#     new_recipe = Recipe(content=recipe, owner_id=current_user.id)
#     session.add(new_recipe)
#     session.commit()
#     session.refresh(new_recipe)
#     return {"status": "Recipe saved successfully", "recipe_id": new_recipe.id}
