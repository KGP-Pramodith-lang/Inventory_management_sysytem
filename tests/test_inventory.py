"""
Unit tests for the InventoryManager class.
"""

import os
import tempfile
import unittest
from inventory_management.inventory import InventoryManager


class TestInventoryManager(unittest.TestCase):
    """Test cases for the InventoryManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(
            mode='w', suffix='.json', delete=False
        )
        self.temp_file.close()
        self.manager = InventoryManager(self.temp_file.name)
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
        backup_file = self.temp_file.name + ".backup"
        if os.path.exists(backup_file):
            os.unlink(backup_file)
    
    # ==================== Add Product Tests ====================
    
    def test_add_product_success(self):
        """Test adding a valid product."""
        success, message = self.manager.add_product(
            name="Test Product",
            category="Electronics",
            price=99.99,
            quantity=50
        )
        
        self.assertTrue(success)
        self.assertIn("added", message.lower())
        self.assertEqual(self.manager.get_product_count(), 1)
    
    def test_add_product_with_custom_sku(self):
        """Test adding a product with custom SKU."""
        success, message = self.manager.add_product(
            name="Custom SKU Product",
            category="Electronics",
            price=149.99,
            quantity=30,
            sku="CUSTOM001"
        )
        
        self.assertTrue(success)
        product = self.manager.get_product("CUSTOM001")
        self.assertIsNotNone(product)
        self.assertEqual(product.name, "Custom SKU Product")
    
    def test_add_product_duplicate_sku(self):
        """Test that duplicate SKU is rejected."""
        self.manager.add_product(
            name="First Product",
            category="Electronics",
            price=99.99,
            quantity=50,
            sku="DUP001"
        )
        
        success, message = self.manager.add_product(
            name="Second Product",
            category="Electronics",
            price=149.99,
            quantity=30,
            sku="DUP001"
        )
        
        self.assertFalse(success)
        self.assertIn("already exists", message.lower())
    
    def test_add_product_invalid_price(self):
        """Test that negative price is rejected."""
        success, message = self.manager.add_product(
            name="Bad Price",
            category="Electronics",
            price=-10,
            quantity=50
        )
        
        self.assertFalse(success)
        self.assertIn("negative", message.lower())
    
    # ==================== Update Product Tests ====================
    
    def test_update_product_success(self):
        """Test updating a product."""
        self.manager.add_product(
            name="Original",
            category="Electronics",
            price=100,
            quantity=50,
            sku="UPD001"
        )
        
        success, message = self.manager.update_product(
            sku="UPD001",
            name="Updated Name",
            price=150
        )
        
        self.assertTrue(success)
        product = self.manager.get_product("UPD001")
        self.assertEqual(product.name, "Updated Name")
        self.assertEqual(product.price, 150)
        self.assertEqual(product.quantity, 50)  # unchanged
    
    def test_update_product_not_found(self):
        """Test updating non-existent product."""
        success, message = self.manager.update_product(
            sku="NONEXISTENT",
            name="New Name"
        )
        
        self.assertFalse(success)
        self.assertIn("not found", message.lower())
    
    def test_update_product_invalid_values(self):
        """Test that invalid updates are rejected."""
        self.manager.add_product(
            name="Original",
            category="Electronics",
            price=100,
            quantity=50,
            sku="UPD002"
        )
        
        success, message = self.manager.update_product(
            sku="UPD002",
            price=-50
        )
        
        self.assertFalse(success)
        self.assertIn("negative", message.lower())
    
    # ==================== Delete Product Tests ====================
    
    def test_delete_product_success(self):
        """Test deleting a product."""
        self.manager.add_product(
            name="To Delete",
            category="Electronics",
            price=100,
            quantity=50,
            sku="DEL001"
        )
        
        success, message = self.manager.delete_product("DEL001")
        
        self.assertTrue(success)
        self.assertIsNone(self.manager.get_product("DEL001"))
        self.assertEqual(self.manager.get_product_count(), 0)
    
    def test_delete_product_not_found(self):
        """Test deleting non-existent product."""
        success, message = self.manager.delete_product("NONEXISTENT")
        
        self.assertFalse(success)
        self.assertIn("not found", message.lower())
    
    # ==================== Stock Management Tests ====================
    
    def test_add_stock_success(self):
        """Test adding stock."""
        self.manager.add_product(
            name="Stock Test",
            category="Electronics",
            price=100,
            quantity=50,
            sku="STK001"
        )
        
        success, message = self.manager.add_stock("STK001", 25)
        
        self.assertTrue(success)
        product = self.manager.get_product("STK001")
        self.assertEqual(product.quantity, 75)
    
    def test_add_stock_invalid_quantity(self):
        """Test adding zero or negative stock."""
        self.manager.add_product(
            name="Stock Test",
            category="Electronics",
            price=100,
            quantity=50,
            sku="STK002"
        )
        
        success, message = self.manager.add_stock("STK002", 0)
        self.assertFalse(success)
        
        success, message = self.manager.add_stock("STK002", -10)
        self.assertFalse(success)
    
    def test_remove_stock_success(self):
        """Test removing stock."""
        self.manager.add_product(
            name="Stock Test",
            category="Electronics",
            price=100,
            quantity=50,
            sku="STK003"
        )
        
        success, message = self.manager.remove_stock("STK003", 20)
        
        self.assertTrue(success)
        product = self.manager.get_product("STK003")
        self.assertEqual(product.quantity, 30)
    
    def test_remove_stock_insufficient(self):
        """Test removing more stock than available."""
        self.manager.add_product(
            name="Stock Test",
            category="Electronics",
            price=100,
            quantity=50,
            sku="STK004"
        )
        
        success, message = self.manager.remove_stock("STK004", 100)
        
        self.assertFalse(success)
        self.assertIn("insufficient", message.lower())
        
        # Quantity should be unchanged
        product = self.manager.get_product("STK004")
        self.assertEqual(product.quantity, 50)
    
    # ==================== Search Tests ====================
    
    def test_search_by_name(self):
        """Test searching products by name."""
        self.manager.add_product("Apple iPhone", "Electronics", 999, 10)
        self.manager.add_product("Samsung Galaxy", "Electronics", 899, 15)
        self.manager.add_product("Apple MacBook", "Computers", 1999, 5)
        
        results = self.manager.search_by_name("Apple")
        
        self.assertEqual(len(results), 2)
        names = [p.name for p in results]
        self.assertIn("Apple iPhone", names)
        self.assertIn("Apple MacBook", names)
    
    def test_search_by_category(self):
        """Test filtering products by category."""
        self.manager.add_product("iPhone", "Electronics", 999, 10)
        self.manager.add_product("Galaxy", "Electronics", 899, 15)
        self.manager.add_product("MacBook", "Computers", 1999, 5)
        
        results = self.manager.search_by_category("Electronics")
        
        self.assertEqual(len(results), 2)
    
    def test_get_low_stock_products(self):
        """Test getting low stock products."""
        self.manager.add_product(
            name="Low Stock",
            category="Test",
            price=10,
            quantity=5,
            reorder_level=10
        )
        self.manager.add_product(
            name="Normal Stock",
            category="Test",
            price=10,
            quantity=50,
            reorder_level=10
        )
        
        low_stock = self.manager.get_low_stock_products()
        
        self.assertEqual(len(low_stock), 1)
        self.assertEqual(low_stock[0].name, "Low Stock")
    
    # ==================== Report Tests ====================
    
    def test_get_total_inventory_value(self):
        """Test calculating total inventory value."""
        self.manager.add_product("Product A", "Test", 100, 10)  # $1000
        self.manager.add_product("Product B", "Test", 50, 20)   # $1000
        
        total_value = self.manager.get_total_inventory_value()
        
        self.assertEqual(total_value, 2000)
    
    def test_get_inventory_value_by_category(self):
        """Test inventory value by category."""
        self.manager.add_product("Phone", "Electronics", 500, 10)  # $5000
        self.manager.add_product("Laptop", "Electronics", 1000, 5)  # $5000
        self.manager.add_product("Desk", "Furniture", 300, 3)      # $900
        
        values = self.manager.get_inventory_value_by_category()
        
        self.assertEqual(values["Electronics"], 10000)
        self.assertEqual(values["Furniture"], 900)
    
    def test_generate_inventory_report(self):
        """Test generating inventory report."""
        self.manager.add_product("Test Product", "Test", 100, 50)
        
        report = self.manager.generate_inventory_report()
        
        self.assertIn("INVENTORY REPORT", report)
        self.assertIn("Total Products: 1", report)
        self.assertIn("Total Stock Count: 50", report)
    
    # ==================== Persistence Tests ====================
    
    def test_data_persistence(self):
        """Test that data persists across manager instances."""
        # Add products with first manager
        self.manager.add_product(
            name="Persistent Product",
            category="Test",
            price=100,
            quantity=25,
            sku="PERS001"
        )
        
        # Create new manager with same file
        new_manager = InventoryManager(self.temp_file.name)
        
        # Verify data loaded
        product = new_manager.get_product("PERS001")
        self.assertIsNotNone(product)
        self.assertEqual(product.name, "Persistent Product")
        self.assertEqual(product.quantity, 25)
    
    def test_backup(self):
        """Test creating backup."""
        self.manager.add_product("Backup Test", "Test", 100, 50)
        
        success, message = self.manager.backup()
        
        self.assertTrue(success)
        self.assertTrue(os.path.exists(self.temp_file.name + ".backup"))


if __name__ == "__main__":
    unittest.main()
