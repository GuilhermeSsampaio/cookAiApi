
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
from docling.document_converter import DocumentConverter

load_dotenv()

converter = DocumentConverter()
llm = GoogleGenerativeAI(model="gemini-1.5-flash")

def scrap_recipe(url):
    """
    Scrape a recipe from the given URL and return its content.
    """
    try:
        result =converter.convert(url)
        docling_txt = result.document.export_to_markdown()
        
        print("Receita extraída com sucesso.")
        prompt = """
        Resuma essa receita, passando os ingredientes, tempo de forno e o modo de preparo:

        {text}
        Caso não tenha o tempo de forno indique o recomendado
        Traduza para o português
        """
        result = llm.invoke(prompt.format(text=docling_txt)).strip()
    
        return result
    except Exception as error:
        return {"error": f"Failed to scrape recipe from {url}: {error}"} 


# result = scrap_recipe("https://www.receitasnestle.com.br/receitas/bolo-de-cenoura-com-cobertura-de-brigadeiro")
# print(result)