from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from services.scrap import scrap_recipe
import os

app = FastAPI()

port = int(os.environ.get("PORT", 8000))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)