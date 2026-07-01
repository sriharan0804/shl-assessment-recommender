from fastapi import APIRouter
from app.models.schemas import ChatResponse , ChatRequest
from app.services.agent_service import handle_chat

router = APIRouter()

@router.get("/health")
def health():
    return {"status" : "ok"}

@router.post("/chat" , response_model = ChatResponse)
def chat(request : ChatRequest):
    return handle_chat(request)