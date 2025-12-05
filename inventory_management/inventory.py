"""
Core inventory management functionality.
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
from .models import Product
from .storage import InventoryStorage


class InventoryManager:
    """
    Main inventory management class providing full CRUD operations,
    stock management, and reporting capabilities.
    """
    
    def __init__(self, storage_path: str = "inventory_data.json"):
        """
        Initialize the inventory manager.
        
        Args:
            storage_path: Path to the JSON file for data persistence
        """
        self.storage = InventoryStorage(storage_path)
        self.products: Dict[str, Product] = self.storage.load()
    
    # ==================== CRUD Operations ====================
    
    def add_product(
        self,
        name: str,
        category: str,
        price: float,
        quantity: int,
        description: str = "",
        reorder_level: int = 10,
        supplier: str = "",
        sku: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Add a new product to the inventory.
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            product = Product(
                name=name,
                category=category,
                price=price,
                quantity=quantity,
                description=description,
                reorder_level=reorder_level,
                supplier=supplier
            )
            
            # Override SKU if provided
            if sku:
                if sku in self.products:
                    return False, f"Product with SKU '{sku}' already exists"
                product.sku = sku
            
            self.products[product.sku] = product
            self._save()
            return True, f"Product '{name}' added with SKU: {product.sku}"
            
        except ValueError as e:
            return False, str(e)
    
    def update_product(
        self,
        sku: str,
        name: Optional[str] = None,
        category: Optional[str] = None,
        price: Optional[float] = None,
        quantity: Optional[int] = None,
        description: Optional[str] = None,
        reorder_level: Optional[int] = None,
        supplier: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Update an existing product.
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        if sku not in self.products:
            return False, f"Product with SKU '{sku}' not found"
        
        product = self.products[sku]
        
        try:
            if name is not None:
                if not name:
                    return False, "Product name cannot be empty"
                product.name = name
            if category is not None:
                if not category:
                    return False, "Category cannot be empty"
                product.category = category
            if price is not None:
                if price < 0:
                    return False, "Price cannot be negative"
                product.price = price
            if quantity is not None:
                if quantity < 0:
                    return False, "Quantity cannot be negative"
                product.quantity = quantity
            if description is not None:
                product.description = description
            if reorder_level is not None:
                if reorder_level < 0:
                    return False, "Reorder level cannot be negative"
                product.reorder_level = reorder_level
            if supplier is not None:
                product.supplier = supplier
            
            product.update_timestamp()
            self._save()
            return True, f"Product '{sku}' updated successfully"
            
        except ValueError as e:
            return False, str(e)
    
    def delete_product(self, sku: str) -> Tuple[bool, str]:
        """
        Delete a product from the inventory.
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        if sku not in self.products:
            return False, f"Product with SKU '{sku}' not found"
        
        product_name = self.products[sku].name
        del self.products[sku]
        self._save()
        return True, f"Product '{product_name}' (SKU: {sku}) deleted"
    
    def get_product(self, sku: str) -> Optional[Product]:
        """Get a product by SKU."""
        return self.products.get(sku)
    
    def get_all_products(self) -> List[Product]:
        """Get all products in the inventory."""
        return list(self.products.values())
    
    # ==================== Stock Management ====================
    
    def add_stock(self, sku: str, quantity: int) -> Tuple[bool, str]:
        """
        Add stock to a product.
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        if sku not in self.products:
            return False, f"Product with SKU '{sku}' not found"
        
        if quantity <= 0:
            return False, "Quantity to add must be positive"
        
        product = self.products[sku]
        product.quantity += quantity
        product.update_timestamp()
        self._save()
        return True, f"Added {quantity} units to '{product.name}'. New quantity: {product.quantity}"
    
    def remove_stock(self, sku: str, quantity: int) -> Tuple[bool, str]:
        """
        Remove stock from a product (e.g., for sales).
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        if sku not in self.products:
            return False, f"Product with SKU '{sku}' not found"
        
        if quantity <= 0:
            return False, "Quantity to remove must be positive"
        
        product = self.products[sku]
        
        if quantity > product.quantity:
            return False, f"Insufficient stock. Available: {product.quantity}, Requested: {quantity}"
        
        product.quantity -= quantity
        product.update_timestamp()
        self._save()
        return True, f"Removed {quantity} units from '{product.name}'. Remaining: {product.quantity}"
    
    # ==================== Search & Filter ====================
    
    def search_by_name(self, query: str) -> List[Product]:
        """Search products by name (case-insensitive partial match)."""
        query_lower = query.lower()
        return [p for p in self.products.values() if query_lower in p.name.lower()]
    
    def search_by_category(self, category: str) -> List[Product]:
        """Filter products by category (case-insensitive)."""
        category_lower = category.lower()
        return [p for p in self.products.values() if p.category.lower() == category_lower]
    
    def search_by_supplier(self, supplier: str) -> List[Product]:
        """Filter products by supplier (case-insensitive partial match)."""
        supplier_lower = supplier.lower()
        return [p for p in self.products.values() if supplier_lower in p.supplier.lower()]
    
    def get_low_stock_products(self) -> List[Product]:
        """Get all products that are at or below their reorder level."""
        return [p for p in self.products.values() if p.is_low_stock()]
    
    def get_out_of_stock_products(self) -> List[Product]:
        """Get all products with zero quantity."""
        return [p for p in self.products.values() if p.quantity == 0]
    
    def get_categories(self) -> List[str]:
        """Get a list of all unique categories."""
        return sorted(set(p.category for p in self.products.values()))
    
    # ==================== Reports ====================
    
    def get_total_inventory_value(self) -> float:
        """Calculate the total value of all inventory."""
        return sum(p.total_value() for p in self.products.values())
    
    def get_inventory_value_by_category(self) -> Dict[str, float]:
        """Calculate inventory value grouped by category."""
        values: Dict[str, float] = {}
        for product in self.products.values():
            if product.category not in values:
                values[product.category] = 0
            values[product.category] += product.total_value()
        return values
    
    def get_product_count(self) -> int:
        """Get the total number of products in inventory."""
        return len(self.products)
    
    def get_total_stock_count(self) -> int:
        """Get the total quantity of all items in stock."""
        return sum(p.quantity for p in self.products.values())
    
    def generate_inventory_report(self) -> str:
        """Generate a comprehensive inventory report."""
        report_lines = [
            "=" * 60,
            "INVENTORY REPORT",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 60,
            "",
            f"Total Products: {self.get_product_count()}",
            f"Total Stock Count: {self.get_total_stock_count()} units",
            f"Total Inventory Value: ${self.get_total_inventory_value():.2f}",
            "",
            "--- Value by Category ---"
        ]
        
        category_values = self.get_inventory_value_by_category()
        for category, value in sorted(category_values.items()):
            report_lines.append(f"  {category}: ${value:.2f}")
        
        low_stock = self.get_low_stock_products()
        if low_stock:
            report_lines.extend([
                "",
                "--- Low Stock Alert ---",
                f"  {len(low_stock)} product(s) at or below reorder level:"
            ])
            for product in low_stock:
                report_lines.append(
                    f"    - {product.name} (SKU: {product.sku}): "
                    f"{product.quantity} units (reorder at {product.reorder_level})"
                )
        
        out_of_stock = self.get_out_of_stock_products()
        if out_of_stock:
            report_lines.extend([
                "",
                "--- Out of Stock ---",
                f"  {len(out_of_stock)} product(s) out of stock:"
            ])
            for product in out_of_stock:
                report_lines.append(f"    - {product.name} (SKU: {product.sku})")
        
        report_lines.append("")
        report_lines.append("=" * 60)
        
        return "\n".join(report_lines)
    
    # ==================== Utility ====================
    
    def _save(self):
        """Save the current inventory state to storage."""
        self.storage.save(self.products)
    
    def backup(self) -> Tuple[bool, str]:
        """Create a backup of the inventory data."""
        if self.storage.backup():
            return True, "Backup created successfully"
        return False, "Failed to create backup"
    
    def clear_all(self) -> Tuple[bool, str]:
        """Clear all products from inventory (use with caution!)."""
        self.products.clear()
        self._save()
        return True, "All products have been removed from inventory"
