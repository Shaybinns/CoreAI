from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import asyncio
import json

from core.config import settings
from core.brain import AIBrain, BrainConfig

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Universal AI Core API"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global brain instance
brain: Optional[AIBrain] = None

# Request/Response models
class ChatRequest(BaseModel):
    user_id: str
    message: str
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    user_id: str
    metadata: Optional[Dict[str, Any]] = None

class ToolInfo(BaseModel):
    name: str
    description: str

# Startup/Shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize the AI brain on startup"""
    global brain
    
    config = BrainConfig(
        app_name=settings.app_name,
        version=settings.app_version,
        db_url=settings.database_url,
        model_provider=settings.model_provider,
        model_name=settings.model_name,
        temperature=settings.model_temperature,
    )
    
    brain = AIBrain(config)
    await brain.initialize()
    
    # Register example tools
    from domain.example.tools.calculator import CalculatorTool
    brain.components['tools'].register_tool(CalculatorTool())
    
    print(f"✅ {settings.app_name} API started successfully!")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    if brain:
        await brain.shutdown()

# REST Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "brain_initialized": brain is not None
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a chat message"""
    if not brain:
        raise HTTPException(status_code=500, detail="Brain not initialized")
    
    try:
        # Collect full response
        response_text = ""
        async for chunk in brain.process(
            request.user_id,
            request.message,
            request.context
        ):
            response_text += chunk
        
        return ChatResponse(
            response=response_text,
            user_id=request.user_id,
            metadata={"status": "success"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tools", response_model=List[ToolInfo])
async def list_tools():
    """List available tools"""
    if not brain:
        raise HTTPException(status_code=500, detail="Brain not initialized")
    
    tools = brain.components['tools'].list_tools()
    return [ToolInfo(**tool) for tool in tools]

# WebSocket for streaming
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket endpoint for real-time streaming"""
    await websocket.accept()
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            message = message_data.get("message", "")
            context = message_data.get("context", {})
            
            # Send acknowledgment
            await websocket.send_json({
                "type": "ack",
                "status": "processing"
            })
            
            # Stream response
            async for chunk in brain.process(user_id, message, context):
                await websocket.send_json({
                    "type": "chunk",
                    "content": chunk
                })
            
            # Send completion
            await websocket.send_json({
                "type": "complete",
                "status": "success"
            })
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for user: {user_id}")
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    
    print(f"Starting {settings.app_name} API Server...")
    print(f"API Docs: http://localhost:{settings.api_port}/docs")
    
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        reload=True  # Set to False in production
    )
