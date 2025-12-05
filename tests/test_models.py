"""
Unit tests for the Product model.
"""

import unittest
from datetime import datetime
from inventory_management.models import Product


class TestProduct(unittest.TestCase):
    """Test cases for the Product class."""
    
    def test_create_product_valid(self):
        """Test creating a valid product."""
        product = Product(
            name="Test Product",
            category="Electronics",
            price=99.99,
            quantity=50
        )
        
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.category, "Electronics")
        self.assertEqual(product.price, 99.99)
        self.assertEqual(product.quantity, 50)
        self.assertEqual(product.reorder_level, 10)  # default
        self.assertIsNotNone(product.sku)
        self.assertIsNotNone(product.created_at)
    
    def test_create_product_with_all_fields(self):
        """Test creating a product with all fields specified."""
        product = Product(
            name="Full Product",
            category="Books",
            price=29.99,
            quantity=100,
            sku="BOOK001",
            description="A complete product",
            reorder_level=20,
            supplier="Test Supplier"
        )
        
        self.assertEqual(product.sku, "BOOK001")
        self.assertEqual(product.description, "A complete product")
        self.assertEqual(product.reorder_level, 20)
        self.assertEqual(product.supplier, "Test Supplier")
    
    def test_create_product_negative_price(self):
        """Test that negative price raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Product(
                name="Test",
                category="Test",
                price=-10,
                quantity=5
            )
        self.assertIn("Price cannot be negative", str(context.exception))
    
    def test_create_product_negative_quantity(self):
        """Test that negative quantity raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Product(
                name="Test",
                category="Test",
                price=10,
                quantity=-5
            )
        self.assertIn("Quantity cannot be negative", str(context.exception))
    
    def test_create_product_empty_name(self):
        """Test that empty name raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Product(
                name="",
                category="Test",
                price=10,
                quantity=5
            )
        self.assertIn("Product name cannot be empty", str(context.exception))
    
    def test_create_product_empty_category(self):
        """Test that empty category raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Product(
                name="Test",
                category="",
                price=10,
                quantity=5
            )
        self.assertIn("Category cannot be empty", str(context.exception))
    
    def test_is_low_stock(self):
        """Test low stock detection."""
        product = Product(
            name="Test",
            category="Test",
            price=10,
            quantity=5,
            reorder_level=10
        )
        self.assertTrue(product.is_low_stock())
        
        product.quantity = 15
        self.assertFalse(product.is_low_stock())
        
        product.quantity = 10  # exactly at reorder level
        self.assertTrue(product.is_low_stock())
    
    def test_total_value(self):
        """Test total value calculation."""
        product = Product(
            name="Test",
            category="Test",
            price=25.50,
            quantity=4
        )
        self.assertEqual(product.total_value(), 102.00)
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        product = Product(
            name="Dict Test",
            category="Testing",
            price=50.00,
            quantity=10,
            sku="DICT001"
        )
        
        data = product.to_dict()
        
        self.assertEqual(data["name"], "Dict Test")
        self.assertEqual(data["category"], "Testing")
        self.assertEqual(data["price"], 50.00)
        self.assertEqual(data["quantity"], 10)
        self.assertEqual(data["sku"], "DICT001")
    
    def test_from_dict(self):
        """Test creating product from dictionary."""
        data = {
            "name": "From Dict",
            "category": "Testing",
            "price": 75.00,
            "quantity": 25,
            "sku": "FRMD001",
            "description": "Created from dict",
            "reorder_level": 5,
            "supplier": "Dict Supplier"
        }
        
        product = Product.from_dict(data)
        
        self.assertEqual(product.name, "From Dict")
        self.assertEqual(product.category, "Testing")
        self.assertEqual(product.price, 75.00)
        self.assertEqual(product.quantity, 25)
        self.assertEqual(product.sku, "FRMD001")
        self.assertEqual(product.description, "Created from dict")
        self.assertEqual(product.reorder_level, 5)
        self.assertEqual(product.supplier, "Dict Supplier")
    
    def test_roundtrip_dict(self):
        """Test that to_dict and from_dict are symmetric."""
        original = Product(
            name="Roundtrip",
            category="Testing",
            price=100.00,
            quantity=50,
            description="Roundtrip test",
            reorder_level=15,
            supplier="RT Supplier"
        )
        
        data = original.to_dict()
        restored = Product.from_dict(data)
        
        self.assertEqual(original.name, restored.name)
        self.assertEqual(original.category, restored.category)
        self.assertEqual(original.price, restored.price)
        self.assertEqual(original.quantity, restored.quantity)
        self.assertEqual(original.sku, restored.sku)
        self.assertEqual(original.description, restored.description)
        self.assertEqual(original.reorder_level, restored.reorder_level)
        self.assertEqual(original.supplier, restored.supplier)


if __name__ == "__main__":
    unittest.main()
