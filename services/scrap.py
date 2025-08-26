import time
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from google import genai
import os

load_dotenv()

# Configure a API do Gemini
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def scrap_recipe(url):
    """
    Scrape a recipe from the given URL and return its content.
    """
    start_time = time.time()
    print(f"Starting to scrape the recipe from {url}...")
    
    try:
        # Faz a requisição HTTP
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove tags de script e style
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Extrai o texto
        text = soup.get_text(separator='\n', strip=True)
        
        conversion_time = time.time() - start_time
        print(f"Tempo de conversão: {conversion_time:.2f} segundos")

        prompt = f"""
        Resuma essa receita, passando os ingredientes, tempo de forno e o modo de preparo:

        {text}
        Caso não tenha o tempo de forno indique o recomendado.
        Traduza para o português.
        """
        
        model_start_time = time.time()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        model_time = time.time() - model_start_time
        print(f"Tempo de processamento do modelo: {model_time:.2f} segundos")
        
        total_time = time.time() - start_time
        print(f"Tempo total de execução: {total_time:.2f} segundos")
        return response.text
        
    except Exception as error:
        return {"error": f"Failed to scrape recipe from {url}: {error}"}