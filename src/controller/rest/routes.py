from typing import Final, Annotated
from urllib import request

from dependency_injector.wiring import Provide, inject

from fastapi import APIRouter, Depends

from src.agents.general_purpose import GPAgent
from .schemas import ChatRequest, ChatResponse
from ..container import ControllerContainer

router: Final = APIRouter()


@router.post("/chat")
@inject
async def chat(
        general_purpose_agent: Annotated[GPAgent, Depends(Provide[ControllerContainer.general_purpose_agent])],
) -> ChatResponse:
    try:
        response = await general_purpose_agent.run(request.message)
    except Exception as e:
        pass
    return None


