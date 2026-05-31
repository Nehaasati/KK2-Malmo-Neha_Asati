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

# To check LLM give give stats value from dataset such as mean medium if we not have say "no information "not predict  hallucinate
def test_prompt_contains_stat_values():
    builder = PromptBuilder()
    result = builder.invoke(PromptInput(
        question="Any question",
        stats={"rating": {"mean": 4.0, "max": 5.0}},
    ))
    assert "4.0" in result.prompt
    assert "5.0" in result.prompt

# check it promt used column name such as review
def test_prompt_contains_column_name():
    builder = PromptBuilder()
    result = builder.invoke(PromptInput(
        question="Any question",
        stats={"review_length": {"mean": 80.0, "count": 6.0}},
    ))
    assert "review_length" in result.prompt
# check Rewsponse parser work fine 

def  test_parser_plain_text():
    parser = ResponseParser()
    result = parser.invoke(LLMOutput(raw_text="The average rating is 4.0."))
    assert result.answer == "The average rating is 4.0."
# check pipeline is workig fine its does used fake :
def test_llm_runner_returns_correct_text():
    """
    When the model works correctly, LLMRunner must return
    the generated text inside LLMOutput.
    Uses a plain working function — no MagicMock needed.
    """
    def working_model(prompt, **kwargs):
        # Real HuggingFace pipeline returns a list of dicts
        return [{"generated_text": "The average rating is 4.0."}]

    LLMRunner.generator = working_model
    runner = LLMRunner()
    result = runner.invoke(PromptOutput(prompt="Test prompt"))

    assert isinstance(result, LLMOutput)
    assert result.raw_text == "The average rating is 4.0."

    LLMRunner.generator = None
