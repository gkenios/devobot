from langgraph.graph import StateGraph, START, END

from devobot.agent import State, graph_node, rag
from devobot.config import Config, embeddings, llm
from devobot.services.database_vector import ChromaVectorDB


QUESTION = "What time can I park my car in the Devoteam office?"


def other(state: State):
    return State(question=state["question"], answer="Hello")


builder = StateGraph(State)
# Nodes
builder.add_node(
    node="rag",
    action=graph_node(
        rag,
        vector_db=ChromaVectorDB(collection_name="faq", embeddings=embeddings),
        llm=llm,
        prompt=Config.config["agent"]["rag"]["prompt"],
    ),
)
# builder.add_node("rag", other)
# Edges
builder.add_edge(START, "rag")
builder.add_edge("rag", END)

graph = builder.compile()
response = graph.invoke({"question": QUESTION})
print(response)
