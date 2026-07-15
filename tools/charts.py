import os
import time
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend, safe for Streamlit
import matplotlib.pyplot as plt
from langchain_core.tools import tool
from tools.security import validate_csv_path

CHART_PREFIX = "CHART:"

def _save_fig(fig: plt.Figure) -> str:
    """Save a matplotlib figure to the uploads dir and return its path."""
    os.makedirs("uploads", exist_ok=True)
    path = os.path.join("uploads", f"chart_{int(time.time())}.png")
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    return path

@tool
def chart_tool(csv_path: str, chart_type: str, x_column: str, y_column: str = "", title: str = "") -> str:
    """
    Generates a chart from a CSV file and saves it as an image.

    Args:
        csv_path:   Path to the CSV file.
        chart_type: One of 'histogram', 'bar', 'pie', 'scatter', 'line'.
        x_column:   Column name for the X-axis (or the only column for histogram/pie).
        y_column:   Column name for the Y-axis (required for bar, scatter, line).
        title:      Optional chart title.

    Returns:
        A string starting with 'CHART:' followed by the saved image path,
        or an error message if something goes wrong.
    """
    try:
        csv_path = validate_csv_path(csv_path)
        df = pd.read_csv(csv_path)
    except ValueError as e:
        return f"Security error: {e}"
    except Exception as e:
        return f"Error reading CSV: {e}"

    if x_column not in df.columns:
        available = ", ".join(df.columns.tolist())
        return f"Column '{x_column}' not found. Available columns: {available}"

    chart_type = chart_type.lower().strip()
    chart_title = title or f"{chart_type.capitalize()} of {x_column}"

    try:
        fig, ax = plt.subplots(figsize=(8, 5))
        fig.patch.set_facecolor("#1e1e2e")
        ax.set_facecolor("#2a2a3e")
        ax.tick_params(colors="white")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        ax.title.set_color("white")
        for spine in ax.spines.values():
            spine.set_edgecolor("#555577")

        if chart_type == "histogram":
            if not pd.api.types.is_numeric_dtype(df[x_column]):
                return f"Histogram requires a numeric column. '{x_column}' is not numeric."
            ax.hist(df[x_column].dropna(), bins=20, color="#7c6af7", edgecolor="#a89cff")
            ax.set_xlabel(x_column)
            ax.set_ylabel("Frequency")

        elif chart_type == "bar":
            if y_column and y_column in df.columns:
                data = df.groupby(x_column)[y_column].mean().sort_values(ascending=False).head(15)
                ax.bar(data.index.astype(str), data.values, color="#7c6af7", edgecolor="#a89cff")
                ax.set_ylabel(f"Mean {y_column}")
            else:
                data = df[x_column].value_counts().head(15)
                ax.bar(data.index.astype(str), data.values, color="#7c6af7", edgecolor="#a89cff")
                ax.set_ylabel("Count")
            ax.set_xlabel(x_column)
            plt.xticks(rotation=35, ha="right", color="white")

        elif chart_type == "pie":
            data = df[x_column].value_counts().head(8)
            colors = ["#7c6af7", "#f76a8c", "#f7a46a", "#6af7c8", "#f7e46a", "#6ab4f7", "#c86af7", "#6af76a"]
            # pyrefly: ignore [bad-unpacking]
            wedges, texts, autotexts = ax.pie(
                data.values, labels=data.index.astype(str),
                autopct="%1.1f%%", colors=colors,
                textprops={"color": "white"}
            )
            for at in autotexts:
                at.set_color("white")

        elif chart_type == "scatter":
            if not y_column or y_column not in df.columns:
                return f"Scatter chart requires a valid y_column. Available: {', '.join(df.columns)}"
            if not pd.api.types.is_numeric_dtype(df[x_column]) or not pd.api.types.is_numeric_dtype(df[y_column]):
                return f"Scatter chart requires numeric columns. Check '{x_column}' and '{y_column}'."
            ax.scatter(df[x_column], df[y_column], color="#7c6af7", alpha=0.6, edgecolors="#a89cff", linewidths=0.5)
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)

        elif chart_type == "line":
            if not y_column or y_column not in df.columns:
                return f"Line chart requires a valid y_column. Available: {', '.join(df.columns)}"
            ax.plot(df[x_column], df[y_column], color="#7c6af7", linewidth=2, marker="o", markersize=3)
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
            plt.xticks(rotation=35, ha="right", color="white")

        else:
            return f"Unknown chart type '{chart_type}'. Supported: histogram, bar, pie, scatter, line."

        ax.set_title(chart_title, fontsize=14, pad=12)
        path = _save_fig(fig)
        return f"{CHART_PREFIX}{path}"

    except Exception as e:
        return f"Error generating chart: {e}"
