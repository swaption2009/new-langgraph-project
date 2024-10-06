"""Define a simple chatbot agent.

This agent returns a predefined response without using an actual LLM.
"""

from typing import Any, Dict

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START, END

from agent.configuration import Configuration
from agent.state import State


async def my_custom_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Each node does work."""
    configuration = Configuration.from_runnable_config(config)
    # configuration = Configuration.from_runnable_config(config)
    # You can use runtime configuration to alter the behavior of your
    # graph.
    return {
        "changeme": "output from my_custom_node. "
        f"Configured with {configuration.my_configurable_param}"
    }


# Define a new graph
workflow = StateGraph(State, config_schema=Configuration)

# Add the node to the graph
workflow.add_node("my_custom_node", my_custom_node)

# Set the entrypoint as `call_model`
workflow.add_edge(START, "my_custom_node")
workflow.add_edge("my_custom_node", END)

# Compile the workflow into an executable graph
graph = workflow.compile()
graph.name = "Ronny's Graph"  # This defines the custom name in LangSmith
