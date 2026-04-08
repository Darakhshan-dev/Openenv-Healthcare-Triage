---
title: Healthcare Triage OpenEnv
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---

# Healthcare Triage OpenEnv

Real-world healthcare triage environment. **Baseline: 1.00 scores**

## Quick Start
```bash
pip install -r requirements.txt
cp .env.example .env
python inference.py
```

## Tasks
| Task | Difficulty | Baseline |
|------|------------|----------|
| task_easy | Easy | 1.00 |
| task_medium | Medium | 1.00 |
| task_hard | Hard | 1.00 |

## Deploy HF Space
1. Create Space → Docker SDK
2. Push repo
3. Add `OPENAI_API_KEY` secret