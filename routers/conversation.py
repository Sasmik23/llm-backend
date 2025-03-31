from fastapi import APIRouter, HTTPException
from models import Conversation, Prompt
from uuid import UUID
from typing import List

router = APIRouter()


@router.post("", status_code=201)
async def create_conversation(conversation_data: dict):
    """
    Creates a new conversation.
    """
    if "name" not in conversation_data or "model" not in conversation_data:
        raise HTTPException(status_code=400, detail="Missing required fields: name and model")
    
    conversation = Conversation(
        name=conversation_data["name"],
        params=conversation_data.get("params", {}),
        model=conversation_data["model"],
        pinned=conversation_data.get("pinned", False),
        prompts=[],
        tokens=0,
        modifications=[]
    )
    await conversation.insert()
    return {"id": str(conversation.id)}


@router.get("", response_model=List[Conversation])
async def get_conversations():
    """
    Retrieve all conversations.
    """
    conversations = await Conversation.find_all().to_list()
    return conversations


@router.get("/{id}", status_code=200)
async def get_conversation(id: UUID):
    """
    Retrieve full conversation details (including message history).
    """
    conversation = await Conversation.get(id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.put("/{id}", status_code=204)
async def update_conversation(id: UUID, update_data: dict):
    """
    Update conversation properties (e.g. name, params).
    """
    conversation = await Conversation.get(id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Update allowed fields
    if "name" in update_data:
        conversation.name = update_data["name"]
    if "params" in update_data:
        conversation.params = update_data["params"]
    
    await conversation.save()
    return


@router.delete("/{id}", status_code=204)
async def delete_conversation(id: UUID):
    """
    Delete a conversation.
    """
    conversation = await Conversation.get(id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    await conversation.delete()
    return
