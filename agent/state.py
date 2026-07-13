import operator
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """
    The state of our agent. It stores the history of messages,
    as well as the current path to the CSV file we're analyzing.
    """
    messages: Annotated[Sequence[BaseMessage], operator.add]
    csv_file_path: str
