uv init git init touch .gitignore

source .venv/Scripts/activate uv run main.py uv add transformers uv add "fastapi[standard]" from transformers import pipline

uv add "fastapi[standard]" pandas pydantic python-multipart pytest uv add torch

uv add pydantic

uv run fastapi dev app/main.py

uv add --dev pytest uv run pytest tests/test_endpoints.py -v







uvicorn app.main:app --reload   