"""
Storage module for persisting inventory data to JSON files.
"""

import json
import os
from typing import Dict, List, Optional
from .models import Product


class InventoryStorage:
    """Handles reading and writing inventory data to JSON files."""
    
    def __init__(self, filepath: str = "inventory_data.json"):
        """Initialize the storage with a file path."""
        self.filepath = filepath
    
    def save(self, products: Dict[str, Product]) -> bool:
        """
        Save products to the JSON file.
        
        Args:
            products: Dictionary mapping SKU to Product objects
            
        Returns:
            True if save was successful, False otherwise
        """
        try:
            data = {
                "products": [product.to_dict() for product in products.values()]
            }
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except (IOError, OSError) as e:
            print(f"Error saving inventory data: {e}")
            return False
    
    def load(self) -> Dict[str, Product]:
        """
        Load products from the JSON file.
        
        Returns:
            Dictionary mapping SKU to Product objects
        """
        if not os.path.exists(self.filepath):
            return {}
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return {}
                data = json.loads(content)
            
            products = {}
            for product_data in data.get("products", []):
                product = Product.from_dict(product_data)
                products[product.sku] = product
            return products
        except (IOError, OSError, json.JSONDecodeError) as e:
            print(f"Error loading inventory data: {e}")
            return {}
    
    def backup(self, backup_suffix: str = ".backup") -> bool:
        """
        Create a backup of the inventory file.
        
        Args:
            backup_suffix: Suffix to append to backup filename
            
        Returns:
            True if backup was successful, False otherwise
        """
        if not os.path.exists(self.filepath):
            return False
        
        try:
            backup_path = self.filepath + backup_suffix
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = f.read()
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(data)
            return True
        except (IOError, OSError) as e:
            print(f"Error creating backup: {e}")
            return False
    
    def file_exists(self) -> bool:
        """Check if the inventory file exists."""
        return os.path.exists(self.filepath)
