from pydantic import BaseModel


# This schema defines the structure of the request body for an API endpoint that accepts a question. The AskRequest model has a single field, 'question', which is a string. This model can be used to validate incoming requests to ensure they contain the expected data format.
class AskRequest(BaseModel):
    question: str