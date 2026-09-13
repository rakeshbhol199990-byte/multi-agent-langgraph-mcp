from .supervisor_state import AgentState, Message
from .mcp_tools import ModelContextProtocolConnector

mcp = ModelContextProtocolConnector()

class CoderAgent:
    def run(self, state: AgentState) -> AgentState:
        code_res = mcp.execute_code("def process_data(): return 'Clean Structured JSON'")
        state.messages.append(Message(sender="CoderAgent", content=f"Generated code successfully: {code_res['output']}"))
        state.results["code_output"] = code_res
        state.next_agent = "Supervisor"
        return state

class DatabaseAgent:
    def run(self, state: AgentState) -> AgentState:
        if not state.human_approved:
            state.requires_human_approval = True
            state.messages.append(Message(sender="DatabaseAgent", content="WAITING_FOR_HITL_APPROVAL: SQL Write Operation"))
            return state

        db_res = mcp.run_sql("SELECT * FROM enterprise_metrics;")
        state.messages.append(Message(sender="DatabaseAgent", content=f"Executed SQL: {db_res['rows_returned']} rows returned."))
        state.results["db_output"] = db_res
        state.requires_human_approval = False
        state.next_agent = "Supervisor"
        return state

class CRAGWebSearchAgent:
    """Corrective RAG (CRAG) Agent for stale knowledge fallback."""
    def run(self, state: AgentState) -> AgentState:
        search_res = mcp.perform_crag_search(state.task)
        state.crag_fallback_triggered = True
        state.messages.append(Message(sender="CRAGWebSearchAgent", content=f"Retrieved fresh knowledge via CRAG: {search_res['snippet']}"))
        state.results["crag_output"] = search_res
        state.next_agent = "Supervisor"
        return state
