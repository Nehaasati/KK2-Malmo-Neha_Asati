from transformers import pipeline
from app.chain.runnable import Runnable
from app.schemas import (
    PromptInput,
    PromptOutput,
    LLMOutput,
    ParsedAnswer,
)
from typing import ClassVar

# The PromptBuilder class is a specific implementation of the Runnable interface that takes a PromptInput and produces a PromptOutput. The invoke method constructs a prompt string based on the provided dataset statistics and user question, following a specific format that instructs the AI to use only the provided data to answer the question. If the answer cannot be determined from the data, it instructs the AI to respond with "Not enough information." The generated prompt is then returned as a PromptOutput object.
class PromptBuilder(Runnable[PromptInput, PromptOutput]):

    def invoke(self, data: PromptInput) -> PromptOutput:

        # Format stats into clean readable lines
        formatted_stats = ""
        for column, values in data.stats.items():
            formatted_stats += f"\nColumn: {column}\n"
            for key, value in values.items():
                if value != "":  # skip empty cells
                    formatted_stats += f"  {key}: {value}\n"

        # Better prompt — simpler instruction, clear answer format
        prompt = f"""You are a data analyst. Use ONLY the statistics below.

Dataset statistics:
{formatted_stats}

Question: {data.question}

Give a short direct answer in 1 sentence. Start with the answer immediately."""

        return PromptOutput(prompt=prompt.strip())

# The invoke method constructs a prompt string using the provided dataset statistics and user question. It follows a specific format that instructs the AI to use only the provided data to answer the question, and to respond with "Not enough information." if the answer cannot be determined from the data. The generated prompt is returned as a PromptOutput object.
    
# The prompt string is constructed using a multi-line f-string that incorporates the dataset statistics and user question from the PromptInput. The prompt instructs the AI to be a strict data analyst, to use only the provided dataset statistics, and to answer briefly and clearly. If the answer cannot be determined from the data, it explicitly tells the AI to respond with "Not enough information."
        
# The generated prompt is returned as a PromptOutput object, which can be used in subsequent steps of the processing chain, such as sending it to a language model for generating an answer.
    
# The LLMRunner class is another implementation of the Runnable interface that takes a PromptOutput and produces an LLMOutput. The invoke method uses the previously defined text generation pipeline to generate a response based on the prompt contained in the PromptOutput. The generated text is extracted from the result and returned as an LLMOutput object.
class LLMRunner(Runnable[PromptOutput, LLMOutput]):
    generator: ClassVar = None

    def _load_generator(self):
        """Lazy load the Hugging Face model only when needed"""
        if LLMRunner.generator is None:
            LLMRunner.generator = pipeline(
                "text-generation",
                model="HuggingFaceTB/SmolLM2-135M-Instruct"
            )

    def invoke(self, data: PromptOutput) -> LLMOutput:

        # The invoke method attempts to generate a response using the text generation pipeline. 
        # It calls the generator with the prompt from the PromptOutput, specifying a maximum of 250 new tokens and enabling truncation. 
        # The generated text is extracted from the result, and only the portion of the text that was generated (excluding the original prompt) is returned as an LLMOutput object. 
        # If any exceptions occur during this process, an LLMOutput containing an error message is returned instead.
        try:
            self._load_generator()

            result = LLMRunner.generator(
                data.prompt,
                max_new_tokens=250,
                return_full_text=False, # Only return the generated text, not the original prompt.
                truncation=True
            )

            generated_text = result[0]["generated_text"].strip()

            return LLMOutput(raw_text=generated_text)
        
        except Exception as e:

            return LLMOutput(
                raw_text=f"Model error: {str(e)}"
            )
    
# The ResponseParser class is a simple implementation of the Runnable interface that takes an LLMOutput and produces a ParsedAnswer. 

class ResponseParser(Runnable[LLMOutput, ParsedAnswer]):

    def invoke(self, data: LLMOutput) -> ParsedAnswer:

        text = data.raw_text.strip()

        # Remove empty lines
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        if not lines:
            return ParsedAnswer(answer="No answer generated.")

        # Take first meaningful line
        answer = lines[0]

        # ✓ FIX: break after first prefix match — don't loop all prefixes
        prefixes = ["Answer:", "A:", "Response:", "Result:", "-", "*"]
        for prefix in prefixes:
            if answer.lower().startswith(prefix.lower()):
                answer = answer[len(prefix):].strip()
                break  # ← THIS WAS MISSING — caused "Dataset statistics:" bug

        # ✓ FIX: quote removal is OUTSIDE the for loop now
        if answer.startswith('"') and answer.endswith('"'):
            answer = answer[1:-1].strip()

        # Collapse spaces
        answer = " ".join(answer.split())

        if not answer:
            answer = "No answer generated."

        return ParsedAnswer(answer=answer)