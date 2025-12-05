"""
Product model for the inventory management system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class Product:
    """Represents a product in the inventory."""
    
    name: str
    category: str
    price: float
    quantity: int
    sku: str = field(default_factory=lambda: str(uuid.uuid4())[:8].upper())
    description: str = ""
    reorder_level: int = 10
    supplier: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def __post_init__(self):
        """Validate product data after initialization."""
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative")
        if self.reorder_level < 0:
            raise ValueError("Reorder level cannot be negative")
        if not self.name:
            raise ValueError("Product name cannot be empty")
        if not self.category:
            raise ValueError("Category cannot be empty")
    
    def to_dict(self) -> dict:
        """Convert product to dictionary for serialization."""
        return {
            "sku": self.sku,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "quantity": self.quantity,
            "description": self.description,
            "reorder_level": self.reorder_level,
            "supplier": self.supplier,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        """Create a Product instance from a dictionary."""
        return cls(
            sku=data.get("sku", ""),
            name=data["name"],
            category=data["category"],
            price=data["price"],
            quantity=data["quantity"],
            description=data.get("description", ""),
            reorder_level=data.get("reorder_level", 10),
            supplier=data.get("supplier", ""),
            created_at=data.get("created_at", datetime.now().isoformat()),
            updated_at=data.get("updated_at", datetime.now().isoformat())
        )
    
    def is_low_stock(self) -> bool:
        """Check if product is below reorder level."""
        return self.quantity <= self.reorder_level
    
    def total_value(self) -> float:
        """Calculate total inventory value for this product."""
        return self.price * self.quantity
    
    def update_timestamp(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now().isoformat()
