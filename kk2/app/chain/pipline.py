from app.chain.step import (
    PromptBuilder,
    LLMRunner,
    ResponseParser
)

# The oracle_chain is a sequential processing chain that combines the PromptBuilder, LLMRunner, and ResponseParser. 
# This chain takes an input, processes it through each step in order, and produces a final output. 
# The PromptBuilder constructs a prompt based on according to  dataset  and user question, the LLMRunner generates a response using the language model, and the ResponseParser extracts a clean answer from the generated text. 


oracle_chain = (
    PromptBuilder()
    | LLMRunner()
    | ResponseParser()
)