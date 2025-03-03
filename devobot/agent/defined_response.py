from ._common import State


async def defined_response(state: State, response: str) -> State:
    yield State(question=state["question"], answer=response)
