from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from claude import chat_with_search
from chat_history import chat_history
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging
import uuid
from langchain.memory import ConversationBufferMemory
from datetime import datetime

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins 
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    session_id: str
    current_date: str

class ClearHistoryRequest(BaseModel):
    session_id: str = None

# Dictionary to store memory for each session
session_memories = {}

@app.get("/")
async def root():
    return {"message": "Hello, world!"}

@app.post("/chat", response_model=ChatResponse)
@limiter.limit("5/minute")
async def chat_endpoint(request: Request, chat_request: ChatRequest):
    logger.info(f"Received chat request: {chat_request}")
    try:
        session_id = chat_request.session_id or str(uuid.uuid4())
        
        if session_id not in session_memories:
            session_memories[session_id] = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        memory = session_memories[session_id]
        
        response = chat_with_search(chat_request.message, memory)
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Extract the text from the response if it's a list of dictionaries
        if isinstance(response, list) and len(response) > 0 and 'text' in response[0]:
            response_text = response[0]['text']
        else:
            response_text = str(response)
        
        logger.info(f"Chat response: {response_text}")
        return ChatResponse(message=response_text, session_id=session_id, current_date=current_date)
    except Exception as e:
        logger.error(f"Error in chat_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear_history")
async def clear_history(request: ClearHistoryRequest):
    logger.info(f"Received clear history request: {request}")
    try:
        if request.session_id:
            if request.session_id in session_memories:
                del session_memories[request.session_id]
            logger.info(f"Cleared history for session {request.session_id}")
            return {"message": f"Chat history cleared for session {request.session_id}"}
        else:
            logger.info("No session ID provided for clear history request")
            return {"message": "No session ID provided. Nothing to clear."}
    except Exception as e:
        logger.error(f"Error in clear_history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))