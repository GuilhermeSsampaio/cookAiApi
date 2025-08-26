from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
from database.db import init_db, engine
from sqlmodel import Session
from routes.recipes import router as recipes_router
import uvicorn

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

# Inclui as rotas de receitas
app.include_router(recipes_router, dependencies=[Depends(get_session)])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)