from app.chain.step import PromptBuilder, ResponseParser, LLMRunner
from app.chain.runnable import Runnable
from app.schemas import PromptInput, LLMOutput, PromptOutput
from unittest.mock import patch
from app.chain.pipeline import oracle_chain 

# PROMPTBUILDER TESTS
# We test PromptBuilder in total isolation — no LLM, no API call.
# We give it known input and check the output string contains
# exactly what we expect

def test_prompt_contains_question():
    """
    The question must appear in the prompt.
    If it doesn't, the LLM will answer the wrong question.
    """
    builder = PromptBuilder()

    result = builder.invoke(PromptInput(
        question="What is the average rating?",
        stats={"rating": {"mean": 4.0, "max": 5.0, "min": 1.0}},
    ))

    # The question must be somewhere in the built prompt
    assert "What is the average rating?" in result.prompt