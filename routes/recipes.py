from fastapi import APIRouter, Query, Body, Depends
from sqlmodel import Session, select
from models.recipe import Recipe
from services.scrap import scrap_recipe
from database.db import engine
from utils.extract_fields import extract_title

def get_session():
    with Session(engine) as session:
        yield session

router = APIRouter()

@router.get("/saved_recipes")
def get_recipes(session: Session = Depends(get_session)):
    recipes = session.exec(select(Recipe)).all()
    return recipes

@router.get("/scrap")
def extract_scrap_recipe_get(url: str = Query(...)):
    scrap_result = scrap_recipe(url)
    return scrap_result

@router.post("/scrap")
def extract_scrap_recipe_post(url: str):
    scrap_result = scrap_recipe(url)
    return scrap_result

@router.post("/save_recipe")
def save_recipe(recipe: dict = Body(...), session: Session = Depends(get_session)):
    try:
        new_recipe = Recipe(content=recipe["recipe"])
        session.add(new_recipe)
        session.commit()
        session.refresh(new_recipe)
        title = extract_title(new_recipe.content)
        if title:
            new_recipe.title = title
            session.add(new_recipe)
            session.commit()
            session.refresh(new_recipe)
        return {"status": "Recipe saved successfully", "recipe_id": new_recipe.id}
    except Exception as e:
        session.rollback()
        return {"status": "error", "message": str(e)}

