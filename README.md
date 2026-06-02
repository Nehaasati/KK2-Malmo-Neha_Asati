AI-Powered Amazon Reviews Analysis Service

Overview

This project is a complete AI-driven data analysis service built with 'FastAPI', 'Pandas', 'Pydantic', and a local language model (SmolLM2-135M-Instruct).

The application allows users to upload an Amazon Reviews dataset in CSV format, automatically computes descriptive statistics, and enables users to ask natural-language questions about the data through an AI interface.

The system uses a modular Runnable pipeline:

PromptBuilder -> LLMRunner -> ResponseParser


This pipeline:

1 Builds a structured prompt from the dataset statistics and user question.
2 Runs the local SmolLM model.
3 Extracts and cleans the final response before returning it to the user.

 Features

* Upload Amazon review datasets in CSV format
* Automatic dataset validation
* Statistical analysis using Pandas
* AI-powered question answering
* Runnable-based pipeline architecture
* Local LLM execution (no external API required)
* Comprehensive testing with pytest
* Modular and extensible design

Installation

 Clone the Repository
git clone https://github.com/your-username/amazon-review-ai.git
cd amazon-review-ai

 Install Dependencies

The project uses uv for dependency management.

uv sync
Running the Application
Start the FastAPI server:
uv run uvicorn app.main:app --reload
If a .venv directory exists, remove it first:
rm -rf .venv
uv sync
uv run uvicorn app.main:app --reload
The server will be available at:
http://127.0.0.1:8000
API Documentation
Swagger UI is automatically available at:
http://127.0.0.1:8000/docs

Usage

#1. Upload Dataset

Navigate to:
POST /data/upload
Upload an Amazon Reviews CSV file.
product,sentiment,rating,review_length
Laptop,positive,5,120
Phone,negative,1,45
Mouse,positive,4,80
Keyboard,positive,5,100
Headphones,negative,2,60
Monitor,positive,4,90
Example:
curl -X POST \
-F "file=@Amazon_reviews.csv" \
http://127.0.0.1:8000/data/upload
Example response:
json
{
  "rows": 50000,
  "columns": [
    "reviewText",
    "overall",
    "summary",
    "reviewTime"
  ]
}
2. Retrieve Dataset Statistics

Request:
curl http://127.0.0.1:8000/data/stats
Example response:
json
{
  "overall": {
    "count": 50000,
    "mean": 4.21,
    "std": 1.12,
    "min": 1,
    "25%": 4,
    "50%": 5,
    "75%": 5,
    "max": 5
  }
}
3. Ask AI Questions

Request:
bash
curl -X POST \
http://127.0.0.1:8000/ai/ask \
-H "Content-Type: application/json" \
-d '{"question":"What is the average review rating?"}'

Example response:
json
{
  "question": "What is the average review rating?",
  "answer": "The average review rating is approximately 4.21 stars.",
  "model": "SmolLM2-135M-Instruct"
}


 Runnable Pipeline Architecture
PromptBuilder

Responsibilities:

* Receives dataset statistics and user question.
* Creates a structured system prompt.
* Restricts the model to use only available statistics.

Example prompt:
You are a strict data analyst AI.

Use ONLY the provided dataset statistics.

If the answer cannot be determined from the data, respond:

"Not enough information."
 LLMRunner

Responsibilities:

* Loads and executes SmolLM locally.
* Uses lazy loading to reduce startup time.
* Can be mocked during testing.

Benefits:

* No external API dependency.
* Full local execution.
* Improved privacy.

ResponseParser

Responsibilities:

* Extracts the first meaningful answer.
* Removes unwanted prefixes.
* Cleans model output.

Example:

Input:
Answer:
The average rating is 4.21 stars.

Output:
The average rating is 4.21 stars.

Project Structure


app/
├── main.py                # FastAPI application
├── data.py                # Dataset handling and statistics
├── schemas.py             # Pydantic models

├── chain/
│   ├── runnable.py        # Runnable base classes
│   ├── steps.py           # PromptBuilder, LLMRunner, ResponseParser
│   └── pipeline.py        # Runnable chain definition

tests/
├── test_chain.py
├── test_endpoints.py
└── ...

Assumptions

* Users upload datasets through '/data/upload'.
* Datasets are stored only in memory.
* Files are never written to disk.
* Statistical analysis is performed using Pandas.
* The model only has access to computed statistics.
* The service is a prototype and not intended for processing sensitive personal data.
* LLM responses are treated as generated insights rather than absolute truth.


 Security Considerations

 File Upload Protection

The application:

* Accepts only '.csv' files.
* Rejects unreadable files.
* Processes files in memory only.
* Logs uploads for traceability.

Potential risks:

* Malformed CSV files.
* Large file uploads (DoS risk).
* Invalid formats.

Future improvements:

* File size restrictions.
* Content validation.
* Malware scanning.


Testing

Run all tests:
uv run pytest

Run endpoint tests:
uv run pytest tests/test_endpoints.py -v

Run chain tests:
uv run pytest tests/test_chain.py -v




 Design Decisions

Runnable Pattern

The Runnable architecture provides:

* Clear separation of concerns
* Strong typing with Pydantic
* Easy testing
* Modular extensibility
* Readable pipelines

Example:
oracle_chain = (
    PromptBuilder()
    | LLMRunner()
    | ResponseParser()

Pydantic provides:

* Validation
* Type safety
* Consistent data contracts
* Improved reliability

Lazy Model Loading

The model is loaded only when first needed.

Advantages:

* Faster application startup
* Reduced memory usage
* Faster test execution

 Limitations

Because the project uses a small language model (SmolLM2-135M-Instruct), limitations include:

* Occasional hallucinations
* Reduced reasoning capabilities
* Less accurate responses than larger models
* Potential bias inherited from training data

Therefore, generated answers should always be interpreted critically.

Future Improvements

* Multi-dataset support
* Persistent storage
* User authentication
* Dataset versioning
* Advanced analytics
* Enhanced prompt injection protection
* GDPR compliance features
* Larger language model support

 Conclusion

This project demonstrates how FastAPI, Pandas, Pydantic, Runnable pipelines, and SmolLM can be combined into a modular AI-powered data analysis system.

The architecture emphasizes:

* Clean separation of responsibilities
* Testability
* Security
* Maintainability
* Local AI inference

The result is a flexible and extensible platform that transforms raw Amazon review data into useful AI-assisted insights.

You can customize the repository URL, endpoint names, and dataset-specific column examples to exactly match your implementation.
