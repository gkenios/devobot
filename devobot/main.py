import asyncio

from langgraph.graph.state import CompiledStateGraph

from devobot.agent import State
from devobot.config import STEP_SYMBOL
from devobot.init.create_graph import graph
from devobot.init.create_nodes import end_nodes


QUESTION = "What time can I park my car?"
USER_EMAIL = "georgios.gkenios@devoteam.com"


async def main(state: State, graph: CompiledStateGraph) -> None:
    last_answer_is_streaming = False

    async for update, message in graph.astream(
        input=state, stream_mode=["updates", "messages"]
    ):
        # If it is a streaming message and part of the end nodes
        if (
            update == "messages"
            and message[1].get("langgraph_node") in end_nodes
        ):
            print(message[0].content, end="", flush=True)
            await asyncio.sleep(0.025)
            last_answer_is_streaming = True

        # At the end of each node, print the output
        if update == "updates":
            node_name = next(iter(message))
            # Print the steps
            if node_name not in end_nodes:
                step_output = message[node_name]["lineage"][-1]["step_output"]
                if step_output:
                    print(f"{STEP_SYMBOL} {step_output}")
            # Print the final message if it is not streaming
            elif not last_answer_is_streaming:
                print(message[node_name]["output"])


if __name__ == "__main__":
    state = State(input=QUESTION, user_email=USER_EMAIL, lineage=[])
    asyncio.run(main(state, graph))
