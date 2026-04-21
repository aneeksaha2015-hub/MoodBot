from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

result = client.models.embed_content(
    model="gemini-embedding-001",
    contents="You are going to learn Gen AI"
)

vector = result.embeddings[0].values
print(vector[:5])