from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class Reward(BaseModel):
    value: float = Field(..., description="Reward value")
    reason: str = Field(..., description="Reward reason")

class Observation(BaseModel):
    task_id: str
    summary: str
    turn: int
    max_turns: int
    visible_symptoms: List[str]
    available_actions: List[str] 
    messages: List[str]

class State(BaseModel):
    task_id: str
    turn: int
    done: bool
    total_reward: float
    completed_steps: Dict[str, bool]
    discovered: Dict[str, Any]
    final_decision: Optional[str] = None
    final_score: float = 0.0

class Action(BaseModel):
    action_type: str
    target: str
    content: Optional[str] = None

class StepResult(BaseModel):
    observation: Observation
    reward: Reward
    done: bool