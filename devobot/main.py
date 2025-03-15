import asyncio

from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

from devobot.agent import State
from init.create_agent import AgentNode


QUESTION = "What time can I park my car in the Devoteam office?"


async def main(graph: CompiledStateGraph):
    async for msg, _ in graph.astream(
        input=State(lineage=[], input=QUESTION),
        stream_mode="messages",
    ):
        if msg.content:
            print(msg.content, end="", flush=True)
            await asyncio.sleep(0.05)


if __name__ == "__main__":
    builder = StateGraph(State)

    # Test One
    builder.add_node(node="intent", action=getattr(AgentNode, "intent"))
    builder.add_edge(START, "intent")
    builder.add_edge("intent", END)

    # Test Two
    # builder.add_node(node="faq", action=getattr(AgentNode, "faq"))
    # builder.add_edge(START, "faq")
    # builder.add_edge("faq", END)

    graph = builder.compile()
    asyncio.run(main(graph))
