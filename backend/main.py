"""
NexusAI Backend - FastAPI server powered by MiMo V2.5
"""

import os
import uuid
import json
from datetime import datetime
from typing import Optional, List
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import httpx
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="NexusAI",
    description="Smart Reasoning Assistant powered by MiMo V2.5",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Config
MIMO_API_BASE = os.getenv("MIMO_API_BASE", "https://api.pina.my.id/v1")
MIMO_API_KEY = os.getenv("MIMO_API_KEY", "")
MIMO_MODEL = os.getenv("MIMO_MODEL", "mimo-v2.5-pro")

# Storage
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
SESSIONS_DIR = Path("sessions")
SESSIONS_DIR.mkdir(exist_ok=True)


# ==================== Models ====================

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None
    reasoning: bool = True

class ChatResponse(BaseModel):
    response: str
    reasoning_steps: Optional[List[str]] = None
    session_id: str
    model: str
    tokens_used: Optional[int] = None

class TTSRequest(BaseModel):
    text: str
    voice: str = "default"
    speed: float = 1.0


# ==================== Helpers ====================

async def call_mimo_api(messages: list, model: str = MIMO_MODEL, **kwargs) -> dict:
    """Call MiMo V2.5 API (OpenAI-compatible)"""
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{MIMO_API_BASE}/chat/completions",
            headers={
                "Authorization": f"Bearer {MIMO_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": messages,
                "temperature": kwargs.get("temperature", 0.7),
                "max_tokens": kwargs.get("max_tokens", 2048),
                **({"response_format": {"type": "json_object"}} if kwargs.get("json_mode") else {})
            }
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"MiMo API error: {response.text}")
        
        return response.json()


def get_session_history(session_id: str) -> list:
    """Load session history from file"""
    session_file = SESSIONS_DIR / f"{session_id}.json"
    if session_file.exists():
        with open(session_file) as f:
            return json.load(f)
    return []


def save_session_history(session_id: str, history: list):
    """Save session history to file"""
    session_file = SESSIONS_DIR / f"{session_id}.json"
    with open(session_file, "w") as f:
        json.dump(history, f, indent=2)


# ==================== Endpoints ====================

@app.get("/")
async def root():
    return {
        "name": "NexusAI",
        "model": MIMO_MODEL,
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "model": MIMO_MODEL}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatMessage):
    """Chat with reasoning engine"""
    session_id = request.session_id or str(uuid.uuid4())
    
    # Load history
    history = get_session_history(session_id)
    
    # Build messages
    system_prompt = """You are NexusAI, a smart reasoning assistant powered by MiMo V2.5.

When answering complex questions:
1. Break down the problem into steps
2. Show your reasoning process
3. Provide clear, actionable answers
4. Consider multiple perspectives

Format your reasoning with clear steps when the question requires analysis."""
    
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": request.message})
    
    # Call API
    result = await call_mimo_api(messages)
    
    assistant_message = result["choices"][0]["message"]["content"]
    reasoning_steps = None
    
    # Extract reasoning if enabled
    if request.reasoning and "step" in assistant_message.lower():
        lines = assistant_message.split("\n")
        reasoning_steps = [l.strip() for l in lines if l.strip().startswith(("1.", "2.", "3.", "4.", "5.", "-", "•", "Step"))]
    
    # Update history
    history.append({"role": "user", "content": request.message})
    history.append({"role": "assistant", "content": assistant_message})
    save_session_history(session_id, history)
    
    return ChatResponse(
        response=assistant_message,
        reasoning_steps=reasoning_steps if reasoning_steps else None,
        session_id=session_id,
        model=MIMO_MODEL,
        tokens_used=result.get("usage", {}).get("total_tokens")
    )


@app.post("/api/analyze-image")
async def analyze_image(
    image: UploadFile = File(...),
    prompt: str = Form("Describe this image in detail")
):
    """Analyze image with multimodal MiMo"""
    # Save uploaded file
    file_path = UPLOAD_DIR / f"{uuid.uuid4()}_{image.filename}"
    with open(file_path, "wb") as f:
        content = await image.read()
        f.write(content)
    
    # For now, use text-based description (MiMo multimodal would need vision API)
    # In production, this would use MiMo's vision capabilities
    messages = [
        {"role": "system", "content": "You are an image analysis expert. Describe images in detail."},
        {"role": "user", "content": f"Analyze this image: {prompt}\n\n[Image uploaded: {image.filename}]"}
    ]
    
    result = await call_mimo_api(messages)
    
    return {
        "description": result["choices"][0]["message"]["content"],
        "filename": image.filename,
        "prompt": prompt,
        "model": MIMO_MODEL
    }


@app.post("/api/document-qa")
async def document_qa(
    document: UploadFile = File(...),
    question: str = Form(...)
):
    """Question answering on uploaded documents"""
    # Save and read document
    file_path = UPLOAD_DIR / f"{uuid.uuid4()}_{document.filename}"
    content = await document.read()
    
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Extract text (simplified - in production use proper document parsing)
    try:
        text_content = content.decode("utf-8")[:4000]  # Limit context
    except:
        text_content = f"[Binary file: {document.filename}]"
    
    messages = [
        {"role": "system", "content": "You are a document analysis expert. Answer questions based on the provided document content. Be precise and cite relevant sections."},
        {"role": "user", "content": f"Document content:\n\n{text_content}\n\nQuestion: {question}"}
    ]
    
    result = await call_mimo_api(messages)
    
    return {
        "answer": result["choices"][0]["message"]["content"],
        "document": document.filename,
        "question": question,
        "model": MIMO_MODEL
    }


@app.post("/api/tts")
async def text_to_speech(request: TTSRequest):
    """Convert text to speech using MiMo TTS"""
    # In production, this would call MiMo TTS API
    # For demo, return a placeholder
    return {
        "message": "TTS endpoint ready - requires MiMo TTS API integration",
        "text": request.text,
        "voice": request.voice,
        "speed": request.speed,
        "audio_url": None  # Would be actual audio file URL
    }


@app.get("/api/sessions")
async def list_sessions():
    """List all chat sessions"""
    sessions = []
    for session_file in SESSIONS_DIR.glob("*.json"):
        with open(session_file) as f:
            history = json.load(f)
        if history:
            sessions.append({
                "session_id": session_file.stem,
                "message_count": len(history),
                "last_message": history[-1]["content"][:100] if history else ""
            })
    return {"sessions": sessions}


@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    """Get session history"""
    history = get_session_history(session_id)
    return {"session_id": session_id, "messages": history}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
