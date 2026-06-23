import os
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow
from openai import OpenAI

# LangGraph Imports
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END

app = FastAPI(title="Autonomous Multimodal Security Pipeline")
client = OpenAI()

# ───────────────────────────────────────────────────────────────────────
# SYSTEM CONFIGURATION
# ───────────────────────────────────────────────────────────────────────
mlflow.set_tracking_uri("http://10.169.0.73:8080")  # Keep your Mac IP here
mlflow.set_experiment("Autonomous_Multimodal_Security_Pipeline")


class PipelineState(TypedDict):
    repo_path: str
    architecture_diagram: str
    vulnerabilities: List[str]
    status: str
    target_file_path: str
    raw_code: str


# ───────────────────────────────────────────────────────────────────────
# 2. LIVE AI NODES
# ───────────────────────────────────────────────────────────────────────

def auditor_node(state: PipelineState) -> dict:
    """Workstation 1: Real LLM scan of the target file code."""
    # Look for our new advanced controller file
    target_file = f"{state['repo_path']}/api_v2.py"
    print(f"--> [Auditor Node] Reading target file: {target_file}")
    # ... rest of your code remains exactly the same!

    if not os.path.exists(target_file):
        return {"vulnerabilities": [], "status": "Target file not found."}

    with open(target_file, "r") as f:
        code_content = f.read()

    print("--> [Auditor Node] Sending code to OpenAI for vulnerability analysis...")

    # Call OpenAI to inspect the code
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert cybersecurity auditor. Review the provided code and state any vulnerabilities found concisely. If none, say NONE."},
            {"role": "user", "content": f"Review this code:\n\n{code_content}"}
        ]
    )

    analysis = response.choices[0].message.content
    print(f"--> [Auditor Analysis]: {analysis}")

    vulnerabilities = [analysis] if "NONE" not in analysis.upper() else []

    return {
        "vulnerabilities": vulnerabilities,
        "raw_code": code_content,
        "target_file_path": target_file,
        "status": "Auditing Complete"
    }


def patch_node(state: PipelineState) -> dict:
    """Workstation 2: Takes the analysis and physically rewrites the file on your Mac."""
    if not state["vulnerabilities"]:
        return {"status": "Secure. No patches required."}

    print("--> [Patch Node] Requesting secure code patch from OpenAI...")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert secure coding assistant. Rewrite the user's code to fix the security vulnerabilities. Return ONLY valid, executable Python code block. Do not include markdown formatting or backticks outside the raw code."},
            {"role": "user", "content": f"Vulnerabilities found:\n{state['vulnerabilities'][0]}\n\nOriginal Code:\n{state['raw_code']}"}
        ]
    )

    patched_code = response.choices[0].message.content.strip()

    # Clean up markdown code blocks if the LLM accidentally added them
    if patched_code.startswith("```python"):
        patched_code = patched_code.split("```python")[1].split("```")[0].strip()
    elif patched_code.startswith("```"):
        patched_code = patched_code.split("```")[1].split("```")[0].strip()

    # CRITICAL PROD STEP: Physically overwrite the file via the volume bridge!
    print(f"--> [Patch Node] Overwriting target file with secure patch: {state['target_file_path']}")
    with open(state['target_file_path'], "w") as f:
        f.write(patched_code)

    mlflow.log_metric("vulnerabilities_patched", len(state["vulnerabilities"]))

    return {
        "status": "Patched Successfully"
    }


# ───────────────────────────────────────────────────────────────────────
# 3. ORCHESTRATION GRAPH
# ───────────────────────────────────────────────────────────────────────
workflow = StateGraph(PipelineState)
workflow.add_node("auditor", auditor_node)
workflow.add_node("patcher", patch_node)
workflow.set_entry_point("auditor")
workflow.add_edge("auditor", "patcher")
workflow.add_edge("patcher", END)
compiled_pipeline = workflow.compile()


# ───────────────────────────────────────────────────────────────────────
# 4. API GATEWAY
# ───────────────────────────────────────────────────────────────────────
class AuditRequest(BaseModel):
    repo_path: str
    architecture_diagram: str

@app.post("/api/v1/audit")
async def run_audit(payload: AuditRequest):
    try:
        with mlflow.start_run(run_name="agent_security_audit"):
            mlflow.log_param("target_repo", payload.repo_path)

            initial_state = {
                "repo_path": payload.repo_path,
                "architecture_diagram": payload.architecture_diagram,
                "vulnerabilities": [],
                "status": "Initialized",
                "target_file_path": "",
                "raw_code": ""
            }

            final_output = compiled_pipeline.invoke(initial_state)

            return {
                "status": "success",
                "pipeline_final_status": final_output["status"],
                "vulnerabilities_found": len(final_output["vulnerabilities"]),
                "patched": final_output["status"] == "Patched Successfully"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))