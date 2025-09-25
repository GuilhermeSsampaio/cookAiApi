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



