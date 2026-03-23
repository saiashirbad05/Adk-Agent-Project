import os
import uuid
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from adk_agent.agent import root_agent


APP_NAME = "adk_agent"
USER_ID = "cloud-run-user"


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to summarize.")


class SummarizeResponse(BaseModel):
    original_text: str
    summary: str
    status: Literal["success"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    app.state.session_service = session_service
    app.state.runner = runner
    yield


app = FastAPI(
    title="adk-agent",
    version="1.0.0",
    description="Production-ready text summarization agent using Google ADK and Gemini.",
    lifespan=lifespan,
)


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.post("/summarize", response_model=SummarizeResponse)
async def summarize(payload: SummarizeRequest):
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="The 'text' field must not be empty.")

    session_id = str(uuid.uuid4())
    session_service = app.state.session_service
    runner = app.state.runner

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
    )

    message = Content(role="user", parts=[Part(text=text)])
    summary = ""

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=message,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            parts = [part.text for part in event.content.parts if getattr(part, "text", None)]
            summary = " ".join(parts).strip()

    if not summary:
        raise HTTPException(status_code=502, detail="The agent returned an empty summary.")

    return SummarizeResponse(
        original_text=text,
        summary=summary,
        status="success",
    )


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", "8080"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
