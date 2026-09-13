from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .graph_workflow import LangGraphSupervisorWorkflow
from .mcp_tools import ModelContextProtocolConnector

app = FastAPI(
    title="Multi-Agent Autonomous AI Workflow API",
    description="LangGraph Supervisor State Machine with MCP Tool Protocol, HITL Gates, and CRAG Fallback",
    version="1.0.0"
)

workflow = LangGraphSupervisorWorkflow()
mcp = ModelContextProtocolConnector()

class WorkflowExecuteRequest(BaseModel):
    task: str = Field(..., description="Task prompt for the multi-agent system")
    auto_approve_hitl: bool = Field(default=True, description="Auto-approve HITL database write gates")

@app.get("/")
def read_root():
    return {
        "service": "Multi-Agent LangGraph Supervisor Workflow",
        "status": "Online",
        "mcp_tools_available": mcp.list_tools()
    }

@app.post("/execute-workflow")
def execute_workflow(payload: WorkflowExecuteRequest):
    try:
        final_state = workflow.run_full_execution(payload.task, approve_hitl=payload.auto_approve_hitl)
        return {
            "task": payload.task,
            "status": "completed",
            "messages": [m.dict() for m in final_state.messages],
            "results": final_state.results,
            "crag_fallback_triggered": final_state.crag_fallback_triggered
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
