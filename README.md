# Inventory Management System

A simple inventory management system made for our Cost & Management Accounting course.

## Features

- **Dual Interface**: Both GUI (Graphical) and CLI (Command-line) interfaces available
- **Product Management**: Add, update, delete, and view products in your inventory
- **Stock Tracking**: Track quantities, add/remove stock, monitor stock levels
- **Search & Filter**: Search products by name, category, or supplier
- **Low Stock Alerts**: Automatic detection of products below reorder levels
- **Reports**: Generate comprehensive inventory reports including:
  - Total inventory value
  - Value breakdown by category
  - Low stock alerts
  - Out of stock items
- **Data Persistence**: All data is saved to a JSON file for easy backup and portability
- **Backup**: Create backups of your inventory data

## Requirements

- Python 3.7 or higher
- tkinter (for GUI - usually included with Python, or install via `python3-tk` on Linux)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/KGP-Pramodith-lang/Inventory_management_sysytem.git
cd Inventory_management_sysytem
```

2. On Linux, ensure tkinter is installed (for GUI):
```bash
sudo apt-get install python3-tk
```

3. Run the application:
```bash
# Launch GUI (default)
python main.py

# Or explicitly launch GUI
python main.py --gui

# Or launch CLI
python main.py --cli
```

## Usage

### Graphical User Interface (GUI)

Run the GUI application:

```bash
python main.py
# or
python main.py --gui
```

The GUI provides a tabbed interface with the following sections:

![Inventory Management GUI](https://github.com/user-attachments/assets/d41c1012-51c9-4e00-8c8c-29ee632a9ae9)

**GUI Features:**
- **All Products Tab**: View all inventory items in a table with refresh, view details, update, and delete functions
- **Add Product Tab**: Form to add new products with all necessary fields
- **Stock Management Tab**: Separate sections to add or remove stock from products
- **Search Tab**: Search products by name, category, or supplier
- **Reports Tab**: Generate comprehensive inventory reports and view low stock items
- **Menu Bar**: File operations (backup, exit), view options, and help

### Command Line Interface (CLI)

Run the interactive CLI:

```bash
python main.py --cli
```

You can also specify a custom storage file:

```bash
python main.py --cli my_inventory.json
```

### Menu Options (CLI)

1. **Add New Product** - Add products with name, category, price, quantity, and more
2. **View All Products** - Display all products in a table format
3. **View Product Details** - Get detailed information about a specific product
4. **Update Product** - Modify product information
5. **Delete Product** - Remove a product from inventory
6. **Add Stock** - Increase stock quantity for a product
7. **Remove Stock (Sale)** - Decrease stock quantity (for sales transactions)
8. **Search Products** - Search by name, category, or supplier
9. **View Low Stock Items** - See products that need reordering
10. **Generate Inventory Report** - Get a comprehensive inventory summary
11. **Backup Data** - Create a backup of your inventory data
12. **Exit** - Close the application

### Using as a Library

You can also use the inventory management system programmatically:

```python
from inventory_management.inventory import InventoryManager

# Create manager instance
manager = InventoryManager("my_inventory.json")

# Add a product
success, message = manager.add_product(
    name="Widget",
    category="Electronics",
    price=29.99,
    quantity=100,
    description="A useful widget",
    reorder_level=20,
    supplier="Widget Co."
)

# Search for products
results = manager.search_by_name("Widget")

# Add stock
manager.add_stock("WIDGET01", 50)

# Remove stock (sale)
manager.remove_stock("WIDGET01", 10)

# Get inventory report
report = manager.generate_inventory_report()
print(report)

# Get total inventory value
total_value = manager.get_total_inventory_value()
```

### Using the GUI Programmatically

```python
from inventory_management.gui import InventoryGUI

# Create and run GUI
app = InventoryGUI("my_inventory.json")
app.run()
```

## Project Structure

```
Inventory_management_sysytem/
├── main.py                      # Entry point (supports --gui and --cli flags)
├── inventory_management/        # Main package
│   ├── __init__.py
│   ├── models.py               # Product data model
│   ├── storage.py              # JSON file storage
│   ├── inventory.py            # Core inventory operations
│   ├── cli.py                  # Command-line interface
│   └── gui.py                  # Graphical user interface (NEW)
├── tests/                      # Unit tests
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_storage.py
│   └── test_inventory.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Running Tests

Run all tests:

```bash
python -m unittest discover tests
```

Run specific test file:

```bash
python -m unittest tests.test_models
python -m unittest tests.test_inventory
python -m unittest tests.test_storage
```

## Data Storage

Inventory data is stored in a JSON file (default: `inventory_data.json`). The file format is:

```json
{
  "products": [
    {
      "sku": "ABC12345",
      "name": "Product Name",
      "category": "Category",
      "price": 99.99,
      "quantity": 50,
      "description": "Product description",
      "reorder_level": 10,
      "supplier": "Supplier Name",
      "created_at": "2024-01-01T12:00:00",
      "updated_at": "2024-01-01T12:00:00"
    }
  ]
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
