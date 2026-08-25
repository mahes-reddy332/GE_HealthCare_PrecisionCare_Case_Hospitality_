from ..schemas.chat import ChatResponse

class ChatService:
    @staticmethod
    async def handle_query(query: str) -> ChatResponse:
        return ChatResponse(reply="I am a mock response.")
