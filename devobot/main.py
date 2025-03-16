import asyncio

from langgraph.graph.state import CompiledStateGraph

from devobot.agent import State
from devobot.init.create_graph import graph


QUESTION = "What time can I park my car in the Devoteam office?"


async def main(state: State, graph: CompiledStateGraph) -> None:
    async for msg, _ in graph.astream(input=state, stream_mode="messages"):
        if msg.content:  # type: ignore
            print(msg.content, end="", flush=True)  # type: ignore
            await asyncio.sleep(0.05)


if __name__ == "__main__":
    state = State(input=QUESTION, lineage=[])
    asyncio.run(main(state, graph))
