from pydantic import BaseModel


# This schema defines the structure of the request body for an API endpoint that accepts a question. The AskRequest model has a single field, 'question', which is a string. This model can be used to validate incoming requests to ensure they contain the expected data format.
class AskRequest(BaseModel):
    question: str


# These schemas define the structure of the data used in the application. PromptInput represents the input for generating a prompt, containing a question and associated statistics. PromptOutput represents the output of the prompt generation process, containing the generated prompt as a string. LLMOutput represents the raw text output from a language model, while ParsedAnswer represents a structured answer extracted from the raw text, containing just the answer as a string. These models can be used for data validation and serialization in API endpoints or other parts of the application that handle these types of data.
class PromptInput(BaseModel):
    question: str
    stats: dict

# The PromptOutput model represents the output of a prompt generation process, containing the generated prompt as a string. This model can be used to structure the response from an API endpoint that generates prompts based on input data.
class PromptOutput(BaseModel):
    prompt: str

# The LLMOutput model represents the raw text output from a language model.
class LLMOutput(BaseModel):
    raw_text: str


class ParsedAnswer(BaseModel):
    answer: str    