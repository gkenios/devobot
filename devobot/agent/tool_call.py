from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import BaseTool
from langchain_core.prompts import PromptTemplate
from langchain.chains.base import Chain
from langchain_core.messages import HumanMessage, ToolMessage

from .common import NodeInteraction, State
import devobot.agent.tools as custom_tools


DEFAULT_PROMPT = """Answer the following question using the available tools.

Question: {question}
"""


def tool_call(
    state: State,
    llm: BaseChatModel,
    # Config parameters
    tools: list[BaseTool],
    prompt: str = DEFAULT_PROMPT,
) -> NodeInteraction:
    # Get the question from the state
    question = state.input
    messages = [HumanMessage(question)]

    # Create the chain
    prompt = PromptTemplate(input_variables=["question"], template=prompt)
    llm_with_tools = llm.bind_tools(tools)
    chain: Chain = prompt | llm_with_tools

    # Invoke the chain
    result = chain.invoke(messages)
    messages.append(result)

    # Invoke the tools
    for tool_config in result.tool_calls:
        func = getattr(custom_tools, tool_config["name"])
        result = func.invoke(tool_config["args"])
        messages.append(ToolMessage(result, tool_call_id=tool_config["id"]))

    return llm_with_tools.invoke(messages).content
