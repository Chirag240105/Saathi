from fastapi import APIRouter, Depends

from app.core.security import require_key
from app.schemas.care import ChatIn, ChatOut, ToolCallRecordOut
from app.simulator.agent import chat

router = APIRouter(prefix="/api/simulator", tags=["simulator"], dependencies=[Depends(require_key)])


@router.post("/chat", response_model=ChatOut)
async def simulator_chat(body: ChatIn) -> ChatOut:
    res = await chat(body.text)
    return ChatOut(
        reply=res.reply, used_llm=res.used_llm,
        tool_calls=[ToolCallRecordOut(name=c.name, arguments=c.arguments, result=c.result,
                                      duration_ms=c.duration_ms, success=c.success)
                    for c in res.tool_calls],
    )
