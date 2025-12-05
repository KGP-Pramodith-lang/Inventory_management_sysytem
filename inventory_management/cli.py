"""
Command-line interface for the inventory management system.
"""

import sys
from typing import Optional
from .inventory import InventoryManager
from .models import Product


class InventoryCLI:
    """Interactive command-line interface for inventory management."""
    
    def __init__(self, storage_path: str = "inventory_data.json"):
        """Initialize the CLI with an inventory manager."""
        self.manager = InventoryManager(storage_path)
    
    def run(self):
        """Run the main CLI loop."""
        print("\n" + "=" * 50)
        print("  INVENTORY MANAGEMENT SYSTEM")
        print("=" * 50)
        
        while True:
            self._show_menu()
            choice = input("\nEnter your choice (1-12): ").strip()
            
            if choice == "1":
                self._add_product()
            elif choice == "2":
                self._view_all_products()
            elif choice == "3":
                self._view_product()
            elif choice == "4":
                self._update_product()
            elif choice == "5":
                self._delete_product()
            elif choice == "6":
                self._add_stock()
            elif choice == "7":
                self._remove_stock()
            elif choice == "8":
                self._search_products()
            elif choice == "9":
                self._view_low_stock()
            elif choice == "10":
                self._view_report()
            elif choice == "11":
                self._backup_data()
            elif choice == "12":
                print("\nThank you for using the Inventory Management System!")
                print("Goodbye!\n")
                break
            else:
                print("\n[!] Invalid choice. Please try again.")
    
    def _show_menu(self):
        """Display the main menu."""
        print("\n" + "-" * 40)
        print("MAIN MENU")
        print("-" * 40)
        print("1.  Add New Product")
        print("2.  View All Products")
        print("3.  View Product Details")
        print("4.  Update Product")
        print("5.  Delete Product")
        print("6.  Add Stock")
        print("7.  Remove Stock (Sale)")
        print("8.  Search Products")
        print("9.  View Low Stock Items")
        print("10. Generate Inventory Report")
        print("11. Backup Data")
        print("12. Exit")
        print("-" * 40)
    
    def _add_product(self):
        """Handle adding a new product."""
        print("\n--- Add New Product ---")
        
        name = input("Product Name: ").strip()
        if not name:
            print("[!] Product name cannot be empty.")
            return
        
        category = input("Category: ").strip()
        if not category:
            print("[!] Category cannot be empty.")
            return
        
        try:
            price = float(input("Price: $").strip())
            quantity = int(input("Initial Quantity: ").strip())
        except ValueError:
            print("[!] Invalid number format.")
            return
        
        description = input("Description (optional): ").strip()
        
        try:
            reorder_level_input = input("Reorder Level (default: 10): ").strip()
            reorder_level = int(reorder_level_input) if reorder_level_input else 10
        except ValueError:
            reorder_level = 10
        
        supplier = input("Supplier (optional): ").strip()
        
        sku_input = input("Custom SKU (press Enter for auto-generated): ").strip()
        sku = sku_input if sku_input else None
        
        success, message = self.manager.add_product(
            name=name,
            category=category,
            price=price,
            quantity=quantity,
            description=description,
            reorder_level=reorder_level,
            supplier=supplier,
            sku=sku
        )
        
        if success:
            print(f"\n[✓] {message}")
        else:
            print(f"\n[!] {message}")
    
    def _view_all_products(self):
        """Display all products in a table format."""
        products = self.manager.get_all_products()
        
        if not products:
            print("\n[!] No products in inventory.")
            return
        
        print("\n--- All Products ---")
        self._print_product_table(products)
    
    def _view_product(self):
        """View details of a specific product."""
        print("\n--- View Product Details ---")
        
        sku = input("Enter Product SKU: ").strip().upper()
        product = self.manager.get_product(sku)
        
        if not product:
            print(f"\n[!] Product with SKU '{sku}' not found.")
            return
        
        print("\n" + "-" * 40)
        print(f"SKU:           {product.sku}")
        print(f"Name:          {product.name}")
        print(f"Category:      {product.category}")
        print(f"Price:         ${product.price:.2f}")
        print(f"Quantity:      {product.quantity}")
        print(f"Description:   {product.description or 'N/A'}")
        print(f"Reorder Level: {product.reorder_level}")
        print(f"Supplier:      {product.supplier or 'N/A'}")
        print(f"Created:       {product.created_at}")
        print(f"Last Updated:  {product.updated_at}")
        print(f"Total Value:   ${product.total_value():.2f}")
        print(f"Stock Status:  {'LOW STOCK!' if product.is_low_stock() else 'OK'}")
        print("-" * 40)
    
    def _update_product(self):
        """Update an existing product."""
        print("\n--- Update Product ---")
        
        sku = input("Enter Product SKU to update: ").strip().upper()
        product = self.manager.get_product(sku)
        
        if not product:
            print(f"\n[!] Product with SKU '{sku}' not found.")
            return
        
        print(f"\nCurrent product: {product.name}")
        print("(Press Enter to keep current value)\n")
        
        name = input(f"Name [{product.name}]: ").strip() or None
        category = input(f"Category [{product.category}]: ").strip() or None
        
        try:
            price_input = input(f"Price [${product.price:.2f}]: $").strip()
            price = float(price_input) if price_input else None
            
            qty_input = input(f"Quantity [{product.quantity}]: ").strip()
            quantity = int(qty_input) if qty_input else None
            
            desc_input = input(f"Description [{product.description or 'N/A'}]: ").strip()
            description = desc_input if desc_input else None
            
            reorder_input = input(f"Reorder Level [{product.reorder_level}]: ").strip()
            reorder_level = int(reorder_input) if reorder_input else None
        except ValueError:
            print("\n[!] Invalid number format. Update cancelled.")
            return
        
        supplier_input = input(f"Supplier [{product.supplier or 'N/A'}]: ").strip()
        supplier = supplier_input if supplier_input else None
        
        success, message = self.manager.update_product(
            sku=sku,
            name=name,
            category=category,
            price=price,
            quantity=quantity,
            description=description,
            reorder_level=reorder_level,
            supplier=supplier
        )
        
        if success:
            print(f"\n[✓] {message}")
        else:
            print(f"\n[!] {message}")
    
    def _delete_product(self):
        """Delete a product from inventory."""
        print("\n--- Delete Product ---")
        
        sku = input("Enter Product SKU to delete: ").strip().upper()
        product = self.manager.get_product(sku)
        
        if not product:
            print(f"\n[!] Product with SKU '{sku}' not found.")
            return
        
        confirm = input(f"Are you sure you want to delete '{product.name}'? (yes/no): ").strip().lower()
        
        if confirm == "yes":
            success, message = self.manager.delete_product(sku)
            if success:
                print(f"\n[✓] {message}")
            else:
                print(f"\n[!] {message}")
        else:
            print("\n[i] Deletion cancelled.")
    
    def _add_stock(self):
        """Add stock to a product."""
        print("\n--- Add Stock ---")
        
        sku = input("Enter Product SKU: ").strip().upper()
        product = self.manager.get_product(sku)
        
        if not product:
            print(f"\n[!] Product with SKU '{sku}' not found.")
            return
        
        print(f"Current stock for '{product.name}': {product.quantity}")
        
        try:
            quantity = int(input("Quantity to add: ").strip())
        except ValueError:
            print("[!] Invalid quantity.")
            return
        
        success, message = self.manager.add_stock(sku, quantity)
        
        if success:
            print(f"\n[✓] {message}")
        else:
            print(f"\n[!] {message}")
    
    def _remove_stock(self):
        """Remove stock from a product (for sales)."""
        print("\n--- Remove Stock (Sale) ---")
        
        sku = input("Enter Product SKU: ").strip().upper()
        product = self.manager.get_product(sku)
        
        if not product:
            print(f"\n[!] Product with SKU '{sku}' not found.")
            return
        
        print(f"Current stock for '{product.name}': {product.quantity}")
        
        try:
            quantity = int(input("Quantity to remove: ").strip())
        except ValueError:
            print("[!] Invalid quantity.")
            return
        
        success, message = self.manager.remove_stock(sku, quantity)
        
        if success:
            print(f"\n[✓] {message}")
        else:
            print(f"\n[!] {message}")
    
    def _search_products(self):
        """Search for products."""
        print("\n--- Search Products ---")
        print("1. Search by Name")
        print("2. Search by Category")
        print("3. Search by Supplier")
        
        choice = input("\nSearch option (1-3): ").strip()
        
        if choice == "1":
            query = input("Enter name to search: ").strip()
            results = self.manager.search_by_name(query)
        elif choice == "2":
            categories = self.manager.get_categories()
            if categories:
                print(f"Available categories: {', '.join(categories)}")
            query = input("Enter category: ").strip()
            results = self.manager.search_by_category(query)
        elif choice == "3":
            query = input("Enter supplier name: ").strip()
            results = self.manager.search_by_supplier(query)
        else:
            print("[!] Invalid search option.")
            return
        
        if results:
            print(f"\nFound {len(results)} product(s):")
            self._print_product_table(results)
        else:
            print("\n[i] No products found matching your search.")
    
    def _view_low_stock(self):
        """View products with low stock."""
        print("\n--- Low Stock Items ---")
        
        low_stock = self.manager.get_low_stock_products()
        
        if not low_stock:
            print("[✓] No products are low on stock.")
            return
        
        print(f"[!] {len(low_stock)} product(s) at or below reorder level:\n")
        self._print_product_table(low_stock)
    
    def _view_report(self):
        """Display the inventory report."""
        print("\n" + self.manager.generate_inventory_report())
    
    def _backup_data(self):
        """Create a backup of inventory data."""
        print("\n--- Backup Data ---")
        
        success, message = self.manager.backup()
        
        if success:
            print(f"[✓] {message}")
        else:
            print(f"[!] {message}")
    
    def _print_product_table(self, products: list):
        """Print products in a formatted table."""
        if not products:
            return
        
        # Header
        print("-" * 90)
        print(f"{'SKU':<10} {'Name':<25} {'Category':<15} {'Price':>10} {'Qty':>8} {'Value':>12} {'Status':<8}")
        print("-" * 90)
        
        # Rows
        for p in products:
            status = "LOW" if p.is_low_stock() else "OK"
            print(f"{p.sku:<10} {p.name[:24]:<25} {p.category[:14]:<15} "
                  f"${p.price:>9.2f} {p.quantity:>8} ${p.total_value():>11.2f} {status:<8}")
        
        print("-" * 90)
        print(f"Total: {len(products)} products")


def main():
    """Entry point for the CLI application."""
    storage_path = "inventory_data.json"
    
    # Check for custom storage path in command line args
    if len(sys.argv) > 1:
        storage_path = sys.argv[1]
    
    cli = InventoryCLI(storage_path)
    cli.run()


if __name__ == "__main__":
    main()
