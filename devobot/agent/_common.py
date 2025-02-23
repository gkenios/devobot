from typing import TypedDict


class State(TypedDict):
    question: str
    answer: str


def graph_node(func, **wrapper_kwargs):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs, **wrapper_kwargs)

    return wrapper
