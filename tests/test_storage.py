"""
Unit tests for the InventoryStorage class.
"""

import json
import os
import tempfile
import unittest
from inventory_management.storage import InventoryStorage
from inventory_management.models import Product


class TestInventoryStorage(unittest.TestCase):
    """Test cases for the InventoryStorage class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_file = tempfile.NamedTemporaryFile(
            mode='w', suffix='.json', delete=False
        )
        self.temp_file.close()
        self.storage = InventoryStorage(self.temp_file.name)
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
        backup_file = self.temp_file.name + ".backup"
        if os.path.exists(backup_file):
            os.unlink(backup_file)
    
    def test_save_and_load(self):
        """Test saving and loading products."""
        products = {
            "SKU001": Product(
                name="Test Product",
                category="Electronics",
                price=99.99,
                quantity=50,
                sku="SKU001"
            )
        }
        
        # Save
        result = self.storage.save(products)
        self.assertTrue(result)
        
        # Load
        loaded = self.storage.load()
        self.assertEqual(len(loaded), 1)
        self.assertIn("SKU001", loaded)
        self.assertEqual(loaded["SKU001"].name, "Test Product")
    
    def test_load_empty_file(self):
        """Test loading from non-existent file."""
        storage = InventoryStorage("nonexistent.json")
        loaded = storage.load()
        self.assertEqual(loaded, {})
    
    def test_load_corrupted_file(self):
        """Test loading from corrupted JSON file."""
        with open(self.temp_file.name, 'w') as f:
            f.write("not valid json{{{")
        
        loaded = self.storage.load()
        self.assertEqual(loaded, {})
    
    def test_backup(self):
        """Test creating backup file."""
        products = {
            "SKU001": Product(
                name="Backup Test",
                category="Test",
                price=100,
                quantity=10,
                sku="SKU001"
            )
        }
        
        self.storage.save(products)
        result = self.storage.backup()
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.temp_file.name + ".backup"))
    
    def test_file_exists(self):
        """Test file_exists method."""
        # File exists after save
        products = {
            "SKU001": Product(
                name="Test",
                category="Test",
                price=10,
                quantity=1,
                sku="SKU001"
            )
        }
        self.storage.save(products)
        
        self.assertTrue(self.storage.file_exists())
        
        # File doesn't exist
        storage = InventoryStorage("definitely_not_a_file.json")
        self.assertFalse(storage.file_exists())
    
    def test_save_multiple_products(self):
        """Test saving multiple products."""
        products = {
            "SKU001": Product("Product 1", "Cat1", 100, 10, sku="SKU001"),
            "SKU002": Product("Product 2", "Cat1", 200, 20, sku="SKU002"),
            "SKU003": Product("Product 3", "Cat2", 300, 30, sku="SKU003")
        }
        
        result = self.storage.save(products)
        self.assertTrue(result)
        
        loaded = self.storage.load()
        self.assertEqual(len(loaded), 3)
        self.assertEqual(loaded["SKU002"].price, 200)


if __name__ == "__main__":
    unittest.main()
