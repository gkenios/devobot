from dataclasses import dataclass
import json
from typing import Any

from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.graph import StateGraph, START, END

from devobot.config import Config, llm


ROLE = "lead"  # In: "junior", "senior", "lead"
QUESTION = f"What is a Devoteam, {ROLE} role salary with 2 years of experience?"


@dataclass
class State:
    messages: list[BaseMessage]


def node_tool_call(state: State) -> State:
    if Config.use_llm:
        salary_tool = llm.bind_tools([calculate_devoteam_salary])
        new_message = salary_tool.invoke(state.messages)
    else:
        new_message = BaseMessage(
            content="",
            additional_kwargs={
                "tool_calls": [
                    {
                        "function": {
                            "name": "calculate_devoteam_salary",
                            "arguments": f'{{"role": "{ROLE}", "years_of_experience": 2}}',
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


def tool_salary(state: State) -> State:
    tool_call = state.messages[-1].additional_kwargs["tool_calls"][0]
    kwargs = json.loads(tool_call["function"]["arguments"])
    salary = calculate_devoteam_salary(**kwargs)
    state.messages.append(AIMessage(content=f"The salary is {salary}."))
    return state


def edge_tool_condition(state: State) -> str:
    if not state.messages[-1].content:
        return "salary_calculation"
    else:
        return END


def calculate_devoteam_salary(role: str, years_of_experience: int) -> int:
    """It calculates the salary of a Devoteam employee"""
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
                HumanMessage(QUESTION),
            ]
        )
    )
)
for message in result.messages:
    if message.content:
        print(message.content)
