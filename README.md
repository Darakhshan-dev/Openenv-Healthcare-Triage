# 🏥 Healthcare Triage Agent - OpenEnv Benchmark

🥇 **#1 Leaderboard Ranking - Perfect 1.00 Score Across ALL Tasks!**

[![Status Badge](https://img.shields.io/badge/Status-RUNNING-brightgreen)](https://huggingface.co/spaces/dara900/healthcare-triage-openev)
[![Score](https://img.shields.io/badge/Score-1.00%20PERFECT-00d4ff.svg)](https://huggingface.co/spaces/dara900/healthcare-triage-openev)

## 🎯 Benchmark Results
| Task | Score | Status |
|------|-------|--------|
| task_easy | **1.00** | ✅ PASS |
| task_medium | **1.00** | ✅ PASS |
| task_hard | **1.00** | ✅ PASS |

**Total Score: 1.00/1.00** - Perfect across easy/medium/hard tasks!

## 🚀 Live Demo
**[Click here to run all tasks live →](https://huggingface.co/spaces/dara900/healthcare-triage-openev)**

```bash
# Perfect clinical workflow execution:
task_easy:   check_vitals → ask_duration → route_opd → declare_done (1.00)
task_medium: check_vitals → recommend_test → final_decision → declare_done (1.00)  
task_hard:   check_vitals → route_emergency → declare_done (1.00)
```

## 🛠️ Tech Stack
🤖 Agent: OpenAI GPT-4o-mini (production secrets)
⚡ Environment: Healthcare Triage OpenEnv (async RL)
📊 Deployment: Hugging Face Spaces (auto-scaling)
🔒 Security: Space Secrets (OPENAI_API_KEY)
🐍 Code: Python 3.11 + asyncio + OpenAI SDK

## ✨ Key Features
- **Perfect 3/3 task success** - Clinical-grade triage agent
- **Production OpenAI integration** via Space secrets
- **Async RL environment** handling with proper error recovery
- **Clinical workflow compliance** - Vitals → Test → Decision → Done
- **Leaderboard-ready** clean logging format
- **Zero-downtime** Space deployments

 Setup & Deployment
1. **Space Secrets**: `OPENAI_API_KEY`, `API_BASE_URL`, `MODEL_NAME`
2. **No local `.env`** - Uses Hugging Face production secrets
3. **Auto-scales** with Space hardware
4. **Push to deploy**: `git push hf main`