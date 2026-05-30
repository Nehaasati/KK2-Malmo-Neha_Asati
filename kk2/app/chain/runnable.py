from pydentic import Basemodel ,ConfigDict,SerilizerasAny
from typing import Generic, TypeVar, Any, Callable

# Type variable for INput output and inermidatevariable
I = TypeVar("I")
M = TypeVar("M")
O = TypeVar("o")

# A Runnable is a callable object that can be invoked with some input data to produce an output.
# A Runnable is caa object callable methord that can be invoked with some input data to produce an output
class Runnable(Basemodel,Generic[I,O]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str | None = None

# invoke methord must by implement by sub class to define how runnable methord process input data and produce output data
def invoke(self, data: I) -> O:
    raise NotImplementedError()

#The __ror__  methord is | pipline , this methord allow chaaining runnable togather in reverse order , if other object is callable , it wraps it  in a runnableLambda and runnablesequence with the current runnable as second part of sequense
def __ror__(self, other: Any):
        if callable(other):
            return RunnableSequence.model_construct(
                first=RunnableLambda.model_construct(func=other),
                second=self
            )

        return NotImplemented
# Runnablelambda is simple implementation of Runnable that wraps a callable function ,The invoke methord simpaly call the wrapped function with input data

class RunnableLambda(Runnable(I,O)):
    func : Callable[[I], O]

## The invoke method calls the wrapped function with the provided input data and returns the result.
def invoke(self, data: I) -> O:
        return self.func(data)

## RunnableSequence is an implementation of Runnable that represents a sequence of two Runnables. The invoke method first invokes the first Runnable with the input data, then takes the output and passes it to the second Runnable, returning the final output.
class RunnableSequence(Runnable[I, O], Generic[I, M, O]):
    first: SerializeAsAny[Runnable[I, M]]
    second: SerializeAsAny[Runnable[M, O]]

# The invoke method processes the input data through the first Runnable to get an intermediate result, which is then passed to the second Runnable to produce the final output.
    def invoke(self, data: I) -> O:
        return self.second.invoke(self.first.invoke(data))    