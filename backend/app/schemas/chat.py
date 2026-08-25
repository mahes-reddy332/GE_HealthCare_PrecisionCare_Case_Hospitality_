from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str
    patient_id: Optional[int] = None

class ChatSourceCitation(BaseModel):
    source: str
    confidence: str

class ChatToolCall(BaseModel):
    tool: str
    args: str

class ChatResponse(BaseModel):
    reply: str
    citations: List[ChatSourceCitation] = []
