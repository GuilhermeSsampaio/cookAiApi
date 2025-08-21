from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

import os

port = int(os.environ.get("PORT", 8000))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port)
