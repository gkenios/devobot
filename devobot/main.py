from dataclasses import dataclass
import json

from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.graph import StateGraph, START, END

from devobot.config import llm, USE_LLM


@dataclass
class Fake:
    content: str
    additional_kwargs: dict | None = None
    response_metadata: dict | None = None


@dataclass
class State:
    messages: list[BaseMessage]


def node_tool_call(state: State):
    if USE_LLM:
        new_message = llm.bind_tools([calculate_devoteam_salary]).invoke(state.messages)
    else:
        new_message = Fake(
            content="",
            additional_kwargs={
                "tool_calls": [
                    {
                        "function": {
                            "name": "calculate_devoteam_salary",
                            "arguments": '{"role": "junior", "years_of_experience": 2}',
                        }
                    }
                ]
            },
        )
    state.messages.append(
        AIMessage(
            content=new_message.content,
            additional_kwargs=new_message.additional_kwargs,
        )
    )
    return state


def tool_salary(state: State):
    kwargs = json.loads(
        state.messages[-1].additional_kwargs["tool_calls"][0]["function"]["arguments"]
    )
    salary = calculate_devoteam_salary(**kwargs)
    state.messages.append(AIMessage(content=f"The salary is {salary}."))
    return state


def edge_tool_condition(state: State):
    if not state.messages[-1].content:
        return "salary_calculation"
    else:
        return END


def calculate_devoteam_salary(role: str, years_of_experience: int) -> int:
    """It calculates the salary of a Devoteam employee based on their role and years of experience."""
    if role == "junior":
        return 30000 + years_of_experience * 1000
    elif role == "senior":
        return 40000 + years_of_experience * 2000
    elif role == "lead":
        return 50000 + years_of_experience * 3000
    else:
        return 0


builder = StateGraph(State)
# Nodes
builder.add_node("tool_call", node_tool_call)
builder.add_node("salary_calculation", tool_salary)
# Edges
builder.add_edge(START, "tool_call")
builder.add_conditional_edges("tool_call", edge_tool_condition)
builder.add_edge("salary_calculation", END)

result = State(
    **builder.compile().invoke(
        State(
            messages=[
                HumanMessage(
                    "What is the salary of a Devoteam junior with 2 years of experience?"
                )
            ]
        )
    )
)
for message in result.messages:
    if message.content:
        print(message.content)