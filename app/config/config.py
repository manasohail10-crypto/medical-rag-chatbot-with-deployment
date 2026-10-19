import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DB_FAISS_PATH='vectorstore/db_faiss'
DATA_PATH='data/'
EMBEDDING_MODEL_NAME = "abhinand/MedEmbed-base-v0.1"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
LLM_MODEL_NAME = "openai/gpt-oss-120b"