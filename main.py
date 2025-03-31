from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from contextlib import asynccontextmanager


from models import Conversation, PromptQueryDocument
from routers import conversation, queries


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient("mongodb://mongodb:27017")
    await init_beanie(database=client.llm_db, document_models=[Conversation, PromptQueryDocument])
    yield
    client.close()

app = FastAPI(title="LLM Interaction API", version="2.0.0", lifespan=lifespan)

app.include_router(conversation.router, prefix="/conversations", tags=["Conversations"])
app.include_router(queries.router, prefix="/queries", tags=["LLM Queries"])