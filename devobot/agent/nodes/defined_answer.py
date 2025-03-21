from devobot.agent import NodeInteraction, State


async def defined_answer(state: State, answer: str) -> NodeInteraction:
    question = state.input
    return NodeInteraction(input=question, output=answer)
