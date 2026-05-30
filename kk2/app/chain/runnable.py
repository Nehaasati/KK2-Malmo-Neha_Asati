from pydantic import BaseModel, ConfigDict, SerializeAsAny
from typing import Generic, TypeVar, Any, Callable

# Type variables for input, output, and intermediate types
I = TypeVar("I")
O = TypeVar("O")
M = TypeVar("M")


# A Runnable is a callable object that can be invoked with some input data to produce an output.
class Runnable(BaseModel, Generic[I, O]):
    """
    Base class for all processing steps in the chain.
    Each Runnable transforms input of type I into output of type O.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str | None = None

# The invoke method must be implemented by subclasses to define how the Runnable processes input data to produce output.
    def invoke(self, data: I) -> O:
        raise NotImplementedError("Subclasses must implement invoke().")

# The __or__ method allows chaining Runnables together using the | operator. 
# If the other object is a Runnable, it creates a RunnableSequence. 
# If the other object is a callable, it wraps it in a RunnableLambda and then creates a RunnableSequence.
    def __or__(self, other: Any) -> 'RunnableSequence':
        """
        Allows chaining: step1 | step2
        """
        if isinstance(other, Runnable):
            return RunnableSequence.model_construct(first=self, second=other)

        if callable(other):
            wrapped = RunnableLambda.model_construct(
                func=other,
                name=getattr(other, "_name_", None)
            )
            return RunnableSequence.model_construct(first=self, second=wrapped)
        return NotImplemented

# The __ror__ method allows chaining Runnables together in reverse order using the | operator. 
# If the other object is a callable, it wraps it in a RunnableLambda and then creates a RunnableSequence with the current Runnable as the second part of the sequence.
    def __ror__(self, other: Any) -> Any :
        """
        Allows chaining in reverse order: func | step
        """
        if callable(other):
            wrapped = RunnableLambda.model_construct(
                func=other,
                name=getattr(other, "_name_", None)
            )
            return RunnableSequence.model_construct(first=wrapped, second=self)

        return NotImplemented

# RunnableLambda is a simple implementation of Runnable that wraps a callable function. 
# The invoke method simply calls the wrapped function with the input data.
class RunnableLambda(Runnable[I, O]):
    """
    Wraps a simple Python function into a Runnable.
    """
    func: Callable[[I], O]

# The invoke method calls the wrapped function with the provided input data and returns the result.
    def invoke(self, data: I) -> O:
        return self.func(data)

# RunnableSequence is an implementation of Runnable that represents a sequence of two Runnables. 
# The invoke method first invokes the first Runnable with the input data, then takes the output and passes it to the second Runnable, returning the final output.
class RunnableSequence(Runnable[I, O], Generic[I, M, O]):
    """
    Represents a chain of two Runnables: first -> second.
    """
    first: SerializeAsAny[Runnable[I, M]]
    second: SerializeAsAny[Runnable[M, O]]

    # improved type annotations for invoke method
    def invoke(self, data: I) -> O:
        intermediate = self.first.invoke(data)
        return self.second.invoke(intermediate)