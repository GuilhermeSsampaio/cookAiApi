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

@app.post("/scrap")
def extract_scrap_recipe(url: str):
    scrap_result = scrap_recipe(url)
    return scrap_result

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)