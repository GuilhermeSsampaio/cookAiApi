from urllib import response
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents="What is the capital of France?")

print(response.text)