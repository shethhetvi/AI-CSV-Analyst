"""
tools/security.py
-----------------
Centralised security helpers for the AI CSV Analyst app.

Provides:
  - validate_csv_path()   : Path traversal guard for tool calls
  - sanitize_user_input() : Prompt injection + input hygiene
  - MAX_QUERIES_PER_SESSION : Session rate-limit constant
  - MAX_FILE_SIZE_BYTES     : Upload size cap constant
  - MAX_ROWS                : DataFrame row cap constant
"""
