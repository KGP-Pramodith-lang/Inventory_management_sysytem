"""
Graphical User Interface for the inventory management system using tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Optional
from .inventory import InventoryManager
from .models import Product


class InventoryGUI:
    """Tkinter-based GUI for inventory management."""
    
    def __init__(self, storage_path: str = "inventory_data.json"):
        """Initialize the GUI with an inventory manager."""
        self.manager = InventoryManager(storage_path)
        self.root = tk.Tk()
        self.root.title("Inventory Management System")
        self.root.geometry("1200x700")
        
        # Create main container
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface."""
        # Create menu bar
        self.create_menu_bar()
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_products_tab()
        self.create_add_product_tab()
        self.create_stock_management_tab()
        self.create_search_tab()
        self.create_reports_tab()
        
    def create_menu_bar(self):
        """Create the menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Backup Data", command=self.backup_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Refresh All", command=self.refresh_all)
        view_menu.add_command(label="Low Stock Items", command=self.show_low_stock)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_products_tab(self):
        """Create the products listing tab."""
        products_frame = ttk.Frame(self.notebook)
        self.notebook.add(products_frame, text="All Products")
        
        # Top frame with buttons
        top_frame = ttk.Frame(products_frame)
        top_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(top_frame, text="Refresh", command=self.refresh_products_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="View Details", command=self.view_product_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Update Product", command=self.update_product_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Delete Product", command=self.delete_product).pack(side=tk.LEFT, padx=5)
        
        # Create treeview for products
        columns = ("SKU", "Name", "Category", "Price", "Quantity", "Value", "Status")
        self.products_tree = ttk.Treeview(products_frame, columns=columns, show="headings", height=20)
        
        # Configure columns
        self.products_tree.heading("SKU", text="SKU")
        self.products_tree.heading("Name", text="Name")
        self.products_tree.heading("Category", text="Category")
        self.products_tree.heading("Price", text="Price ($)")
        self.products_tree.heading("Quantity", text="Quantity")
        self.products_tree.heading("Value", text="Total Value ($)")
        self.products_tree.heading("Status", text="Status")
        
        self.products_tree.column("SKU", width=100)
        self.products_tree.column("Name", width=200)
        self.products_tree.column("Category", width=120)
        self.products_tree.column("Price", width=100)
        self.products_tree.column("Quantity", width=100)
        self.products_tree.column("Value", width=120)
        self.products_tree.column("Status", width=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(products_frame, orient=tk.VERTICAL, command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=scrollbar.set)
        
        self.products_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Populate the tree
        self.refresh_products_list()
    
    def create_add_product_tab(self):
        """Create the add product tab."""
        add_frame = ttk.Frame(self.notebook)
        self.notebook.add(add_frame, text="Add Product")
        
        # Create form
        form_frame = ttk.LabelFrame(add_frame, text="Product Information", padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Name
        ttk.Label(form_frame, text="Product Name:*").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.add_name_entry = ttk.Entry(form_frame, width=40)
        self.add_name_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # Category
        ttk.Label(form_frame, text="Category:*").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.add_category_entry = ttk.Entry(form_frame, width=40)
        self.add_category_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Price
        ttk.Label(form_frame, text="Price ($):*").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.add_price_entry = ttk.Entry(form_frame, width=40)
        self.add_price_entry.grid(row=2, column=1, pady=5, padx=10)
        
        # Quantity
        ttk.Label(form_frame, text="Initial Quantity:*").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.add_quantity_entry = ttk.Entry(form_frame, width=40)
        self.add_quantity_entry.grid(row=3, column=1, pady=5, padx=10)
        
        # Description
        ttk.Label(form_frame, text="Description:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.add_description_entry = ttk.Entry(form_frame, width=40)
        self.add_description_entry.grid(row=4, column=1, pady=5, padx=10)
        
        # Reorder Level
        ttk.Label(form_frame, text="Reorder Level:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.add_reorder_entry = ttk.Entry(form_frame, width=40)
        self.add_reorder_entry.insert(0, "10")
        self.add_reorder_entry.grid(row=5, column=1, pady=5, padx=10)
        
        # Supplier
        ttk.Label(form_frame, text="Supplier:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.add_supplier_entry = ttk.Entry(form_frame, width=40)
        self.add_supplier_entry.grid(row=6, column=1, pady=5, padx=10)
        
        # SKU (optional)
        ttk.Label(form_frame, text="Custom SKU:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.add_sku_entry = ttk.Entry(form_frame, width=40)
        self.add_sku_entry.grid(row=7, column=1, pady=5, padx=10)
        ttk.Label(form_frame, text="(Leave blank for auto-generated)", font=("Arial", 8, "italic")).grid(
            row=8, column=1, sticky=tk.W, padx=10
        )
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=9, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Add Product", command=self.add_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_add_form).pack(side=tk.LEFT, padx=5)
    
    def create_stock_management_tab(self):
        """Create the stock management tab."""
        stock_frame = ttk.Frame(self.notebook)
        self.notebook.add(stock_frame, text="Stock Management")
        
        # Create two sections: Add Stock and Remove Stock
        add_stock_frame = ttk.LabelFrame(stock_frame, text="Add Stock", padding=20)
        add_stock_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Add Stock section
        ttk.Label(add_stock_frame, text="Product SKU:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.add_stock_sku_entry = ttk.Entry(add_stock_frame, width=30)
        self.add_stock_sku_entry.grid(row=0, column=1, pady=5, padx=10)
        
        ttk.Label(add_stock_frame, text="Quantity to Add:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.add_stock_qty_entry = ttk.Entry(add_stock_frame, width=30)
        self.add_stock_qty_entry.grid(row=1, column=1, pady=5, padx=10)
        
        ttk.Button(add_stock_frame, text="Add Stock", command=self.add_stock).grid(
            row=2, column=0, columnspan=2, pady=10
        )
        
        # Remove Stock section
        remove_stock_frame = ttk.LabelFrame(stock_frame, text="Remove Stock (Sale)", padding=20)
        remove_stock_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(remove_stock_frame, text="Product SKU:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.remove_stock_sku_entry = ttk.Entry(remove_stock_frame, width=30)
        self.remove_stock_sku_entry.grid(row=0, column=1, pady=5, padx=10)
        
        ttk.Label(remove_stock_frame, text="Quantity to Remove:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.remove_stock_qty_entry = ttk.Entry(remove_stock_frame, width=30)
        self.remove_stock_qty_entry.grid(row=1, column=1, pady=5, padx=10)
        
        ttk.Button(remove_stock_frame, text="Remove Stock", command=self.remove_stock).grid(
            row=2, column=0, columnspan=2, pady=10
        )
    
    def create_search_tab(self):
        """Create the search tab."""
        search_frame = ttk.Frame(self.notebook)
        self.notebook.add(search_frame, text="Search")
        
        # Search controls
        control_frame = ttk.LabelFrame(search_frame, text="Search Options", padding=10)
        control_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(control_frame, text="Search By:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.search_type = tk.StringVar(value="name")
        ttk.Radiobutton(control_frame, text="Name", variable=self.search_type, value="name").grid(
            row=0, column=1, sticky=tk.W, padx=5
        )
        ttk.Radiobutton(control_frame, text="Category", variable=self.search_type, value="category").grid(
            row=0, column=2, sticky=tk.W, padx=5
        )
        ttk.Radiobutton(control_frame, text="Supplier", variable=self.search_type, value="supplier").grid(
            row=0, column=3, sticky=tk.W, padx=5
        )
        
        ttk.Label(control_frame, text="Search Term:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.search_entry = ttk.Entry(control_frame, width=50)
        self.search_entry.grid(row=1, column=1, columnspan=2, pady=5, padx=5)
        
        ttk.Button(control_frame, text="Search", command=self.search_products).grid(
            row=1, column=3, padx=5
        )
        
        # Results treeview
        results_frame = ttk.LabelFrame(search_frame, text="Search Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ("SKU", "Name", "Category", "Price", "Quantity", "Supplier")
        self.search_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=15)
        
        self.search_tree.heading("SKU", text="SKU")
        self.search_tree.heading("Name", text="Name")
        self.search_tree.heading("Category", text="Category")
        self.search_tree.heading("Price", text="Price ($)")
        self.search_tree.heading("Quantity", text="Quantity")
        self.search_tree.heading("Supplier", text="Supplier")
        
        self.search_tree.column("SKU", width=100)
        self.search_tree.column("Name", width=200)
        self.search_tree.column("Category", width=120)
        self.search_tree.column("Price", width=100)
        self.search_tree.column("Quantity", width=100)
        self.search_tree.column("Supplier", width=150)
        
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.search_tree.yview)
        self.search_tree.configure(yscrollcommand=scrollbar.set)
        
        self.search_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_reports_tab(self):
        """Create the reports tab."""
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="Reports")
        
        # Buttons frame
        button_frame = ttk.Frame(reports_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Generate Full Report", command=self.generate_report).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(button_frame, text="View Low Stock", command=self.show_low_stock_in_report).pack(
            side=tk.LEFT, padx=5
        )
        
        # Text area for report
        self.report_text = scrolledtext.ScrolledText(reports_frame, wrap=tk.WORD, width=100, height=30)
        self.report_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Action methods
    
    def refresh_products_list(self):
        """Refresh the products list in the treeview."""
        # Clear existing items
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # Get all products and populate
        products = self.manager.get_all_products()
        for product in products:
            status = "LOW" if product.is_low_stock() else "OK"
            self.products_tree.insert("", tk.END, values=(
                product.sku,
                product.name,
                product.category,
                f"{product.price:.2f}",
                product.quantity,
                f"{product.total_value():.2f}",
                status
            ))
    
    def add_product(self):
        """Add a new product."""
        try:
            name = self.add_name_entry.get().strip()
            category = self.add_category_entry.get().strip()
            price = float(self.add_price_entry.get().strip())
            quantity = int(self.add_quantity_entry.get().strip())
            description = self.add_description_entry.get().strip()
            reorder_level = int(self.add_reorder_entry.get().strip() or "10")
            supplier = self.add_supplier_entry.get().strip()
            sku = self.add_sku_entry.get().strip() or None
            
            if not name or not category:
                messagebox.showerror("Error", "Name and Category are required!")
                return
            
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
                messagebox.showinfo("Success", message)
                self.clear_add_form()
                self.refresh_products_list()
            else:
                messagebox.showerror("Error", message)
                
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
    
    def clear_add_form(self):
        """Clear the add product form."""
        self.add_name_entry.delete(0, tk.END)
        self.add_category_entry.delete(0, tk.END)
        self.add_price_entry.delete(0, tk.END)
        self.add_quantity_entry.delete(0, tk.END)
        self.add_description_entry.delete(0, tk.END)
        self.add_reorder_entry.delete(0, tk.END)
        self.add_reorder_entry.insert(0, "10")
        self.add_supplier_entry.delete(0, tk.END)
        self.add_sku_entry.delete(0, tk.END)
    
    def view_product_details(self):
        """View detailed information about selected product."""
        selection = self.products_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a product first!")
            return
        
        item = self.products_tree.item(selection[0])
        sku = item['values'][0]
        product = self.manager.get_product(sku)
        
        if product:
            details = f"""
