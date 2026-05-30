from dotenv import load_dotenv
import os

load_dotenv()  # reads .env into environment variables

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3-8b-8192")
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB limit