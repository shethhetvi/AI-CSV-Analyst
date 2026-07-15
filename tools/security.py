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

import os


def validate_csv_path(csv_path: str) -> str:
    """
    Guard against path traversal attacks.

    Resolves the given path to an absolute path and verifies it lives
    inside the project's ``uploads/`` directory.  Raises ``ValueError``
    if the path escapes the allowed directory so callers can return a
    safe error message instead of reading arbitrary files.

    Args:
        csv_path: The path string supplied by the LLM or the user.

    Returns:
        The resolved absolute path (str) when it is safe.

    Raises:
        ValueError: If the path resolves outside ``uploads/``.
    """
    # Resolve both sides to real absolute paths (handles ../ tricks)
    uploads_dir = os.path.realpath(
        os.path.join(os.path.dirname(__file__), "..", "uploads")
    )
    resolved = os.path.realpath(csv_path)

    if not resolved.startswith(uploads_dir + os.sep) and resolved != uploads_dir:
        raise ValueError(
            f"Access denied: '{csv_path}' is outside the permitted uploads directory."
        )

    if not resolved.endswith(".csv"):
        raise ValueError(
            f"Access denied: only .csv files are permitted, got '{os.path.basename(resolved)}'."
        )

    return resolved
