import os

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..agent.agent import Agent

agent_router = APIRouter()


class AgentRequest(BaseModel):
    message: str
    stream: bool | None = False


class AgentResponse(BaseModel):
    response: str
    analysis: dict | None = None


@agent_router.post("/chat")
async def chat_with_agent(request: AgentRequest):
    """Chat with the organization agent"""
    try:
        mistral_api_key = os.getenv("MISTRAL_API_KEY")
        if not mistral_api_key:
            raise HTTPException(status_code=400, detail="MISTRAL_API_KEY not configured")

        agent = Agent(mistral_api_key)

        if request.stream:
            # For streaming responses
            async def generate():
                for chunk in agent.run(request.message):
                    yield chunk

            return generate()
        else:
            # For non-streaming responses
            response_chunks = list(agent.run(request.message))
            full_response = "".join(response_chunks)

            return AgentResponse(response=full_response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@agent_router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "agent": "organAIzer"}


@agent_router.get("/capabilities")
async def get_capabilities():
    """Get agent capabilities"""
    return {
        "capabilities": [
            "priority_analysis",
            "organization_tips",
            "project_planning",
            "todoist_integration",
            "notion_integration"
        ]
    }
