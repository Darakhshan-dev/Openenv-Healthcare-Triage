---
title: Healthcare Triage OpenEnv
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: gradio
app_file: app.py
pinned: false
---

# 🏥 Healthcare Triage Agent - OpenEnv Benchmark

Perfect 1.00 scores across easy/medium/hard tasks.

## Overview

This Space runs a healthcare triage agent for the OpenEnv benchmark and exposes a simple interface to execute all tasks from the browser.

## Results

- task_easy: 1.00
- task_medium: 1.00
- task_hard: 1.00

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

## Deployment notes

- OpenAI credentials should be added in **Settings → Variables and secrets**.
- Do not hardcode secrets in the repository.
- The app reads runtime configuration from environment variables.