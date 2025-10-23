"""FastAPI application for NoPickles AI POS MVP."""

import os
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn

from models import ChatMessage, ChatResponse, MenuItem, Order
from agent import agent
from menu import menu_manager

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="NoPickles AI POS - MVP",
    description="A conversational AI Point-of-Sale system for fast food orders",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main HTML interface."""
    with open("static/index.html", "r") as f:
        return HTMLResponse(content=f.read())


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "NoPickles AI POS MVP",
        "llm_enabled": agent.use_llm
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Process a chat message and return AI response."""
    try:
        response = agent.process_message(message.session_id, message.message)
        order = agent.get_order(message.session_id)
        
        order_status = None
        if order:
            order_status = {
                "items_count": len(order.items),
                "total": order.total,
                "status": order.status
            }
        
        return ChatResponse(
            response=response,
            session_id=message.session_id,
            order_status=order_status
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/menu", response_model=List[MenuItem])
async def get_menu():
    """Get all menu items."""
    return menu_manager.get_all_items()


@app.get("/api/menu/category/{category}", response_model=List[MenuItem])
async def get_menu_by_category(category: str):
    """Get menu items by category."""
    items = menu_manager.get_items_by_category(category)
    if not items:
        raise HTTPException(status_code=404, detail=f"No items found in category: {category}")
    return items


@app.get("/api/orders")
async def get_all_orders():
    """Get all orders."""
    orders = agent.get_all_orders()
    return {
        "total_orders": len(orders),
        "orders": {sid: order.dict() for sid, order in orders.items()}
    }


@app.get("/api/orders/{session_id}", response_model=Order)
async def get_order(session_id: str):
    """Get order for a specific session."""
    order = agent.get_order(session_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"No order found for session: {session_id}")
    return order


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print("\n" + "="*60)
    print("🍔 NoPickles AI POS - MVP")
    print("="*60)
    print(f"\n🌐 Server starting at: http://{host}:{port}")
    print(f"📖 API Docs available at: http://{host}:{port}/docs")
    print(f"🤖 LLM Mode: {'Enabled (OpenAI)' if agent.use_llm else 'Mock Mode'}")
    print("\n" + "="*60 + "\n")
    
    uvicorn.run(app, host=host, port=port)
