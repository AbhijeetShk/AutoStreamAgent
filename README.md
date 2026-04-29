# AutoStream Conversational AI Agent - Social-to-Lead

## Overview
This project is a LangGraph-based conversational agent for AutoStream. It can classify user intent, answer pricing or policy questions using local RAG, detect buying intent, collect lead details and trigger a backend tool.

## Demo Video

[Watch the demo](./demo.mov)

## Why LangGraph
The workflow has multiple states: answering questions, switching into lead qualification mode, collecting fields, then executing an action. LangGraph made this efficient than writing one long procedural chatbot script.

## LLM Used
Groq API with Llama 3.1 8B Instant (free tier friendly).

## Features
- Intent detection
- Knowledge base Q&A
- Lead capture flow
- Multi-turn memory

## Integrating Whatsapp (Future Enhancement)

For integrating whatsapp cloud we can use Whatsapp Cloud API by meta and python backend (Fast api maybe)

## Example Flow

When a user sends a message on WhatsApp, Meta sends that message to our webhook URL. The webhook receives details like the user’s phone number and message text.

From there:

Receive incoming message on webhook
Identify the user using their phone number
Pass message + previous conversation state into the LangGraph agent
Get agent response
Send reply back through WhatsApp API

So if someone asks pricing, the bot replies instantly. If they show interest, it moves into lead collection mode.


## Architecture


### Handling Memory Efficiently

Since this project needs multi-turn memory, I’d store each user’s conversation state using their phone number as a unique ID.

Example:

Asked pricing already
Interested in Pro plan
Name collected
Waiting for email

This can be stored in Redis (caching and fast option) or PostgreSQL if persistence is needed.


### Lead Capture Flow

Once the bot collects:

Name
Email
Creator platform

It can trigger mock_lead_capture() or send the lead to a real CRM like HubSpot.

### Security / Production Considerations

For real deployment we can add:

HTTPS only for trust, security and ranking
Request validation/auth
Webhook token verification
Logging and retry handling

### Stack (In case of whatsapp feature)
FastAPI – webhook backend
LangGraph – conversation workflow
Redis – memory/session state
Render / AWS – deployment


## Run Locally

### Run Streamlit UI

```bash
streamlit run ui/streamlit_app.py
```
### Using Docker

```bash
docker build -t autostream-agent .
docker run -p 8000:8000 --env-file .env autostream-agent
```

### Run Locally API

```bash
uvicorn main:app --reload
```