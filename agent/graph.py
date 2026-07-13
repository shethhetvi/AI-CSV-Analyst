# pyrefly: ignore [missing-import]
from langgraph.graph import StateGraph, START, END
# pyrefly: ignore [missing-import]
from langgraph.prebuilt import ToolNode
from agent.state import AgentState
from agent.nodes import call_model, tools

# Create the graph
workflow = StateGraph(AgentState)

# Define the two nodes: the LLM and the tools
workflow.add_node("agent", call_model)
tool_node = ToolNode(tools)
workflow.add_node("tools", tool_node)

# Define the routing logic
def should_continue(state: AgentState):
    """Return the next node to execute."""
    messages = state["messages"]
    last_message = messages[-1]
    # If the LLM makes a tool call, then we route to the "tools" node
    if last_message.tool_calls:
        return "tools"
    # Otherwise, we stop (reply to the user)
    return END

# Build the graph edges
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, ["tools", END])
workflow.add_edge("tools", "agent")

# Compile it into a runnable app
app_graph = workflow.compile()
