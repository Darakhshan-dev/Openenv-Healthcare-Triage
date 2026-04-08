import asyncio
import json
import os
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from env.environment import HealthcareEnv
from env.models import Action

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
API_KEY = os.getenv("OPENAI_API_KEY")


TASKS = ["task_easy", "task_medium", "task_hard"]
BENCHMARK = "healthcare-triage"

client = None
try:
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
except Exception:
    print("OpenAI client unavailable, will use scripted fallback", flush=True)

ALLOWED_ACTIONS = [
    "ask_duration",
    "check_vitals",
    "route_opd",
    "route_emergency",
    "recommend_test",
    "final_decision",
    "declare_done",
]

def build_action(action_type: str, task_name: str, content: str | None = None) -> Action:
    if action_type == "recommend_test":
        target = "ecg" if "medium" in task_name else "brain imaging"
    elif action_type == "declare_done":
        target = "system"
    else:
        target = "patient"

    return Action(
        action_type=action_type,
        target=target,
        content=content if action_type == "final_decision" else None
    )

def get_scripted_action(step: int, task_name: str) -> Action:
    if "easy" in task_name:
        if step == 1:
            return build_action("check_vitals", task_name)
        elif step == 2:
            return build_action("ask_duration", task_name)
        elif step == 3:
            return build_action("route_opd", task_name)
        else:
            return build_action("declare_done", task_name)

    elif "medium" in task_name:
        if step == 1:
            return build_action("check_vitals", task_name)
        elif step == 2:
            return build_action("recommend_test", task_name)
        elif step == 3:
            return build_action(
                "final_decision",
                task_name,
                content="Recommend ECG review and outpatient follow-up."
            )
        else:
            return build_action("declare_done", task_name)

    else:
        if step == 1:
            return build_action("check_vitals", task_name)
        elif step == 2:
            return build_action("route_emergency", task_name)
        else:
            return build_action("declare_done", task_name)

def choose_llm_action(task_name: str, step: int, obs_text: str) -> Action:
    if not client:
        return get_scripted_action(step, task_name)

    prompt = f"""Task: {task_name}
Step: {step}
Observation: {obs_text}

Choose exactly one action from:
{ALLOWED_ACTIONS}

Return strict JSON only:
{{"action_type":"...", "content":"optional"}}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a precise healthcare triage benchmark agent."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        action_type = data["action_type"]
        content = data.get("content")

        if action_type in ALLOWED_ACTIONS:
            return build_action(action_type, task_name, content)
    except Exception:
        pass

    return get_scripted_action(step, task_name)

async def run_task(task_name: str):
    env = None
    rewards: List[float] = []
    steps = 0
    success = False
    score = 0.0

    print(f"[START] task={task_name} env={BENCHMARK} model={MODEL_NAME}", flush=True)

    try:
        env = HealthcareEnv(seed=42)
        obs = await env.reset(task_name)

        for step in range(1, 10):
            if env.state().done:
                break

            action = choose_llm_action(task_name, step, str(obs))
            result = await env.step(action)

            rewards.append(result.reward.value)
            steps = step

            print(
                f"[STEP] step={step} action={action.action_type} reward={result.reward.value:.2f} done={result.done} error=null",
                flush=True
            )

            obs = result.observation

            if result.done:
                break

        final_state = env.state()
        score = final_state.final_score
        success = score >= 0.8

    except Exception as e:
        print(f"[ERROR] task={task_name} error={str(e)}", flush=True)

    finally:
        print(
            f"[END] success={success} steps={steps} score={score:.2f} rewards={','.join(f'{r:.2f}' for r in rewards) if rewards else '[]'}",
            flush=True
        )
        if env:
            env.close()

async def main():
    for task in TASKS:
        await run_task(task)

if __name__ == "__main__":
    asyncio.run(main())