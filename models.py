"""Data models for the NoPickles AI POS MVP."""

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class MenuItem(BaseModel):
    """Represents a menu item."""
    id: str
    name: str
    category: str
    price: float
    description: Optional[str] = None
    available: bool = True


class OrderItem(BaseModel):
    """Represents an item in an order."""
    menu_item_id: str
    menu_item_name: str
    quantity: int = 1
    price: float
    subtotal: float


class Order(BaseModel):
    """Represents a customer order."""
    session_id: str
    items: List[OrderItem] = Field(default_factory=list)
    total: float = 0.0
    status: str = "in_progress"  # in_progress, completed, cancelled
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def add_item(self, item: OrderItem) -> None:
        """Add an item to the order."""
        self.items.append(item)
        self.total += item.subtotal

    def calculate_total(self) -> float:
        """Calculate the total price of the order."""
        self.total = sum(item.subtotal for item in self.items)
        return self.total


class ChatMessage(BaseModel):
    """Represents a chat message from the user."""
    message: str
    session_id: str


class ChatResponse(BaseModel):
    """Represents a response from the AI agent."""
    response: str
    session_id: str
    order_status: Optional[dict] = None
