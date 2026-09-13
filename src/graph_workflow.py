from .supervisor_state import AgentState, Message
from .agents import CoderAgent, DatabaseAgent, CRAGWebSearchAgent

class LangGraphSupervisorWorkflow:
    """
    LangGraph Supervisor State Machine Workflow:
    - Coordinates Coder, Database, and CRAG Web Search agents.
    - Persistent stateful memory checkpointing.
    - Human-in-the-loop (HITL) approval gates for database mutations.
    - Corrective RAG (CRAG) fallback for low retrieval confidence.
    """
    def __init__(self):
        self.coder_agent = CoderAgent()
        self.db_agent = DatabaseAgent()
        self.crag_agent = CRAGWebSearchAgent()

    def route_supervisor(self, state: AgentState) -> str:
        task_lower = state.task.lower()
        if "sql" in task_lower or "database" in task_lower:
            return "DatabaseAgent"
        elif "stale" in task_lower or "search" in task_lower or "latest" in task_lower:
            return "CRAGWebSearchAgent"
        else:
            return "CoderAgent"

    def step(self, state: AgentState) -> AgentState:
        if state.next_agent == "Supervisor":
            target = self.route_supervisor(state)
            state.next_agent = target
            state.messages.append(Message(sender="Supervisor", content=f"Routing task to {target}"))
            return state

        if state.next_agent == "CoderAgent":
            state = self.coder_agent.run(state)
        elif state.next_agent == "DatabaseAgent":
            state = self.db_agent.run(state)
        elif state.next_agent == "CRAGWebSearchAgent":
            state = self.crag_agent.run(state)

        if not state.requires_human_approval and state.next_agent == "Supervisor":
            state.next_agent = "FINISH"

        return state

    def run_full_execution(self, task: str, approve_hitl: bool = True) -> AgentState:
        state = AgentState(task=task)
        # Step 1: Supervisor Route
        state = self.step(state)
        # Step 2: Agent Execution
        state = self.step(state)
        
        # Step 3: Handle HITL Checkpoint if triggered
        if state.requires_human_approval:
            state.human_approved = approve_hitl
            state = self.step(state)  # Re-run after approval

        return state
