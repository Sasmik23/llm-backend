import asyncio
from uuid import UUID
from fastapi import APIRouter, HTTPException
from models import Conversation, Prompt, PromptQueryDocument
from typing import Dict
import hashlib
import openai
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from fastapi import HTTPException
import re


load_dotenv()  

router = APIRouter()

def anonymize_prompt(prompt: Prompt) -> Prompt:
    anon_content = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '[REDACTED_EMAIL]', prompt.content)
    anon_content = re.sub(r'\b(?:\+?65[-\s]?)?[689]\d{7}\b', '[REDACTED_SG_PHONE]', anon_content)
    return Prompt(role=prompt.role, content=anon_content)


async def call_llm(context: str, params: dict, model: str) -> str:

    client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    try:
        response = await client.responses.create(
            model=model,
            input=context,
            **params 
        )
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Error calling OpenAI API: {e}")
    
    return response.output_text

@router.post("/{id}", status_code=201)
async def create_prompt(id: UUID, prompt: Prompt):
    conversation = await Conversation.get(id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    anonymized_query = anonymize_prompt(prompt)

    conversation_context = "\n".join([p.content for p in conversation.prompts if isinstance(p, Prompt)])
    context = f"{conversation_context}\n{anonymized_query.content}" if conversation_context else anonymized_query.content

    response_text = await call_llm(context, conversation.params, conversation.model)
    response_prompt = Prompt(role="assistant", content=response_text)
    anonymized_response = anonymize_prompt(response_prompt)

    conversation.prompts.append(anonymized_query)
    conversation.prompts.append(anonymized_response)

    conversation.tokens += len(anonymized_query.content.split()) + len(anonymized_response.content.split())

    await conversation.save()

    audit_doc = PromptQueryDocument(
        conversation_id=id,
        anonymized_data={
            "query": anonymized_query.model_dump(),
            "response": anonymized_response.model_dump()
        }
    )
    await audit_doc.insert()

    return {"id": str(audit_doc.id)}
