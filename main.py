from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from services.scrap import scrap_recipe

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajuste para restringir em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
@app.head("/", include_in_schema=False)
def read_root():
    return {"message": "Welcome to the CookAi API"}

@app.get("/scrap")
def extract_scrap_recipe_get(url: str = Query(...)):
    scrap_result = scrap_recipe(url)
    return scrap_result

@app.post("/scrap")
def extract_scrap_recipe(url: str = Query(...)):
    scrap_result = scrap_recipe(url)
    return scrap_result

if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
