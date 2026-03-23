# ADK-AGENT-PROJECT

Production-ready text summarization agent built with Google ADK and Gemini, exposed through FastAPI, containerized with Docker, stored in Artifact Registry, and deployed on Cloud Run.

## Overview

This project implements a single AI agent named `adk-agent` that:

- uses Google ADK for agent orchestration
- uses Gemini for summarization
- accepts JSON input over HTTP
- returns structured JSON output
- is designed for Cloud Shell, Docker, Artifact Registry, and Cloud Run

## API

### Endpoint

`POST /summarize`

### Request

```json
{
  "text": "Cloud Run is a serverless platform for running containerized applications. It automatically scales and integrates with Google Cloud services."
}
```

### Response

```json
{
  "original_text": "Cloud Run is a serverless platform for running containerized applications. It automatically scales and integrates with Google Cloud services.",
  "summary": "Cloud Run is a serverless platform for containerized applications that automatically scales and integrates with Google Cloud services.",
  "status": "success"
}
```

## Project Structure

```text
.
|-- adk_agent/
|   |-- __init__.py
|   `-- agent.py
|-- docs/
|   |-- PROJECT_GUIDE.txt
|   `-- service_sab.txt
|-- main.py
|-- requirements.txt
|-- Dockerfile
|-- .dockerignore
|-- .gitignore
`-- README.md
```

## Main Files

- [adk_agent/agent.py](C:\Users\saias\OneDrive\Pictures\Documents\New project\adk-agent-project\adk_agent\agent.py)
- [main.py](C:\Users\saias\OneDrive\Pictures\Documents\New project\adk-agent-project\main.py)
- [requirements.txt](C:\Users\saias\OneDrive\Pictures\Documents\New project\adk-agent-project\requirements.txt)
- [Dockerfile](C:\Users\saias\OneDrive\Pictures\Documents\New project\adk-agent-project\Dockerfile)
- [PROJECT_GUIDE.txt](C:\Users\saias\OneDrive\Pictures\Documents\New project\adk-agent-project\docs\PROJECT_GUIDE.txt)

## Run In Cloud Shell

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --no-cache-dir -r requirements.txt
export GOOGLE_API_KEY="YOUR_REAL_GEMINI_API_KEY"
uvicorn main:app --host 0.0.0.0 --port 8080 --log-level debug
```

## Quick Test

```bash
curl -X POST http://127.0.0.1:8080/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Cloud Run is a serverless platform for running containerized applications. It automatically scales and integrates with Google Cloud services."
  }'
```

## Deployment Summary

1. Enable required APIs.
2. Build the image with Cloud Build.
3. Push to Artifact Registry.
4. Store `GOOGLE_API_KEY` in Secret Manager.
5. Deploy the container to Cloud Run.

Detailed instructions are in [PROJECT_GUIDE.txt](C:\Users\saias\OneDrive\Pictures\Documents\New project\adk-agent-project\docs\PROJECT_GUIDE.txt).

## Live Service

Cloud Run service URL:

`https://adk-agent-197228016542.us-central1.run.app`

Working endpoint:

`https://adk-agent-197228016542.us-central1.run.app/summarize`

## Important Notes

- Internal ADK agent name must be `adk_agent`.
- Final working Gemini model is `gemini-2.5-flash`.
- If deployment looks stale, use a fresh timestamped image tag instead of reusing `latest`.
