import asyncio
import random
from typing import Dict, List, Optional
from .models import Observation, Reward, StepResult, State, Action

class HealthcareEnv:
    TASKS = {
        "task_easy": {
            "summary": "22yo patient with 2-day fever and weakness",
            "initial_symptoms": ["fever", "weakness", "fatigue"],
            "symptoms": ["fever", "weakness", "fatigue", "mild cough"],
            "available_actions": ["ask_duration", "check_vitals", "route_opd", "route_emergency", "recommend_test", "final_decision", "declare_done"]
        },
        "task_medium": {
            "summary": "48yo patient with chest pain and sweating x1hr",
            "initial_symptoms": ["chest pain", "sweating"],
            "symptoms": ["chest pain", "sweating", "shortness of breath", "nausea"],
            "available_actions": ["ask_duration", "check_vitals", "route_opd", "route_emergency", "recommend_test", "final_decision", "declare_done"]
        },
        "task_hard": {
            "summary": "67yo patient with sudden slurred speech, right arm weakness",
            "initial_symptoms": ["slurred speech", "right arm weakness"],
            "symptoms": ["slurred speech", "right arm weakness", "facial droop", "confusion"],
            "available_actions": ["ask_duration", "check_vitals", "route_opd", "route_emergency", "recommend_test", "final_decision", "declare_done"]
        }
    }
    
    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.seed = seed
        self.task_id = None
        self.task_data = None
        self.turn = 0
        self.max_turns = 10
        self.done = False
        self.total_reward = 0.0
        self.completed_steps = {}
        self.discovered = {}
        self.messages = []
        self.final_decision = None
        
    def _reset_sync(self, task_id: str):
        self.task_id = task_id
        self.turn = 0
        self.done = False
        self.total_reward = 0.0
        self.completed_steps = {}
        self.discovered = {}
        self.messages = []
        self.final_decision = None
        
        self.task_data = self.TASKS.get(task_id, self.TASKS["task_easy"])
        
        obs = Observation(
            task_id=task_id,
            summary=self.task_data["summary"],
            turn=0,
            max_turns=self.max_turns,
            visible_symptoms=self.task_data["initial_symptoms"],
            available_actions=self.task_data["available_actions"],
            messages=["Patient arrived. Please triage appropriately."]
        )
        return obs
    
    async def reset(self, task_id: str):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._reset_sync, task_id)
    
    def _step_sync(self, action: Action):
        if self.done:
            return StepResult(
                observation=Observation(task_id=self.task_id, turn=self.turn, max_turns=self.max_turns, visible_symptoms=[], available_actions=[], messages=[]),
                reward=Reward(value=0.0, reason="Episode already done"),
                done=True
            )
        
        self.turn += 1
        reward = Reward(value=0.0, reason="No reward")
        
        if action.action_type == "ask_duration":
            self.completed_steps["ask_duration"] = True
            self.messages.append("Patient reports symptoms for 2 days.")
            reward = Reward(value=0.1, reason="Basic history taken")
            
        elif action.action_type == "check_vitals":
            self.completed_steps["check_vitals"] = True
            vitals = "BP 120/80, HR 88, Temp 100.4F, O2 98%" if "easy" in self.task_id else "BP 160/100, HR 110, O2 92%"
            self.messages.append(f"Vitals: {vitals}")
            reward = Reward(value=0.15, reason="Vital signs assessed")
            
        elif action.action_type == "route_opd":
            if "task_easy" in self.task_id:
                self.completed_steps["route_opd"] = True
                self.messages.append("✅ Patient routed to OPD - appropriate")
                reward = Reward(value=0.4, reason="Correct routing")
            else:
                self.messages.append("❌ Wrong routing for urgent case")
                reward = Reward(value=-0.2, reason="Incorrect routing")
                
        elif action.action_type == "route_emergency":
            if "task_easy" not in self.task_id:
                self.completed_steps["route_emergency"] = True
                self.messages.append("✅ Emergency activated - correct")
                reward = Reward(value=0.4, reason="Correct escalation")
            else:
                reward = Reward(value=-0.1, reason="Over-escalation")
                
        elif action.action_type == "recommend_test":
            correct_test = "ecg" if "medium" in self.task_id else "brain imaging"
            if action.target == correct_test:
                self.completed_steps["recommend_test"] = True
                self.messages.append(f"✅ {action.target.upper()} ordered")
                reward = Reward(value=0.25, reason="Correct test")
            else:
                reward = Reward(value=0.05, reason="Suboptimal test")
                
        elif action.action_type == "final_decision":
            self.final_decision = action.content or "Decision recorded"
            self.messages.append(f"📋 Final decision: {self.final_decision}")
            reward = Reward(value=0.2, reason="Decision made")
            
        elif action.action_type == "declare_done":
            self.done = True
            reward = Reward(value=0.1, reason="Episode ended")
            
        self.total_reward += reward.value
        
        obs = Observation(
            task_id=self.task_id,
            summary=self.task_data["summary"],
            turn=self.turn,
            max_turns=self.max_turns,
            visible_symptoms=self.task_data["symptoms"],
            available_actions=self.task_data["available_actions"],
            messages=self.messages[-5:]
        )
        
        if self.turn >= self.max_turns:
            self.done = True
            
        return StepResult(observation=obs, reward=reward, done=self.done)
    
    async def step(self, action: Action):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._step_sync, action)
    
    def state(self) -> State:
        # Simple scoring logic - no grader dependency
        score = 0.0
        steps_count = sum(1 for v in self.completed_steps.values() if v)
        
        if self.task_id == "task_easy":
            if self.completed_steps.get("route_opd") and steps_count >= 3:
                score = 1.0
            elif steps_count >= 2:
                score = 0.7
        elif self.task_id == "task_medium":
            if self.completed_steps.get("route_emergency") and self.completed_steps.get("recommend_test"):
                score = 1.0
            elif self.completed_steps.get("route_emergency"):
                score = 0.8
        elif self.task_id == "task_hard":
            if self.completed_steps.get("route_emergency") and self.completed_steps.get("recommend_test"):
                score = 1.0
            elif self.completed_steps.get("route_emergency"):
                score = 0.8
        
        return State(
            task_id=self.task_id or "",
            turn=self.turn,
            done=self.done,
            total_reward=self.total_reward,
            completed_steps=self.completed_steps,
            discovered=self.discovered,
            final_decision=self.final_decision,
            final_score=score
        )
    
    def close(self):
        self.done = True