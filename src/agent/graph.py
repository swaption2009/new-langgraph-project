"""Define a custom Reasoning and Action agent.

Works with a chat model with tool calling support.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List

import anthropic
from agent.configuration import Configuration
from agent.state import State
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph

# Define the function that calls the model


async def call_model(
    state: State, config: RunnableConfig
) -> Dict[str, List[Dict[str, Any]]]:
    """Call the LLM powering our "agent".

    This function prepares the prompt, initializes the model, and processes the response.

    Args:
        state (State): The current state of the conversation.
        config (RunnableConfig): Configuration for the model run.

    Returns:
        dict: A dictionary containing the model's response message.
    """
    configuration = Configuration.from_runnable_config(config)
    system_prompt = configuration.system_prompt.format(
        system_time=datetime.now(tz=timezone.utc).isoformat()
    )
    toks = []
    async with anthropic.AsyncAnthropic() as client:
        async with client.messages.stream(
            model=configuration.model_name,
            max_tokens=1024,
            system=system_prompt,
            messages=state.messages,
        ) as stream:
            async for text in stream.text_stream:
                toks.append(text)

    # Return the model's response as a list to be added to existing messages
    return {
        "messages": [
            {"role": "assistant", "content": [{"type": "text", "text": "".join(toks)}]}
        ]
    }


# Define a new graph

workflow = StateGraph(State, config_schema=Configuration)

# Define the two nodes we will cycle between
workflow.add_node(call_model)

# Set the entrypoint as `call_model`
# This means that this node is the first one called
workflow.add_edge("__start__", "call_model")


# Compile the workflow into an executable graph
# You can customize this by adding interrupt points for state updates
graph = workflow.compile(
    interrupt_before=[],  # Add node names here to update state before they're called
    interrupt_after=[],  # Add node names here to update state after they're called
)
graph.name = "My New Graph"  # This defines the custom name in LangSmith
