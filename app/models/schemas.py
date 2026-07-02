from typing import List , Literal
from pydantic import BaseModel , Field

class Message(BaseModel):
    role: Literal["user" , "assistant" , "system"]
    content:str = Field(... , min_length = 1)

class ChatRequest(BaseModel):
    messages: List[Message]

class Recommendation(BaseModel):
    name : str
    url :str
    test_type : str

class ChatResponse(BaseModel):
    reply : str
    recommendations : List[Recommendation]
    end_of_conversation : bool

    