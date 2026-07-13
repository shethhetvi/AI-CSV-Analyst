import streamlit as st
import pandas as pd
from tools.csv_loader import save_and_load_csv

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
        df = save_and_load_csv(uploaded_file)
        st.session_state["df"] = df
        st.session_state["file_path"] = f"uploads/{uploaded_file.name}"
        
        st.success("File uploaded successfully!")
        st.subheader("Data Preview")
        st.dataframe(df.head(10))
        st.caption(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    except Exception as e:
        st.error(f"Error loading file: {e}")
else:
    st.info("Please upload a CSV file in the sidebar to get started.")