Product Details
{'='*50}

SKU:           {product.sku}
Name:          {product.name}
Category:      {product.category}
Price:         ${product.price:.2f}
Quantity:      {product.quantity}
Description:   {product.description or 'N/A'}
Reorder Level: {product.reorder_level}
Supplier:      {product.supplier or 'N/A'}
Created:       {product.created_at}
Last Updated:  {product.updated_at}
Total Value:   ${product.total_value():.2f}
Stock Status:  {'LOW STOCK!' if product.is_low_stock() else 'OK'}
"""
            messagebox.showinfo("Product Details", details)
    
    def update_product_dialog(self):
        """Open dialog to update selected product."""
        selection = self.products_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a product first!")
            return
        
        item = self.products_tree.item(selection[0])
        sku = item['values'][0]
        product = self.manager.get_product(sku)
        
        if not product:
            messagebox.showerror("Error", "Product not found!")
            return
        
        # Create update dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Update Product - {product.name}")
        dialog.geometry("500x400")
        
        # Create form
        ttk.Label(dialog, text="Name:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.insert(0, product.name)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Category:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        category_entry = ttk.Entry(dialog, width=40)
        category_entry.insert(0, product.category)
        category_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Price ($):").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        price_entry = ttk.Entry(dialog, width=40)
        price_entry.insert(0, str(product.price))
        price_entry.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Quantity:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        quantity_entry = ttk.Entry(dialog, width=40)
        quantity_entry.insert(0, str(product.quantity))
        quantity_entry.grid(row=3, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Description:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        description_entry = ttk.Entry(dialog, width=40)
        description_entry.insert(0, product.description)
        description_entry.grid(row=4, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Reorder Level:").grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
        reorder_entry = ttk.Entry(dialog, width=40)
        reorder_entry.insert(0, str(product.reorder_level))
        reorder_entry.grid(row=5, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Supplier:").grid(row=6, column=0, sticky=tk.W, padx=10, pady=5)
        supplier_entry = ttk.Entry(dialog, width=40)
        supplier_entry.insert(0, product.supplier)
        supplier_entry.grid(row=6, column=1, padx=10, pady=5)
        
        def save_update():
            try:
                success, message = self.manager.update_product(
                    sku=sku,
                    name=name_entry.get().strip() or None,
                    category=category_entry.get().strip() or None,
                    price=float(price_entry.get().strip()) if price_entry.get().strip() else None,
                    quantity=int(quantity_entry.get().strip()) if quantity_entry.get().strip() else None,
                    description=description_entry.get().strip() or None,
                    reorder_level=int(reorder_entry.get().strip()) if reorder_entry.get().strip() else None,
                    supplier=supplier_entry.get().strip() or None
                )
                
                if success:
                    messagebox.showinfo("Success", message)
                    dialog.destroy()
                    self.refresh_products_list()
                else:
                    messagebox.showerror("Error", message)
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {str(e)}")
        
        ttk.Button(dialog, text="Save", command=save_update).grid(row=7, column=0, pady=20, padx=10)
        ttk.Button(dialog, text="Cancel", command=dialog.destroy).grid(row=7, column=1, pady=20, padx=10)
    
    def delete_product(self):
        """Delete the selected product."""
        selection = self.products_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a product first!")
            return
        
        item = self.products_tree.item(selection[0])
        sku = item['values'][0]
        product = self.manager.get_product(sku)
        
        if product:
            if messagebox.askyesno("Confirm Delete", 
                                   f"Are you sure you want to delete '{product.name}'?"):
                success, message = self.manager.delete_product(sku)
                if success:
                    messagebox.showinfo("Success", message)
                    self.refresh_products_list()
                else:
                    messagebox.showerror("Error", message)
    
    def add_stock(self):
        """Add stock to a product."""
        try:
            sku = self.add_stock_sku_entry.get().strip().upper()
            quantity = int(self.add_stock_qty_entry.get().strip())
            
            success, message = self.manager.add_stock(sku, quantity)
            
            if success:
                messagebox.showinfo("Success", message)
                self.add_stock_sku_entry.delete(0, tk.END)
                self.add_stock_qty_entry.delete(0, tk.END)
                self.refresh_products_list()
            else:
                messagebox.showerror("Error", message)
                
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity!")
    
    def remove_stock(self):
        """Remove stock from a product."""
        try:
            sku = self.remove_stock_sku_entry.get().strip().upper()
            quantity = int(self.remove_stock_qty_entry.get().strip())
            
            success, message = self.manager.remove_stock(sku, quantity)
            
            if success:
                messagebox.showinfo("Success", message)
                self.remove_stock_sku_entry.delete(0, tk.END)
                self.remove_stock_qty_entry.delete(0, tk.END)
                self.refresh_products_list()
            else:
                messagebox.showerror("Error", message)
                
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity!")
    
    def search_products(self):
        """Search for products."""
        # Clear existing results
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
        
        search_term = self.search_entry.get().strip()
        search_type = self.search_type.get()
        
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a search term!")
            return
        
        if search_type == "name":
            results = self.manager.search_by_name(search_term)
        elif search_type == "category":
            results = self.manager.search_by_category(search_term)
        elif search_type == "supplier":
            results = self.manager.search_by_supplier(search_term)
        else:
            results = []
        
        if results:
            for product in results:
                self.search_tree.insert("", tk.END, values=(
                    product.sku,
                    product.name,
                    product.category,
                    f"{product.price:.2f}",
                    product.quantity,
                    product.supplier or "N/A"
                ))
        else:
            messagebox.showinfo("Search Results", "No products found matching your search.")
    
    def generate_report(self):
        """Generate and display inventory report."""
        report = self.manager.generate_inventory_report()
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(1.0, report)
    
    def show_low_stock_in_report(self):
        """Show low stock items in the report tab."""
        low_stock = self.manager.get_low_stock_products()
        
        self.report_text.delete(1.0, tk.END)
        
        if not low_stock:
            self.report_text.insert(1.0, "No products are low on stock.")
        else:
            report_lines = [
                "=" * 60,
                "LOW STOCK REPORT",
                "=" * 60,
                "",
                f"Total Low Stock Items: {len(low_stock)}",
                "",
                "-" * 60
            ]
            
            for product in low_stock:
                report_lines.append(f"SKU:      {product.sku}")
                report_lines.append(f"Name:     {product.name}")
                report_lines.append(f"Quantity: {product.quantity} (Reorder at {product.reorder_level})")
                report_lines.append(f"Supplier: {product.supplier or 'N/A'}")
                report_lines.append("-" * 60)
            
            self.report_text.insert(1.0, "\n".join(report_lines))
    
    def show_low_stock(self):
        """Show low stock items in a popup."""
        low_stock = self.manager.get_low_stock_products()
        
        if not low_stock:
            messagebox.showinfo("Low Stock", "No products are low on stock.")
        else:
            message = f"Found {len(low_stock)} low stock item(s):\n\n"
            for product in low_stock[:10]:  # Show first 10
                message += f"• {product.name} (SKU: {product.sku}): {product.quantity} units\n"
            
            if len(low_stock) > 10:
                message += f"\n... and {len(low_stock) - 10} more"
            
            messagebox.showwarning("Low Stock Alert", message)
    
    def backup_data(self):
        """Create a backup of inventory data."""
        success, message = self.manager.backup()
        if success:
            messagebox.showinfo("Backup", message)
        else:
            messagebox.showerror("Backup Error", message)
    
    def refresh_all(self):
        """Refresh all views."""
        self.refresh_products_list()
        messagebox.showinfo("Refresh", "All views refreshed!")
    
    def show_about(self):
        """Show about dialog."""
        about_text = """
Inventory Management System
Version 1.0

A comprehensive inventory management application
with CLI and GUI interfaces.

Features:
• Product Management (CRUD operations)
• Stock Tracking
• Search & Filter
• Low Stock Alerts
• Inventory Reports
• Data Backup

© 2024 - Cost & Management Accounting Course
"""
        messagebox.showinfo("About", about_text)
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()


def main():
    """Entry point for the GUI application."""
    import sys
    storage_path = "inventory_data.json"
    
    # Check for custom storage path in command line args
    if len(sys.argv) > 1:
        storage_path = sys.argv[1]
    
    app = InventoryGUI(storage_path)
    app.run()


if __name__ == "__main__":
    main()
