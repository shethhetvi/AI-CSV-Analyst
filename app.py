import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from tools.charts import CHART_PREFIX
from tools.security import sanitize_user_input, MAX_QUERIES_PER_SESSION, validate_csv_path

# Load environment variables (like GOOGLE_API_KEY)
load_dotenv()

# --- Security: startup environment check ---
_GOOGLE_KEY = os.getenv("GOOGLE_API_KEY", "")
if not _GOOGLE_KEY or _GOOGLE_KEY.strip() == "":
    st.warning(
        "⚠️ **GOOGLE_API_KEY** is not set. "
        "Some features may not work. Add it to your `.env` file and restart the app."
    )

from tools.csv_loader import save_and_load_csv
from agent.graph import app_graph
from langchain_core.messages import HumanMessage, AIMessage

st.set_page_config(page_title="AI CSV Analyst", page_icon="📊", layout="wide")

st.title("📊 AI CSV Analyst")
st.markdown("Upload a CSV file and let the AI agent analyze it for you!")

# Sidebar for file upload
with st.sidebar:
    st.header("1. Upload Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load and show the dataframe
    try:
        if "df" not in st.session_state:
            df, file_path, load_warnings = save_and_load_csv(uploaded_file)
            st.session_state["df"] = df
            st.session_state["file_path"] = file_path
            for w in load_warnings:
                st.warning(w)
            
        st.success("File uploaded successfully!")
        with st.expander("Preview Data"):
            st.dataframe(st.session_state["df"].head(10))
            st.caption(f"Shape: {st.session_state['df'].shape[0]} rows, {st.session_state['df'].shape[1]} columns")
            
    except Exception as e:
        st.error(f"Error loading file: {e}")
        
    st.divider()
    st.header("2. Ask the Agent")
    
    # Initialize chat history and query counter
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "query_count" not in st.session_state:
        st.session_state["query_count"] = 0

    # Show rate-limit progress in sidebar
    with st.sidebar:
        remaining = MAX_QUERIES_PER_SESSION - st.session_state["query_count"]
        st.caption(f"🔒 Queries used: {st.session_state['query_count']} / {MAX_QUERIES_PER_SESSION}")
        st.progress(st.session_state["query_count"] / MAX_QUERIES_PER_SESSION)
        
    # Display chat messages from history
    for msg in st.session_state["messages"]:
        if isinstance(msg, HumanMessage):
            st.chat_message("user").write(msg.content)
        elif isinstance(msg, AIMessage) and msg.content:
            with st.chat_message("assistant"):
                if CHART_PREFIX in msg.content:
                    chart_path = msg.content.split(CHART_PREFIX, 1)[-1].strip()
                    # --- Security: validate chart path before rendering ---
                    try:
                        safe_chart_path = validate_csv_path(chart_path.replace(".png", ".csv")).replace(".csv", ".png")
                        st.image(chart_path, use_container_width=True)
                    except ValueError:
                        st.warning("⚠️ Chart could not be displayed: invalid path.")
                else:
                    st.write(msg.content)
            
    # Chat input
    if st.session_state["query_count"] >= MAX_QUERIES_PER_SESSION:
        st.error(
            f"🚫 You've reached the session limit of {MAX_QUERIES_PER_SESSION} queries. "
            "Please refresh the page to start a new session."
        )
    elif prompt := st.chat_input("Ask me about your data (e.g., 'What are the columns?')..."):
        # --- Security: sanitize user input before sending to LLM ---
        clean_prompt, input_warnings = sanitize_user_input(prompt)
        for w in input_warnings:
            st.warning(w)

        st.chat_message("user").write(clean_prompt)
        st.session_state["messages"].append(HumanMessage(content=clean_prompt))
        
        # Call the LangGraph agent
        with st.spinner("Agent is analyzing..."):
            inputs = {
                "messages": st.session_state["messages"],
                "csv_file_path": st.session_state["file_path"]
            }
            
            final_state = app_graph.invoke(inputs)
            
            # Update our session state with the new messages
            st.session_state["messages"] = final_state["messages"]
            st.session_state["query_count"] += 1  # Track against rate limit
            
            # Display the latest AI message
            latest_ai_msg = final_state["messages"][-1]
            with st.chat_message("assistant"):
                if latest_ai_msg.content and CHART_PREFIX in latest_ai_msg.content:
                    chart_path = latest_ai_msg.content.split(CHART_PREFIX, 1)[-1].strip()
                    # --- Security: validate chart path is inside uploads/ ---
                    try:
                        # Chart paths end in .png; swap extension for validate_csv_path trick
                        uploads_dir = os.path.realpath("uploads")
                        resolved_chart = os.path.realpath(chart_path)
                        if resolved_chart.startswith(uploads_dir + os.sep):
                            st.image(chart_path, use_container_width=True)
                        else:
                            st.warning("⚠️ Chart path is outside allowed directory and was blocked.")
                    except Exception:
                        st.warning("⚠️ Could not verify chart path.")
                elif latest_ai_msg.content:
                    st.write(latest_ai_msg.content)
else:
    st.info("Please upload a CSV file in the sidebar to get started.")
