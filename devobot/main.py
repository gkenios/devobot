import asyncio

from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

from devobot.agent import State
from devobot.config import AgentNode


QUESTION = "What time can I park my car in the Devoteam office?"


async def main(graph: CompiledStateGraph):
    async for msg, _ in graph.astream(
        input=State(question=QUESTION),
        stream_mode="messages",
    ):
        if msg.content:
            print(msg.content, end="", flush=True)
            await asyncio.sleep(0.1)


if __name__ == "__main__":
    builder = StateGraph(State)
    # Nodes
    builder.add_node(node="classify", action=getattr(AgentNode, "classify"))
    builder.add_node(node="rag", action=getattr(AgentNode, "rag"))
    # Edges
    builder.add_edge(START, "classify")
    builder.add_conditional_edges("classify_condition", lambda x: x[""])
    builder.add_edge("rag", END)

    graph = builder.compile()
    asyncio.run(main(graph))
