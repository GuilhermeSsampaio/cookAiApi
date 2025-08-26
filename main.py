from fastapi import FastAPI, Query,Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from services.scrap import scrap_recipe
import os
from database.db import init_db, engine
from models.recipe import Recipe
from sqlmodel import Session, select

app = FastAPI()

port = int(os.environ.get("PORT", 8000))


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_session():
    with Session(engine) as session:
        yield session

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to the CookAi API"}

@app.get("/scrap")
def extract_scrap_recipe_get(url: str = Query(...)):
    scrap_result = scrap_recipe(url)
    return scrap_result

@app.post("/scrap")
def extract_scrap_recipe_post(url: str):
    scrap_result = scrap_recipe(url)
    return scrap_result

@app.post("/save_recipe")
def save_recipe(recipe: dict = Body(...), session: Session = Depends(get_session)):
    try:
        new_recipe = Recipe(content=recipe["recipe"])
        session.add(new_recipe)
        session.commit()
        session.refresh(new_recipe)
        return {"status": "Recipe saved successfully", "recipe_id": new_recipe.id}
    except Exception as e:
        session.rollback()
        return {"status": "error", "message": str(e)}
    
    
@app.get("/recipes")
def get_recipes(session: Session = Depends(get_session)):
    recipes = session.exec(select(Recipe)).all()
    return recipes

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 