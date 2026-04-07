from typing import Dict
from .environment import State

def grade_easy(state: State) -> float:
    """Grade easy task - returns score in [0, 1]"""
    score = 0.0
    
    # Required steps (25% each)
    if state.completed_steps.get("check_vitals"):
        score += 0.25
    if state.completed_steps.get("route_opd"):
        score += 0.50  # Most important for easy case
    if state.final_decision:
        score += 0.25
    
    return min(max(score, 0.0), 1.0)

def grade_medium(state: State) -> float:
    """Grade medium task - returns score in [0, 1]"""  
    score = 0.0
    
    # Required steps with appropriate weights
    if state.completed_steps.get("check_vitals"):
        score += 0.20
    if state.completed_steps.get("recommend_test"):
        score += 0.30  # ECG critical for chest pain
    if state.completed_steps.get("route_emergency"):
        score += 0.30  # Must escalate chest pain
    if state.final_decision:
        score += 0.20
    
    return min(max(score, 0.0), 1.0)

def grade_hard(state: State) -> float:
    """Grade hard task - returns score in [0, 1]"""
    score = 0.0
    
    # Stroke protocol weights
    if state.completed_steps.get("check_vitals"):
        score += 0.20
    if state.completed_steps.get("recommend_test"):  # Brain imaging
        score += 0.30
    if state.completed_steps.get("route_emergency"):
        score += 0.30  # Stroke is time-critical
    if state.final_decision:
        score += 0.20
    
    return min(max(score, 0.0), 1.0)

# Update environment state with real grader scores
def update_final_scores(env):
    """Called by inference.py to set real grader scores"""
    state = env.state()
    if state.task_id == "task_easy":
        state.final_score = grade_easy(state)
    elif state.task_id == "task_medium":
        state.final_score = grade_medium(state)
    elif state.task_id == "task_hard":
        state.final_score = grade_hard(state)
    return state