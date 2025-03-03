from typing import TypedDict


class State(TypedDict):
    question: str
    answer: str


def graph_node(func, **wrapper_kwargs):
    async def wrapper(*args, **kwargs):
        result = func(*args, **kwargs, **wrapper_kwargs)

        # If it's an async generator
        if hasattr(result, "__aiter__"):
            async for item in result:
                # Stream each yielded value
                yield item
        else:
            # Yield final result
            yield await result

    return wrapper
