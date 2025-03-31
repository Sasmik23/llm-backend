from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from models import Conversation
from routers import conversation

app = FastAPI(title="LLM Interaction API", version="2.0.0")

app.include_router(conversation.router, prefix="/conversations", tags=["Conversations"])

@app.on_event("startup")
async def app_init():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(database=client.llm_db, document_models=[Conversation])
