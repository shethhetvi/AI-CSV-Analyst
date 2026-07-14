import os
# pyrefly: ignore [missing-import]
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage
from tools.analyzer import analyzer_tool
from tools.charts import chart_tool
from tools.statistics import statistics_tool

# Initialize the local Ollama model (runs locally, no API key required)
llm = ChatOllama(model="qwen2.5:7b", temperature=0)

# Bind all tools to the LLM
tools = [analyzer_tool, chart_tool, statistics_tool]
llm_with_tools = llm.bind_tools(tools)

def call_model(state):
    """
    Calls the LLM. It looks at the messages and decides whether
    to reply directly or use a tool.
    """
    messages = state["messages"]
    csv_path = state.get("csv_file_path", "No file uploaded")
    
    # Give the agent full context about available tools
    system_prompt = SystemMessage(
        content=(
            f"You are an AI CSV Analyst. You help users explore and understand their data.\n"
            f"The current dataset is located at: {csv_path}\n\n"
            f"You have access to three tools:\n"
            f"1. analyzer_tool  — Use for basic queries: shape, columns, or showing the first few rows.\n"
            f"2. chart_tool     — Use to generate charts. Supported chart_type values: histogram, bar, pie, scatter, line.\n"
            f"3. statistics_tool — Use for statistical analysis: describe, missing, duplicates, correlation, dtypes, unique, value_counts:<col>.\n\n"
            f"Always use a tool when the user asks about the data. Never make up numbers."
        )
    )
    
    response = llm_with_tools.invoke([system_prompt] + messages)
    
    return {"messages": [response]}
