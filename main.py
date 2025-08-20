from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from services.scrap import scrap_recipe
 
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the CookAi API"}

@app.post("/scrap")
def extract_scrap_recipe(url: str):
    scrap_result = scrap_recipe(url)
    return scrap_result

