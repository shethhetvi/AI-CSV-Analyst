<div align="center">
  
  # 🧠✨ AI CSV Analyst

  **Your Intelligent, Agentic Data Scientist in a Box**

  [![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
  [![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
  [![LangGraph](https://img.shields.io/badge/LangGraph-000000.svg?style=for-the-badge&logo=code&logoColor=white)](https://python.langchain.com/v0.1/docs/langgraph/)
  [![Gemini](https://img.shields.io/badge/Powered%20by-Gemini%20%2F%20Ollama-8A2BE2.svg?style=for-the-badge)](https://ai.google.dev/)

  *Upload a CSV, ask questions in plain English, and let the AI analyze, visualize, and summarize your data instantly!*

</div>

---

## 🌟 Why AI CSV Analyst?

Gone are the days of writing repetitive Pandas scripts just to get a basic understanding of your data. **AI CSV Analyst** uses state-of-the-art LLMs combined with agentic routing to figure out *exactly* what you need. 

Want to know the average sales per region? Just ask. Need a scatter plot of age vs. income? Consider it done.

---

## 🚀 Features (Planned & In Progress)

- 📂 **Upload & Explore**: Drop in any CSV and immediately see a structured Pandas DataFrame.
- 🧠 **Agentic Brain**: An intelligent router decides which tool (analyzer, charts, stats) best handles your query.
- 💬 **Chat with your Data**: Ask *"Show me the first 5 rows"* or *"What's the dataset shape?"* for instant, natural language answers.
- 📊 **Beautiful Visualizations**: Auto-generate stunning Matplotlib charts (Histograms, Bar, Pie, Scatter).
- 🧹 **Data Janitor**: Automatically detects missing values, duplicates, and data quality issues.

---

## 🛠️ The Tech Engine

We've built this tool on a modern, robust AI stack:

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend UI** | 🎈 Streamlit | For a slick, reactive web interface |
| **AI / LLM** | 🧠 Gemini & Ollama | The brains powering the natural language understanding |
| **Agentic Flow** | 🕸️ LangGraph | Orchestrates the agent's thought process and tool usage |
| **Data Engine** | 🐼 Pandas | Heavy lifting for data manipulation |
| **Visuals** | 📈 Matplotlib | Rendering crisp, insightful charts |
| **Validation** | 🛡️ Pydantic | Ensuring robust data types and API contracts |

---

## 📂 Project Architecture

```bash
.
├── app.py                  # 🎈 Main Streamlit UI
├── agent/                  # 🧠 The Agent's Brain (LangGraph)
│   ├── graph.py            # Workflow orchestration
│   ├── nodes.py            # Execution nodes
│   └── state.py            # State management
├── tools/                  # 🔧 The Agent's Toolbox
│   ├── analyzer.py         # General data insights
│   ├── charts.py           # Visualization generator
│   ├── csv_loader.py       # Data ingestion
│   └── statistics.py       # Math & metrics
├── uploads/                # 📁 Secure local storage for CSVs
└── requirements.txt        # 📦 Dependencies
```

---

## 🎯 Quick Start Guide

Ready to chat with your data? Follow these steps to spin up your local instance!

### 1️⃣ Clone & Install
```bash
git clone git@github.com:shethhetvi/AI-CSV-Analyst.git
cd AI-CSV-Analyst
pip install -r requirements.txt
```

### 2️⃣ Configure the Magic (API Keys)
Create a `.env` file in the root directory. This is where your AI API key lives securely.
```env
# .env
GOOGLE_API_KEY="your-gcp-api-key-here"
```
> **Note:** The `.env` file is in `.gitignore`, so your secret will stay safe on your local machine.

### 3️⃣ Launch the App!
*(Note: Some features are still a work in progress!)*
```bash
streamlit run app.py
```

<div align="center">
  <i>Built with ❤️ for Data Enthusiasts.</i>
</div>
