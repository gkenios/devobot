from langchain.chains.base import Chain
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.prompts import PromptTemplate

from devobot.agent import (
    NodeInteraction,
    NodeOutputType,
    State,
    format_prompt_with_context,
)
from devobot.agent import tools as custom_tools


DEFAULT_PROMPT = """Answer the following question using the available tools.
For context, today's date is {today}, {weekday}, and the current time is {time}.

Question: {question}
"""


async def tool_call(
    state: State,
    llm: BaseChatModel,
    # Config parameters
    tools: list[str],
    tools_params: dict[str, dict[str, str | int | float]] | None = None,
    prompt: str = DEFAULT_PROMPT,
) -> NodeOutputType:
    # Get the question from the state
    question = state.input
    prompt = format_prompt_with_context(prompt)
    messages = [HumanMessage(question)]

    # Get the tools
    tool_funcs = []
    for tool_name in tools:
        if hasattr(custom_tools, tool_name):
            tool_funcs.append(getattr(custom_tools, tool_name))
        else:
            raise AttributeError(
                f"Tool '{tool_name}' not found in the agent/tools directory."
            )

    # Create the chain
    prompt = PromptTemplate(input_variables=["question"], template=prompt)
    llm_with_tools = llm.bind_tools(tool_funcs)
    chain: Chain = prompt | llm_with_tools

    # Invoke the chain
    result = chain.invoke(messages)
    messages.append(result)

    # Invoke the tools
    for tool_config in result.tool_calls:
        tool_name = tool_config["name"]
        args = tool_config["args"]

        extra_args = tools_params.get(tool_name, {})
        args.update(extra_args)
        args.update(state.__dict__)

        func = getattr(custom_tools, tool_name)
        result = func.invoke(args)
        messages.append(ToolMessage(result, tool_call_id=tool_config["id"]))

    response = ""
    async for chunk in llm_with_tools.astream(messages):
        # Yield each chunk as it arrives
        yield NodeInteraction(input=question, output=chunk.content)  # type: ignore
        response += chunk.content  # type: ignore

    # Yield final response
    yield NodeInteraction(input=question, output=response)
