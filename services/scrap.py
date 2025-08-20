from dotenv import load_dotenv
from docling.document_converter import DocumentConverter
from google import genai
import os

load_dotenv()

converter = DocumentConverter()

# Configure a API do Gemini
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def scrap_recipe(url):
    """
    Scrape a recipe from the given URL and return its content.
    """
    try:
        result = converter.convert(url)
        docling_txt = result.document.export_to_markdown()
        
        print("Receita extraída com sucesso.")
        prompt = f"""
        Resuma essa receita, passando os ingredientes, tempo de forno e o modo de preparo:

        {docling_txt}
        Caso não tenha o tempo de forno indique o recomendado.
        Traduza para o português.
        """
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as error:
        return {"error": f"Failed to scrape recipe from {url}: {error}"} 

# result = scrap_recipe("https://www.receitasnestle.com.br/receitas/bolo-de-cenoura-com-cobertura-de-brigadeiro")
# print(result)