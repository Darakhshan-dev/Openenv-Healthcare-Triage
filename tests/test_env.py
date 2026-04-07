from env.environment import HealthcareEnv
from env.models import Action

def test_easy_task_runs():
    env = HealthcareEnv(seed=42)
    obs = env.reset("task_easy")
    assert obs.task_id == "task_easy"

    result = env.step(Action(action_type="ask_duration", target="patient"))
    assert result.observation.turn == 1
    assert isinstance(result.reward.value, float)