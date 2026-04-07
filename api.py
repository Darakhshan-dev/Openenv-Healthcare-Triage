from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from env.environment import HealthcareEnv
from env.models import Action

app = FastAPI(title="Healthcare Triage OpenEnv API")
_current_env = None

class StepRequest(BaseModel):
    action_type: str
    target: str
    content: Optional[str] = None

@app.get("/health")
async def health():
    return {"status": "ok", "env": "healthcare-triage", "version": "1.0"}

@app.post("/reset/{task_id}")
async def reset(task_id: str):
    global _current_env
    _current_env = HealthcareEnv(seed=42)
    obs = await _current_env.reset(task_id)
    return {"status": "ok", "observation": obs.__dict__, "task_id": task_id}

@app.post("/step")
async def step_action(request: StepRequest):
    global _current_env
    if not _current_env:
        return {"error": "Call /reset/{task_id} first"}
    
    action = Action(**request.dict())
    result = await _current_env.step(action)
    return {
        "reward": result.reward.value,
        "done": result.done,
        "observation": result.observation.__dict__,
        "state": _current_env.state().__dict__
    }

@app.get("/state")
async def get_state():
    global _current_env
    if not _current_env:
        return {"error": "Call /reset first"}
    return _current_env.state().__dict__