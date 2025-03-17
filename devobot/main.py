import asyncio

from langgraph.graph.state import CompiledStateGraph

from devobot.agent import State
from devobot.init.create_graph import graph


QUESTION = "How much does an ice cream cost in Greece?"
USER_EMAIL = "georgios.gkenios@devoteam.com"


async def main(state: State, graph: CompiledStateGraph) -> None:
    async for msg, _ in graph.astream(input=state, stream_mode="messages"):
        if msg.content:  # type: ignore
            print(msg.content, end="", flush=True)  # type: ignore
            await asyncio.sleep(0.05)


if __name__ == "__main__":
    state = State(input=QUESTION, user_email=USER_EMAIL, lineage=[])
    asyncio.run(main(state, graph))
