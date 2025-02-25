import asyncio
import time

from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

from devobot.agent import State, graph_node, rag
from devobot.config import Config, embeddings, llm
from devobot.services.database_vector import ChromaVectorDB


QUESTION = "What time can I park my car in the Devoteam office?"


wrapped_rag = graph_node(
    rag,
    vector_db=ChromaVectorDB(collection_name="faq", embeddings=embeddings),
    llm=llm,
    prompt=Config.config["agent"]["rag"]["prompt"],
)


async def main(graph: CompiledStateGraph):
    async for msg, _ in graph.astream(
        input={"question": QUESTION},
        stream_mode="messages",
    ):
        if msg.content:
            print(msg.content, end="", flush=True)
            time.sleep(0.1)


if __name__ == "__main__":
    builder = StateGraph(State)
    # Nodes
    builder.add_node(node="rag", action=wrapped_rag)
    # Edges
    builder.add_edge(START, "rag")
    builder.add_edge("rag", END)

    graph = builder.compile()
    asyncio.run(main(graph))
