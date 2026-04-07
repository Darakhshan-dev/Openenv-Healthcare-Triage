# Healthcare Triage OpenEnv

A real-world OpenEnv environment for learning clinical triage decision-making through a standard `reset() / step() / state()` API.


This environment simulates patient triage in a healthcare setting. An agent must gather relevant information, choose tests, route the patient safely, and submit a final decision. The environment includes partial rewards, deterministic grading, and three difficulty levels.
---

## Why this is a real-world task

This is not a toy or game environment. It models a realistic workflow that appears in hospitals, telemedicine intake systems, and emergency screening pipelines:

- collect missing patient information
- check vitals
- recommend a diagnostic test
- route to OPD or emergency care
- provide final triage reasoning

The goal is to help AI agents learn safe multi-step decision-making under structured constraints.

---

## Project structure

```text
healthcare-openenv/
├── app.py
├── openenv.yaml
├── README.md
├── requirements.txt
├── Dockerfile
├── .env.example
├── env/
│   ├── __init__.py
│   ├── models.py
│   ├── environment.py
│   ├── grader.py
│   └── tasks.py
├── tasks/
│   ├── task_easy.json
│   ├── task_medium.json
│   └── task_hard.json
├── baseline/
│   ├── scripted_baseline.py
│   └── openai_baseline.py
└── tests/
    └── test_env.py
```

---

## Environment API

The environment follows a simple OpenEnv-style interaction loop:

- `reset(task_id)` → returns the initial observation
- `step(action)` → applies one agent action and returns `StepResult`
- `state()` → returns the current internal environment state

---

## Typed models

The environment uses typed Pydantic models:

- `Action`
- `Observation`
- `Reward`
- `State`
- `StepResult`

This makes the action and state transitions explicit and easier to validate in evaluation pipelines.

---

## Action space

The agent can choose from these structured action types:

- `ask_duration`
- `check_vitals`
- `recommend_test`
- `route_emergency`
- `route_opd`
- `final_decision`
- `declare_done`

### Action schema

```python
Action(
    action_type: str,
    target: str,
    content: Optional[str] = None
)
```

### Example action

```python
Action(action_type="recommend_test", target="ecg")
```

---

## Observation space

Each step returns a structured observation:

```python
Observation(
    task_id: str,
    summary: str,
    visible_symptoms: List[str],
    available_actions: List[str],
    messages: List[str],
    turn: int,
    max_turns: int
)
```

### Example observation fields

- patient summary
- visible symptoms
- current turn number
- allowed actions
- feedback messages from the environment

---

## State space

The internal state tracks learning progress and grading signals:

```python
State(
    task_id: str,
    turn: int,
    max_turns: int,
    total_reward: float,
    final_score: float,
    completed_steps: Dict[str, bool],
    discovered: Dict[str, bool],
    done: bool
)
```

This state supports partial progress tracking and dense rewards.

---

## Tasks

The environment includes three tasks with increasing difficulty:

### `task_easy`
- Fever and weakness
- Expected safe OPD routing
- Simple history and vitals collection

### `task_medium`
- Chest pain and sweating
- Requires emergency routing
- Includes diagnostic test selection

### `task_hard`
- Slurred speech and one-sided weakness
- Stroke-like emergency
- Requires correct escalation and test recommendation

Each task is independently defined in `tasks/*.json`.

---

## Reward design

Rewards are designed to provide meaningful learning signals instead of a single terminal win/loss score.

### Reward principles

- small time penalty for each step
- positive reward for useful information gathering
- positive reward for correct testing
- positive reward for safe routing
- final grading reward at episode end
- penalties for unsafe routing or irrelevant actions

### Typical reward behavior

- collecting history: positive reward
- checking vitals: positive reward
- correct test recommendation: positive reward
- unsafe triage: negative reward
- final `declare_done`: adds final grader score

This supports partial progress learning.

---

## Grading

Each task has a deterministic grader that returns a score between `0.0` and `1.0`.

Scoring is based on whether the agent completed or discovered the required task steps. The grader is implemented in:

```text
env/grader.py
```

This makes evaluation easy to reproduce across runs.

---

## Baselines

The repository includes two baselines.

### 1. Scripted baseline

```bash
python -m baseline.scripted_baseline
```

This is a deterministic rule-based agent and should run without any external API dependency.

### 2. OpenAI baseline

```bash
python -m baseline.openai_baseline
```

This baseline uses the OpenAI API and requires a valid API key with active API quota.

---

## OpenAI baseline setup

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Important note

If the OpenAI baseline fails with a `429` or `insufficient_quota` error, the code is likely correct but the API account does not currently have active billing, credits, or available usage quota.

In that case:

- use the scripted baseline for reproducible local evaluation
- enable billing / credits in the OpenAI platform
- re-run the OpenAI baseline after quota becomes available

---

## Installation

### 1. Create virtual environment

```bash
python -m venv venv
```

### 2. Activate it

#### Windows PowerShell
```bash
venv\Scripts\Activate.ps1
```

#### Linux / macOS
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Local usage

Run the scripted baseline:

```bash
python -m baseline.scripted_baseline
```

Run the OpenAI baseline:

```bash
python -m baseline.openai_baseline
```

Run the Streamlit demo app:

```bash
streamlit run app.py
```

---

## Hugging Face Spaces deployment

This repository includes a Dockerfile for deployment to Hugging Face Spaces.

### Steps

1. Create a new **Docker Space** on Hugging Face
2. Push this repository to the Space
3. Ensure the container launches `app.py`
4. If needed, add `OPENAI_API_KEY` as a Hugging Face Space secret

---

## Reproducibility

- deterministic task files
- deterministic grader
- seeded environment initialization
- scripted reproducible baseline
- explicit typed models

This allows consistent benchmark runs.

---

## Example usage

```python
from env.environment import HealthcareEnv
from env.models import Action

env = HealthcareEnv(seed=42)
obs = env.reset("task_medium")

result = env.step(Action(action_type="ask_duration", target="patient"))
print(result.observation)
print(result.reward)

result = env.step(Action(action_type="check_vitals", target="patient"))
print(result.observation)

result = env.step(Action(action_type="recommend_test", target="ecg"))
print(result.reward)

result = env.step(Action(action_type="route_emergency", target="patient"))
print(env.state())
```

---

## Notes

This environment is intended for research, evaluation, and hackathon prototyping. It does not provide medical advice and should not be used for real patient care.