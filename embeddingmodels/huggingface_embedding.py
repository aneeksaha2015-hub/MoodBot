from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv
load_dotenv()

embeddings = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
)

texts = [
    "Hello this is Aneek",
    "Hello my love is MS"
]

vector = embeddings.embed_documents(texts)
print(vector)