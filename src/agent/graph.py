"""Define a simple chatbot agent.

This agent returns a predefined response without using an actual LLM.
"""
import random
from typing import Any, Dict, Literal

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START, END

from agent.configuration import Configuration
from agent.state import State


async def my_custom_node_1(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Each node does work."""
    configuration = Configuration.from_runnable_config(config)
    # configuration = Configuration.from_runnable_config(config)
    # You can use runtime configuration to alter the behavior of your
    # graph.
    print("---Node 1---")
    return {"graph_state": state['graph_state'] +" I am"}
    # return {
    #     "changeme": "output from my_custom_node_1. "
    #     f"Configured with {configuration.my_configurable_param} + 'I am'"
    # }

async def my_custom_node_2(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Each node does work."""
    configuration = Configuration.from_runnable_config(config)
    # configuration = Configuration.from_runnable_config(config)
    # You can use runtime configuration to alter the behavior of your
    # graph.
    print("---Node 2---")
    return {"graph_state": state['graph_state'] +" happy!"}
    # return {
    #     "changeme": "output from my_custom_node_2. "
    #     f"Configured with {configuration.my_configurable_param} + 'happy!'"
    # }

async def my_custom_node_3(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Each node does work."""
    configuration = Configuration.from_runnable_config(config)
    # configuration = Configuration.from_runnable_config(config)
    # You can use runtime configuration to alter the behavior of your
    # graph.
    print("---Node 3---")
    return {"graph_state": state['graph_state'] +" sad!"}
    # return {
    #     "changeme": "output from my_custom_node_3. "
    #     f"Configured with {configuration.my_configurable_param}+ 'sad!'"
    # }

async def decide_mood(state) -> Literal["my_custom_node_2", "my_custom_node_3"]:
    # Often, we will use state to decide on the next node to visit
    user_input = state['graph_state'] 
    
    # Here, let's just do a 50 / 50 split between nodes 2, 3
    if random.random() < 0.5:

        # 50% of the time, we return Node 2
        return "my_custom_node_2"
    
    # 50% of the time, we return Node 3
    return "my_custom_node_3"


# Define a new graph
workflow = StateGraph(State, config_schema=Configuration)

# Add the node to the graph
workflow.add_node("my_custom_node_1", my_custom_node_1)
workflow.add_node("my_custom_node_2", my_custom_node_2)
workflow.add_node("my_custom_node_3", my_custom_node_3)

workflow.add_edge(START, "my_custom_node_1")
workflow.add_conditional_edges("my_custom_node_1", decide_mood)
workflow.add_edge("my_custom_node_2", END)
workflow.add_edge("my_custom_node_3", END)

# Compile the workflow into an executable graph
graph = workflow.compile()
graph.name = "Ronny's Graph"  # This defines the custom name in LangSmith
