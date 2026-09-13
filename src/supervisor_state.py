from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class Message(BaseModel):
    sender: str
    content: str

class AgentState(BaseModel):
    """
    LangGraph AgentState:
    Maintains persistent memory state across multi-agent turns.
    """
    task: str = Field(..., description="User requested task description")
    messages: List[Message] = Field(default_factory=list)
    next_agent: str = Field(default="Supervisor", description="Next node in LangGraph state machine")
    results: Dict[str, Any] = Field(default_factory=dict)
    requires_human_approval: bool = Field(default=False, description="Human-in-the-Loop (HITL) Checkpoint flag")
    human_approved: Optional[bool] = Field(default=None)
    crag_fallback_triggered: bool = Field(default=False, description="Corrective RAG trigger flag")
