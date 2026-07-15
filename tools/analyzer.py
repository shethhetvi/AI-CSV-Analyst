import pandas as pd
from langchain_core.tools import tool
from tools.security import validate_csv_path

@tool
def analyzer_tool(query: str, csv_path: str) -> str:
    """
    Analyzes a CSV file using pandas.
    Pass the path to the CSV and a query string describing what you want to know.
    Supported queries: "shape" (number of rows/cols), "columns" (list of columns), "head" (first few rows).
    """
    try:
        csv_path = validate_csv_path(csv_path)
        df = pd.read_csv(csv_path)
    except ValueError as e:
        return f"Security error: {e}"
    except Exception as e:
        return f"Error reading CSV: {e}"
        
    query = query.lower()
    
    if "shape" in query or "rows" in query:
        return f"The dataset has {df.shape[0]} rows and {df.shape[1]} columns."
    elif "column" in query:
        cols = ", ".join(df.columns.tolist())
        return f"The columns are: {cols}"
    elif "head" in query or "first" in query:
        return f"Here are the first few rows:\n{df.head().to_string()}"
    else:
        return "I am currently limited to answering questions about shape, columns, or showing the head."
