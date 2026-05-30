from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3-8b-8192")
MAX_FILE_SIZE = 5 * 1024 * 1024

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing in .env file")