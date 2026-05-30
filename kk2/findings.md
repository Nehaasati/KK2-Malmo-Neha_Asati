uv init git init touch .gitignore

source .venv/Scripts/activate uv run main.py uv add transformers uv add "fastapi[standard]" from transformers import pipline

uv add "fastapi[standard]" pandas pydantic python-multipart pytest uv add torch

uv add pydantic

uv run fastapi dev app/main.py

uv add --dev pytest uv run pytest tests/test_endpoints.py -v
Question
   ↓
PromptBuilder
   ↓
SmolLM
   ↓
ResponseParser
   ↓
JSON Answer






uvicorn app.main:app --reload   

"What is the average rating?""question": "What is sentiment of headphon?"
"What trends can you identify?""What is the highest rating?""Summarize overall satisfaction""How many products are in the dataset?""What insights can you draw?""What is the minimum review length?""Analyze customer behavior""What is the most common sentiment?