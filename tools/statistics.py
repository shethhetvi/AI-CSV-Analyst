import pandas as pd
from langchain_core.tools import tool
from tools.security import validate_csv_path


@tool
def statistics_tool(csv_path: str, query: str) -> str:
    """
    Performs statistical analysis on a CSV file.

    Supported queries:
        - 'describe' or 'summary'   : Descriptive statistics (mean, std, min, max, etc.) for all numeric columns.
        - 'missing' or 'null'       : Count of missing (NaN) values per column.
        - 'duplicates'              : Number of duplicate rows in the dataset.
        - 'correlation' or 'corr'  : Pearson correlation matrix of numeric columns.
        - 'dtypes' or 'types'      : Data type of each column.
        - 'unique'                  : Number of unique values per column.
        - 'value_counts:<column>'  : Top 10 value counts for a specific column (e.g. 'value_counts:Gender').

    Args:
        csv_path: Path to the CSV file.
        query:    The analysis query string (see supported queries above).

    Returns:
        A formatted string with the analysis results.
    """
    try:
        csv_path = validate_csv_path(csv_path)
        df = pd.read_csv(csv_path)
    except ValueError as e:
        return f"Security error: {e}"
    except Exception as e:
        return f"Error reading CSV: {e}"

    q = query.lower().strip()

    try:
        # --- Descriptive statistics ---
        if "describe" in q or "summary" in q:
            numeric_df = df.select_dtypes(include="number")
            if numeric_df.empty:
                return "No numeric columns found in the dataset to describe."
            stats = numeric_df.describe().round(3)
            return f"📊 Descriptive Statistics:\n\n{stats.to_string()}"

        # --- Missing values ---
        elif "missing" in q or "null" in q or "nan" in q:
            missing = df.isnull().sum()
            missing_pct = (df.isnull().mean() * 100).round(2)
            result = pd.DataFrame({
                "Missing Count": missing,
                "Missing %": missing_pct
            })
            total_missing = missing.sum()
            return (
                f"🔍 Missing Value Analysis:\n\n{result.to_string()}\n\n"
                f"Total missing values: {total_missing} out of {df.size} cells "
                f"({(total_missing / df.size * 100):.2f}%)"
            )

        # --- Duplicate rows ---
        elif "duplicate" in q:
            dup_count = df.duplicated().sum()
            return (
                f"🔁 Duplicate Row Analysis:\n\n"
                f"Total duplicate rows: {dup_count} out of {len(df)} rows.\n"
                f"({(dup_count / len(df) * 100):.2f}% of the dataset)"
            )

        # --- Correlation matrix ---
        elif "corr" in q or "correlation" in q:
            numeric_df = df.select_dtypes(include="number")
            if numeric_df.empty:
                return "No numeric columns found for correlation analysis."
            if numeric_df.shape[1] < 2:
                return "At least 2 numeric columns are needed for correlation analysis."
            corr = numeric_df.corr().round(3)
            return f"🔗 Pearson Correlation Matrix:\n\n{corr.to_string()}"

        # --- Data types ---
        elif "dtype" in q or "type" in q:
            dtypes = df.dtypes.reset_index()
            dtypes.columns = ["Column", "Data Type"]
            return f"📋 Column Data Types:\n\n{dtypes.to_string(index=False)}"

        # --- Unique value counts per column ---
        elif "unique" in q:
            unique_counts = df.nunique().reset_index()
            unique_counts.columns = ["Column", "Unique Values"]
            return f"🎯 Unique Value Counts per Column:\n\n{unique_counts.to_string(index=False)}"

        # --- Value counts for a specific column ---
        elif q.startswith("value_counts:"):
            col = query.split(":", 1)[1].strip()
            if col not in df.columns:
                available = ", ".join(df.columns.tolist())
                return f"Column '{col}' not found. Available columns: {available}"
            vc = df[col].value_counts().head(10)
            return (
                f"📊 Top 10 Value Counts for '{col}':\n\n"
                + vc.to_string()
                + f"\n\nTotal unique values: {df[col].nunique()}"
            )

        else:
            return (
                "I didn't understand your query. Supported statistical queries:\n"
                "  • describe / summary\n"
                "  • missing / null\n"
                "  • duplicates\n"
                "  • correlation / corr\n"
                "  • dtypes / types\n"
                "  • unique\n"
                "  • value_counts:<column_name>"
            )

    except Exception as e:
        return f"Error performing analysis: {e}"
