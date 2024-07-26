from pydantic import BaseModel

class Query(BaseModel):
    user_id: str
    question: str

class ChatMessage(BaseModel):
    message: str
