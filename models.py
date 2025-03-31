from typing import Any, Dict, List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from beanie import Document


class Prompt(BaseModel):
    role: str  # should be one of system, user, assistant, function
    content: str

    class Config:
        extra = "allow"


class Conversation(Document):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    name: str
    params: Dict[str, Any] = {}
    pinned: bool = False
    prompts: List[Prompt] = []
    model: str
    tokens: int = 0
    modifications: List[Any] = []  

    class Settings:
        name = "conversations"


