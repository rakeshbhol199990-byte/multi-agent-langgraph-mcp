import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.graph_workflow import LangGraphSupervisorWorkflow
from src.mcp_tools import ModelContextProtocolConnector

def run_test_suite():
    print("=" * 70)
    print("RUNNING MULTI-AGENT LANGGRAPH & MCP VERIFICATION SUITE")
    print("=" * 70)

    workflow = LangGraphSupervisorWorkflow()
    mcp = ModelContextProtocolConnector()

    # 1. Test Model Context Protocol (MCP) Tools Discovery
    tools = mcp.list_tools()
    print(f"\n[1] Model Context Protocol (MCP) Tool Discovery Test:")
    print(f"    [+] Registered MCP Tools Count: {len(tools)}")
    for t in tools:
        print(f"      - Tool: '{t['name']}' -> {t['description']}")
    assert len(tools) == 3, "MCP tool count mismatch!"

    # 2. Test Coder Agent Workflow Execution
    coder_task = "Write a Python script for structured Pydantic schema parsing"
    coder_state = workflow.run_full_execution(coder_task)

    print(f"\n[2] Coder Agent Workflow Execution Test:")
    print(f"    [+] Task: '{coder_task}'")
    print(f"    [+] Agent Routed: {coder_state.messages[0].content}")
    print(f"    [+] Code Output: {coder_state.results.get('code_output', {}).get('output')}")
    assert "code_output" in coder_state.results, "Coder Agent execution failed!"

    # 3. Test Database Agent with HITL Approval Gate
    db_task = "Execute SQL database query to update enterprise metrics"
    db_state = workflow.run_full_execution(db_task, approve_hitl=True)

    print(f"\n[3] Database Agent with Human-in-the-Loop (HITL) Gate Test:")
    print(f"    [+] Task: '{db_task}'")
    print(f"    [+] Human Approved: {db_state.human_approved}")
    print(f"    [+] Database Output: {db_state.results.get('db_output')}")
    assert db_state.results.get("db_output", {}).get("rows_returned") == 10, "HITL DB Execution failed!"

    # 4. Test Corrective RAG (CRAG) Web Search Fallback
    crag_task = "Search latest 2026 AI news and stale knowledge updates"
    crag_state = workflow.run_full_execution(crag_task)

    print(f"\n[4] Corrective RAG (CRAG) Web Search Fallback Test:")
    print(f"    [+] Task: '{crag_task}'")
    print(f"    [+] CRAG Triggered: {crag_state.crag_fallback_triggered}")
    print(f"    [+] Snippet Retrieved: {crag_state.results.get('crag_output', {}).get('snippet')}")
    assert crag_state.crag_fallback_triggered is True, "CRAG fallback failed to trigger!"

    print("\n" + "=" * 70)
    print("SUCCESS: ALL TESTS PASSED SUCCESSFULLY! PROJECT 3 VERIFIED 100%")
    print("=" * 70)

if __name__ == "__main__":
    run_test_suite()
