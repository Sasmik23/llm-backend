# LLM Interaction API - Backend 

This is a backend implementation that supports CRUD operations for conversations with an LLM and sending prompt queries. It uses FastAPI, Beanie (with MongoDB), and the OpenAI Python client.

## Features

- **Conversations Endpoints**
  - `POST /conversations` – Create a new conversation.
  - `GET /conversations` – List all conversations.
  - `GET /conversations/{id}` – Retrieve a full conversation (with history).
  - `PUT /conversations/{id}` – Update conversation properties.
  - `DELETE /conversations/{id}` – Delete a conversation.
  
- **LLM Query Endpoint**
  - `POST /queries/{id}`
    - Sends anonymized prompts (with sensitive data redacted) to the LLM.
    - Uses the OpenAI API for generating responses.
    - Logs both the raw and anonymized data for auditing.

## Tech Stack

- Python 3.10
- FastAPI
- Beanie (ODM for MongoDB)
- Motor (Async MongoDB driver)
- OpenAI Python Client
- Docker & Docker Compose

## Prerequisites

- Docker and Docker Compose installed on your system.
- A valid OpenAI API key. This should be stored in a `.env` file in the project root.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Sasmik23/llm-backend.git
cd llm_backend
```

### 2.Create .env file
In the project root, create a file named .env with the following content:
```env
OPENAI_API_KEY=<your_openai_api_key>
```

### 3.Build and run application 
```bash
docker compose up 
```

The MongoDB service will be available at mongodb://mongodb:27017.

The llm-backend service will run on http://localhost:8000, and api endpoints can be tested at http://localhost:8000/docs
