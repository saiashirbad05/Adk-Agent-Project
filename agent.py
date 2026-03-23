from google.adk.agents import LlmAgent


root_agent = LlmAgent(
    name="adk_agent",
    model="gemini-2.5-flash",
    description="A text summarization agent built with Google ADK and Gemini.",
    instruction=(
        "You are adk-agent, a production-style text summarization assistant. "
        "Summarize the user's input clearly and faithfully. "
        "Preserve the core meaning, remove repetition, and keep the response concise. "
        "Return only the summary text, with no preamble and no bullet points."
    ),
)
