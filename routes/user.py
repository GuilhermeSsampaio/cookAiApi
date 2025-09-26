from sys import prefix
from models import User, Recipe
from sqlmodel import Session, select
from database.db import get_session
from fastapi import APIRouter, Depends, Body
from utils.extract_fields import extract_title

router = APIRouter(prefix="/user")

@router.post("/create_user")
def create_user(user: User = Body(...), session: Session = Depends(get_session)):
    try:
        new_user = User(username=user.username, email=user.email, password_hash=user.password_hash, is_premium=user.is_premium)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return {"status": "User created successfully", "user_id": new_user.id}
    except Exception as e:
        session.rollback()
        return {"status": "error", "message": str(e)}
    
@router.post("/login_user")
def login_user(email: str = Body(...), password_hash: str = Body(...), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == email, User.password_hash == password_hash)).first()
    if not user:
        return {"status": "error", "message": "Invalid email or password"}
    return {"status": "Login successful", "user_id": user.id, "username": user.username, "is_premium": user.is_premium}
               
    
@router.post("/save_recipe/{user_id}")
def save_recipe(user_id: int, recipe: dict = Body(...), session: Session = Depends(get_session)):
    try:
        # Verifica se o usuário existe
        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            return {"status": "error", "message": "User not found"}

        # Cria uma nova receita associada ao usuário
        new_recipe = Recipe(content=recipe["recipe"], owner_id=user_id)
        session.add(new_recipe)
        session.commit()
        session.refresh(new_recipe)

        # Extrai o título da receita, se possível
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
    
@router.get("/get_user/{user_id}")
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        return {"status": "error", "message": "User not found"}
    return {"id": user.id, "username": user.username, "email": user.email, "is_premium": user.is_premium}

@router.get("/all_users")
def get_all_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users
    
@router.get("/saved_recipes/{user_id}")
def get_recipes(user_id:int, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        return {"status": "error", "message": "User not found"}
    return {"user": user.username, "recipes": user.recipes}