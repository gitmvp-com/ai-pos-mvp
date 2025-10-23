"""Menu data and management for the NoPickles AI POS MVP."""

from typing import List, Optional
from models import MenuItem

# Sample menu items for a fast food restaurant
MENU_ITEMS: List[MenuItem] = [
    # Burgers
    MenuItem(
        id="burger1",
        name="Classic Burger",
        category="burgers",
        price=6.99,
        description="Beef patty with lettuce, tomato, and special sauce"
    ),
    MenuItem(
        id="burger2",
        name="Cheeseburger",
        category="burgers",
        price=8.99,
        description="Classic burger with melted cheese"
    ),
    MenuItem(
        id="burger3",
        name="Double Burger",
        category="burgers",
        price=10.99,
        description="Two beef patties with all the fixings"
    ),
    MenuItem(
        id="burger4",
        name="Veggie Burger",
        category="burgers",
        price=7.99,
        description="Plant-based patty with fresh vegetables"
    ),
    
    # Sides
    MenuItem(
        id="side1",
        name="French Fries",
        category="sides",
        price=3.49,
        description="Crispy golden fries"
    ),
    MenuItem(
        id="side2",
        name="Onion Rings",
        category="sides",
        price=4.49,
        description="Beer-battered onion rings"
    ),
    MenuItem(
        id="side3",
        name="Side Salad",
        category="sides",
        price=4.99,
        description="Fresh mixed greens with dressing"
    ),
    
    # Drinks
    MenuItem(
        id="drink1",
        name="Small Coke",
        category="drinks",
        price=1.99,
        description="Coca-Cola (16oz)"
    ),
    MenuItem(
        id="drink2",
        name="Medium Coke",
        category="drinks",
        price=2.49,
        description="Coca-Cola (22oz)"
    ),
    MenuItem(
        id="drink3",
        name="Large Coke",
        category="drinks",
        price=2.99,
        description="Coca-Cola (32oz)"
    ),
    MenuItem(
        id="drink4",
        name="Bottled Water",
        category="drinks",
        price=1.49,
        description="Pure spring water"
    ),
    MenuItem(
        id="drink5",
        name="Milkshake",
        category="drinks",
        price=4.99,
        description="Chocolate, vanilla, or strawberry"
    ),
    
    # Desserts
    MenuItem(
        id="dessert1",
        name="Apple Pie",
        category="desserts",
        price=2.99,
        description="Warm apple pie"
    ),
    MenuItem(
        id="dessert2",
        name="Ice Cream Cone",
        category="desserts",
        price=2.49,
        description="Soft serve vanilla ice cream"
    ),
]


class MenuManager:
    """Manages menu items and provides search functionality."""
    
    def __init__(self):
        self.items = {item.id: item for item in MENU_ITEMS}
    
    def get_all_items(self) -> List[MenuItem]:
        """Get all menu items."""
        return list(self.items.values())
    
    def get_item_by_id(self, item_id: str) -> Optional[MenuItem]:
        """Get a menu item by ID."""
        return self.items.get(item_id)
    
    def search_items(self, query: str) -> List[MenuItem]:
        """Search menu items by name (case-insensitive)."""
        query_lower = query.lower()
        return [
            item for item in self.items.values()
            if query_lower in item.name.lower() or 
               (item.description and query_lower in item.description.lower())
        ]
    
    def get_items_by_category(self, category: str) -> List[MenuItem]:
        """Get all items in a specific category."""
        return [
            item for item in self.items.values()
            if item.category.lower() == category.lower()
        ]
    
    def get_menu_text(self) -> str:
        """Generate a formatted menu text for the AI agent."""
        categories = {}
        for item in self.items.values():
            if item.category not in categories:
                categories[item.category] = []
            categories[item.category].append(item)
        
        menu_text = "\n=== MENU ===\n"
        for category, items in sorted(categories.items()):
            menu_text += f"\n{category.upper()}:\n"
            for item in items:
                menu_text += f"  - {item.name}: ${item.price:.2f}\n"
        
        return menu_text


# Global menu manager instance
menu_manager = MenuManager()
