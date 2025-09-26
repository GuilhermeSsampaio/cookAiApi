from sys import prefix
from models.user import User
from fastapi import APIRouter, Query, Body, Depends
from sqlmodel import Session, select
from models.recipe import Recipe
from services.scrap import scrap_recipe
from database.db import get_session
from google import genai
import os
from pydantic import BaseModel


router = APIRouter(prefix="/recipes")
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

@router.post("/scrap")
def extract_scrap_recipe_post(url: str):
    scrap_result = scrap_recipe(url)
    return scrap_result

# class SearchRequest(BaseModel):
#     query: str

# @router.post("/search")
# def search_recipes(request: SearchRequest):
#     query = request.query
#     # Use IA para interpretar a entrada do usuário
#     prompt = f"Encontre receitas com base na seguinte especificação: {query}"
#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt,
#     )
    
#     print(response.text)
    
#     # Retorne os resultados gerados pela IA
#     return {"recipes": response.text}

class SearchRequest(BaseModel):
    query: str

@router.post("/search")
def search_recipes(request: SearchRequest):
    query = request.query
    # Use IA para interpretar a entrada do usuário
    prompt = f"""
    Encontre receitas com base na seguinte especificação: {query}.
    Retorne as receitas no seguinte formato JSON puro:
    [
        {{
            "title": "Título da receita",
            "description": "Descrição ou instruções da receita"
        }},
        ...
    ]
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    
    try:
        # Tenta interpretar a resposta como JSON
        recipes = response.text.strip()
        return {"recipes": recipes}
    except Exception as e:
        print("Erro ao interpretar a resposta:", e)
        return {"error": "Não foi possível processar a resposta da IA."}

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
