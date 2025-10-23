# NoPickles AI POS - MVP

_A simplified conversational AI Point-of-Sale system for fast food orders_

## Overview

This is an MVP version of [NoPickles.ai](https://github.com/iota-tec/nopickles) - a conversational kiosk platform for fast food environments. This simplified version focuses on the core feature: **AI-powered conversational order taking**.

## Features

✅ **Conversational Order Interface** - Natural language order processing using LangChain  
✅ **Menu Management** - Simple in-memory menu system  
✅ **Order Processing** - Complete order flow from greeting to confirmation  
✅ **REST API** - FastAPI-based endpoints for order management  
✅ **Web Interface** - Simple HTML/JS frontend for testing  

## Tech Stack

- **Backend**: FastAPI (Python 3.12+)
- **AI/LLM**: LangChain with OpenAI integration
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Storage**: In-memory (no database required for MVP)

## Quick Start

### Prerequisites

- Python 3.12+
- OpenAI API key (optional - uses mock mode without it)

### Installation

```bash
# Clone the repository
git clone https://github.com/gitmvp-com/ai-pos-mvp.git
cd ai-pos-mvp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file (optional):

```env
OPENAI_API_KEY=your_api_key_here
```

**Note**: The MVP works without an API key in mock mode for testing.

### Run the Application

```bash
python main.py
```

The server will start at `http://localhost:8000`

### Access the Interface

Open your browser and navigate to:
- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/health

## API Endpoints

### Chat with the AI Agent
```http
POST /api/chat
Content-Type: application/json

{
  "message": "I'd like a cheeseburger and fries",
  "session_id": "user123"
}
```

### Get Menu
```http
GET /api/menu
```

### Get All Orders
```http
GET /api/orders
```

### Get Order by Session
```http
GET /api/orders/{session_id}
```

## Project Structure

```
.
├── main.py              # FastAPI application entry point
├── agent.py             # LangChain conversational agent
├── models.py            # Pydantic data models
├── menu.py              # Menu data and management
├── static/
│   └── index.html      # Web interface
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
└── README.md           # This file
```

## Usage Example

**Customer**: "Hi, I'd like to order"
**AI**: "Hello! Welcome to NoPickles. I'm here to help you order. What would you like today?"

**Customer**: "I'll have a cheeseburger and a large coke"
**AI**: "Great! I've added a Cheeseburger ($8.99) and a Large Coke ($2.49) to your order. Your current total is $11.48. Would you like anything else?"

**Customer**: "No, that's it"
**AI**: "Perfect! Your order is complete. Total: $11.48. Thank you for ordering with NoPickles!"

## Differences from Full NoPickles.ai

This MVP simplifies the full system by:

- ❌ No authentication/user management
- ❌ No database (in-memory storage)
- ❌ No face/voice recognition
- ❌ No PyTorch avatar models
- ❌ No vector database (FAISS)
- ❌ No manager dashboard
- ❌ No real-time personalization
- ❌ No multi-kiosk deployment

✅ **Focus**: Core conversational ordering experience

## Development

### Mock Mode (No API Key Required)

The agent automatically falls back to mock responses when no OpenAI API key is configured, making it easy to test the flow without incurring API costs.

### Adding Menu Items

Edit `menu.py` to add or modify menu items:

```python
MENU_ITEMS = [
    MenuItem(
        id="custom1",
        name="Custom Burger",
        category="burgers",
        price=9.99,
        description="Your custom creation"
    )
]
```

## License

MIT License - Based on [iota-tec/nopickles](https://github.com/iota-tec/nopickles)

## Contributing

This is an MVP demonstration. For the full production system, see the [main NoPickles.ai repository](https://github.com/iota-tec/nopickles).
