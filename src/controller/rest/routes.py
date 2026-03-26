from typing import Final, Annotated
from urllib import request

from dependency_injector.wiring import Provide, inject

from fastapi import APIRouter, Depends

from agent import Agent
from .schemas import ChatRequest, ChatResponse
from ..container import ControllerContainer

router: Final = APIRouter()


@router.post("/chat")
@inject
async def chat(
        agent: Annotated[Agent, Depends(Provide[ControllerContainer.agent])],
) -> ChatResponse:
    try:
        response = await agent.run(request.message)
    except Exception as e:
        pass
    return None


