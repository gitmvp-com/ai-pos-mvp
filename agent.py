"""Conversational AI agent for order taking using LangChain."""

import os
from typing import Dict, Optional
from datetime import datetime

from models import Order, OrderItem
from menu import menu_manager


class OrderAgent:
    """AI agent for handling conversational order taking."""
    
    def __init__(self):
        self.orders: Dict[str, Order] = {}
        self.conversation_context: Dict[str, list] = {}
        
        # Check if OpenAI API key is available
        self.has_openai = bool(os.getenv("OPENAI_API_KEY"))
        
        if self.has_openai:
            try:
                from langchain_openai import ChatOpenAI
                from langchain.prompts import ChatPromptTemplate
                from langchain.schema import HumanMessage, SystemMessage
                
                self.llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0.7
                )
                self.use_llm = True
            except Exception as e:
                print(f"Warning: Could not initialize OpenAI: {e}")
                print("Falling back to mock mode")
                self.use_llm = False
        else:
            print("No OpenAI API key found. Running in mock mode.")
            self.use_llm = False
    
    def get_or_create_order(self, session_id: str) -> Order:
        """Get existing order or create a new one for the session."""
        if session_id not in self.orders:
            self.orders[session_id] = Order(session_id=session_id)
        return self.orders[session_id]
    
    def process_message(self, session_id: str, message: str) -> str:
        """Process a message from the user and return a response."""
        order = self.get_or_create_order(session_id)
        
        # Initialize conversation context
        if session_id not in self.conversation_context:
            self.conversation_context[session_id] = []
        
        # Add user message to context
        self.conversation_context[session_id].append({
            "role": "user",
            "content": message
        })
        
        if self.use_llm:
            response = self._process_with_llm(session_id, message, order)
        else:
            response = self._process_mock(session_id, message, order)
        
        # Add assistant response to context
        self.conversation_context[session_id].append({
            "role": "assistant",
            "content": response
        })
        
        return response
    
    def _process_with_llm(self, session_id: str, message: str, order: Order) -> str:
        """Process message using LangChain and OpenAI."""
        from langchain.schema import HumanMessage, SystemMessage
        
        menu_text = menu_manager.get_menu_text()
        order_summary = self._get_order_summary(order)
        
        system_prompt = f"""You are a friendly AI assistant for NoPickles, a fast food restaurant.
Your job is to help customers order food through natural conversation.

{menu_text}

Current order for this customer:
{order_summary}

Guidelines:
- Be friendly and conversational
- Help customers find items on the menu
- Confirm items as you add them
- Provide the running total
- When customers say they're done, summarize the order and thank them
- If they ask for something not on the menu, politely suggest alternatives

Respond naturally to the customer's message."""
        
        messages = [
            SystemMessage(content=system_prompt),
        ]
        
        # Add conversation history
        for msg in self.conversation_context[session_id][-6:]:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
        
        try:
            response = self.llm.invoke(messages)
            ai_response = response.content
            
            # Try to extract order information and update the order
            self._extract_and_add_items(message, order)
            
            return ai_response
        except Exception as e:
            print(f"Error with LLM: {e}")
            return self._process_mock(session_id, message, order)
    
    def _process_mock(self, session_id: str, message: str, order: Order) -> str:
        """Process message using simple rule-based logic (mock mode)."""
        message_lower = message.lower()
        
        # Greeting detection
        greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
        if any(greeting in message_lower for greeting in greetings):
            return "Hello! Welcome to NoPickles. I'm here to help you order. What would you like today?"
        
        # Menu request
        if "menu" in message_lower or "what do you have" in message_lower or "what can i get" in message_lower:
            return f"Here's our menu:{menu_manager.get_menu_text()}\n\nWhat would you like to order?"
        
        # Extract items from message
        added_items = self._extract_and_add_items(message, order)
        
        if added_items:
            items_text = ", ".join([f"{item.menu_item_name} (${item.price:.2f})" for item in added_items])
            return f"Great! I've added {items_text} to your order. Your current total is ${order.total:.2f}. Would you like anything else?"
        
        # Check if customer is done
        done_phrases = ["that's all", "that's it", "nothing else", "no thanks", "i'm done", "that'll be all", "finish", "complete"]
        if any(phrase in message_lower for phrase in done_phrases):
            if order.items:
                order.status = "completed"
                order.completed_at = datetime.now()
                summary = self._get_order_summary(order)
                return f"Perfect! Your order is complete.\n{summary}\n\nThank you for ordering with NoPickles!"
            else:
                return "You haven't ordered anything yet. What would you like?"
        
        # Default response
        return "I'm not sure I understood that. You can tell me what you'd like to order, ask for the menu, or let me know if you're done ordering."
    
    def _extract_and_add_items(self, message: str, order: Order) -> list:
        """Extract menu items from the message and add them to the order."""
        message_lower = message.lower()
        added_items = []
        
        # Search for menu items in the message
        for item in menu_manager.get_all_items():
            item_name_lower = item.name.lower()
            
            # Check if item name is in the message
            if item_name_lower in message_lower:
                # Create order item
                order_item = OrderItem(
                    menu_item_id=item.id,
                    menu_item_name=item.name,
                    quantity=1,
                    price=item.price,
                    subtotal=item.price
                )
                order.add_item(order_item)
                added_items.append(order_item)
        
        return added_items
    
    def _get_order_summary(self, order: Order) -> str:
        """Generate a text summary of the order."""
        if not order.items:
            return "No items ordered yet."
        
        summary = "Order Summary:\n"
        for item in order.items:
            summary += f"  - {item.quantity}x {item.menu_item_name}: ${item.subtotal:.2f}\n"
        summary += f"\nTotal: ${order.total:.2f}"
        return summary
    
    def get_order(self, session_id: str) -> Optional[Order]:
        """Get the order for a specific session."""
        return self.orders.get(session_id)
    
    def get_all_orders(self) -> Dict[str, Order]:
        """Get all orders."""
        return self.orders


# Global agent instance
agent = OrderAgent()
