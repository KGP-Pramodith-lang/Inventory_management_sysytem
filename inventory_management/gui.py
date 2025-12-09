"""
Graphical User Interface for the inventory management system using customtkinter.
"""

import customtkinter as ctk
from tkinter import messagebox
from typing import Optional
from .inventory import InventoryManager
from .models import Product

# Constants
MAX_LOW_STOCK_DISPLAY = 10  # Maximum number of low stock items to display in popup


class InventoryGUI:
    """CustomTkinter-based GUI for inventory management."""
    
    def __init__(self, storage_path: str = "inventory_data.json"):
        """Initialize the GUI with an inventory manager."""
        self.manager = InventoryManager(storage_path)
        
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")  # Dark mode
        ctk.set_default_color_theme("dark-blue")  # Base theme, customized with purple below
        
        self.root = ctk.CTk()
        self.root.title("Inventory Management System")
        self.root.geometry("1200x700")
        
        # Set purple theme colors
        self.purple_primary = "#9370DB"  # Medium purple
        self.purple_dark = "#6A4C93"  # Dark purple
        self.purple_light = "#B19CD9"  # Light purple
        self.bg_dark = "#1a1a1a"  # Dark background
        self.bg_medium = "#2b2b2b"  # Medium background
        
        # Create main container
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface."""
        # Create menu bar frame (since customtkinter doesn't support Menu)
        self.create_menu_bar()
        
        # Create tabview (replaces notebook)
        self.tabview = ctk.CTkTabview(self.root, fg_color=self.bg_medium)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_products_tab()
        self.create_add_product_tab()
        self.create_stock_management_tab()
        self.create_search_tab()
        self.create_reports_tab()
        
    def create_menu_bar(self):
        """Create a menu bar using buttons in a frame."""
        menubar_frame = ctk.CTkFrame(self.root, fg_color=self.purple_dark, height=40)
        menubar_frame.pack(fill="x", padx=0, pady=0)
        
        # File menu buttons
        ctk.CTkButton(
            menubar_frame, text="Backup Data", 
            command=self.backup_data,
            fg_color=self.purple_primary,
            hover_color=self.purple_light,
            width=100
        ).pack(side="left", padx=5, pady=5)
        
        ctk.CTkButton(
            menubar_frame, text="Refresh All", 
            command=self.refresh_all,
            fg_color=self.purple_primary,
            hover_color=self.purple_light,
            width=100
        ).pack(side="left", padx=5, pady=5)
        
        ctk.CTkButton(
            menubar_frame, text="Low Stock", 
            command=self.show_low_stock,
            fg_color=self.purple_primary,
            hover_color=self.purple_light,
            width=100
        ).pack(side="left", padx=5, pady=5)
        
        ctk.CTkButton(
            menubar_frame, text="About", 
            command=self.show_about,
            fg_color=self.purple_primary,
            hover_color=self.purple_light,
            width=80
        ).pack(side="left", padx=5, pady=5)
        
        ctk.CTkButton(
            menubar_frame, text="Exit", 
            command=self.root.quit,
            fg_color="#8B0000",  # Dark red for exit
            hover_color="#A52A2A",
            width=80
        ).pack(side="right", padx=5, pady=5)
    
    def create_products_tab(self):
        """Create the products listing tab."""
        self.tabview.add("All Products")
        products_frame = self.tabview.tab("All Products")
        
        # Top frame with buttons
        top_frame = ctk.CTkFrame(products_frame, fg_color="transparent")
        top_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkButton(
            top_frame, text="Refresh", 
            command=self.refresh_products_list,
            fg_color=self.purple_primary,
            hover_color=self.purple_light
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            top_frame, text="View Details", 
            command=self.view_product_details,
            fg_color=self.purple_primary,
            hover_color=self.purple_light
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            top_frame, text="Update Product", 
            command=self.update_product_dialog,
            fg_color=self.purple_primary,
            hover_color=self.purple_light
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            top_frame, text="Delete Product", 
            command=self.delete_product,
            fg_color="#8B0000",
            hover_color="#A52A2A"
        ).pack(side="left", padx=5)
        
        # Create scrollable frame for products table
        self.products_scroll = ctk.CTkScrollableFrame(
            products_frame, 
            fg_color=self.bg_medium,
            height=500
        )
        self.products_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create table header
        headers = ["", "SKU", "Name", "Category", "Price", "Quantity", "Value", "Status"]
        header_widths = [30, 100, 200, 120, 100, 100, 120, 80]
        
        for col, (header, width) in enumerate(zip(headers, header_widths)):
            label = ctk.CTkLabel(
                self.products_scroll, 
                text=header, 
                font=ctk.CTkFont(weight="bold", size=12),
                fg_color=self.purple_dark,
                width=width
            )
            label.grid(row=0, column=col, padx=2, pady=2, sticky="ew")
        
        # Store product row data
        self.product_rows = []
        
        # Populate the table
        self.refresh_products_list()
    
    def create_add_product_tab(self):
        """Create the add product tab."""
        self.tabview.add("Add Product")
        add_frame = self.tabview.tab("Add Product")
        
        # Create form in a scrollable frame
        form_scroll = ctk.CTkScrollableFrame(add_frame, fg_color="transparent")
        form_scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        form_frame = ctk.CTkFrame(form_scroll, fg_color=self.bg_medium)
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        title_label = ctk.CTkLabel(
            form_frame, 
            text="Product Information",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.purple_light
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))
        
        # Name
        ctk.CTkLabel(form_frame, text="Product Name:*").grid(row=1, column=0, sticky="w", pady=5, padx=10)
        self.add_name_entry = ctk.CTkEntry(form_frame, width=300)
        self.add_name_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Category
        ctk.CTkLabel(form_frame, text="Category:*").grid(row=2, column=0, sticky="w", pady=5, padx=10)
        self.add_category_entry = ctk.CTkEntry(form_frame, width=300)
        self.add_category_entry.grid(row=2, column=1, pady=5, padx=10)
        
        # Price
        ctk.CTkLabel(form_frame, text="Price ($):*").grid(row=3, column=0, sticky="w", pady=5, padx=10)
        self.add_price_entry = ctk.CTkEntry(form_frame, width=300)
        self.add_price_entry.grid(row=3, column=1, pady=5, padx=10)
        
        # Quantity
        ctk.CTkLabel(form_frame, text="Initial Quantity:*").grid(row=4, column=0, sticky="w", pady=5, padx=10)
        self.add_quantity_entry = ctk.CTkEntry(form_frame, width=300)
        self.add_quantity_entry.grid(row=4, column=1, pady=5, padx=10)
        
        # Description
        ctk.CTkLabel(form_frame, text="Description:").grid(row=5, column=0, sticky="w", pady=5, padx=10)
        self.add_description_entry = ctk.CTkEntry(form_frame, width=300)
        self.add_description_entry.grid(row=5, column=1, pady=5, padx=10)
        
        # Reorder Level
        ctk.CTkLabel(form_frame, text="Reorder Level:").grid(row=6, column=0, sticky="w", pady=5, padx=10)
        self.add_reorder_entry = ctk.CTkEntry(form_frame, width=300)
        self.add_reorder_entry.insert(0, "10")
        self.add_reorder_entry.grid(row=6, column=1, pady=5, padx=10)
        
        # Supplier
        ctk.CTkLabel(form_frame, text="Supplier:").grid(row=7, column=0, sticky="w", pady=5, padx=10)
        self.add_supplier_entry = ctk.CTkEntry(form_frame, width=300)
        self.add_supplier_entry.grid(row=7, column=1, pady=5, padx=10)
        
        # SKU (optional)
        ctk.CTkLabel(form_frame, text="Custom SKU:").grid(row=8, column=0, sticky="w", pady=5, padx=10)
        self.add_sku_entry = ctk.CTkEntry(form_frame, width=300)
        self.add_sku_entry.grid(row=8, column=1, pady=5, padx=10)
        
        ctk.CTkLabel(
            form_frame, 
            text="(Leave blank for auto-generated)",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        ).grid(row=9, column=1, sticky="w", padx=10)
        
        # Buttons
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=10, column=0, columnspan=2, pady=20)
        
        ctk.CTkButton(
            button_frame, text="Add Product", 
            command=self.add_product,
            fg_color=self.purple_primary,
            hover_color=self.purple_light,
            width=120
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame, text="Clear Form", 
            command=self.clear_add_form,
            fg_color=self.purple_dark,
            hover_color=self.purple_primary,
            width=120
        ).pack(side="left", padx=5)
    
    def create_stock_management_tab(self):
        """Create the stock management tab."""
        self.tabview.add("Stock Management")
        stock_frame = self.tabview.tab("Stock Management")
        
        # Create two sections: Add Stock and Remove Stock
        add_stock_frame = ctk.CTkFrame(stock_frame, fg_color=self.bg_medium)
        add_stock_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Add Stock section title
        ctk.CTkLabel(
            add_stock_frame, 
            text="Add Stock",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.purple_light
        ).grid(row=0, column=0, columnspan=2, pady=(10, 20))
        
        ctk.CTkLabel(add_stock_frame, text="Product SKU:").grid(row=1, column=0, sticky="w", pady=5, padx=10)
        self.add_stock_sku_entry = ctk.CTkEntry(add_stock_frame, width=250)
        self.add_stock_sku_entry.grid(row=1, column=1, pady=5, padx=10)
        
        ctk.CTkLabel(add_stock_frame, text="Quantity to Add:").grid(row=2, column=0, sticky="w", pady=5, padx=10)
        self.add_stock_qty_entry = ctk.CTkEntry(add_stock_frame, width=250)
        self.add_stock_qty_entry.grid(row=2, column=1, pady=5, padx=10)
        
        ctk.CTkButton(
            add_stock_frame, text="Add Stock", 
            command=self.add_stock,
            fg_color=self.purple_primary,
            hover_color=self.purple_light,
            width=200
        ).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Remove Stock section
        remove_stock_frame = ctk.CTkFrame(stock_frame, fg_color=self.bg_medium)
        remove_stock_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(
            remove_stock_frame, 
            text="Remove Stock (Sale)",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.purple_light
        ).grid(row=0, column=0, columnspan=2, pady=(10, 20))
        
        ctk.CTkLabel(remove_stock_frame, text="Product SKU:").grid(row=1, column=0, sticky="w", pady=5, padx=10)
        self.remove_stock_sku_entry = ctk.CTkEntry(remove_stock_frame, width=250)
        self.remove_stock_sku_entry.grid(row=1, column=1, pady=5, padx=10)
        
        ctk.CTkLabel(remove_stock_frame, text="Quantity to Remove:").grid(row=2, column=0, sticky="w", pady=5, padx=10)
        self.remove_stock_qty_entry = ctk.CTkEntry(remove_stock_frame, width=250)
        self.remove_stock_qty_entry.grid(row=2, column=1, pady=5, padx=10)
        
        ctk.CTkButton(
            remove_stock_frame, text="Remove Stock", 
            command=self.remove_stock,
            fg_color=self.purple_primary,
            hover_color=self.purple_light,
            width=200
        ).grid(row=3, column=0, columnspan=2, pady=10)
    
    def create_search_tab(self):
        """Create the search tab."""
        self.tabview.add("Search")
        search_frame = self.tabview.tab("Search")
        
        # Search controls
        control_frame = ctk.CTkFrame(search_frame, fg_color=self.bg_medium)
        control_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            control_frame, 
            text="Search Options",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.purple_light
        ).grid(row=0, column=0, columnspan=4, pady=(10, 15))
        
        ctk.CTkLabel(control_frame, text="Search By:").grid(row=1, column=0, sticky="w", pady=5, padx=10)
        
        self.search_type = ctk.StringVar(value="name")
        ctk.CTkRadioButton(
            control_frame, text="Name", 
            variable=self.search_type, value="name",
            fg_color=self.purple_primary,
            hover_color=self.purple_light
        ).grid(row=1, column=1, sticky="w", padx=5)
        
        ctk.CTkRadioButton(
            control_frame, text="Category", 
            variable=self.search_type, value="category",
            fg_color=self.purple_primary,
            hover_color=self.purple_light
        ).grid(row=1, column=2, sticky="w", padx=5)
        
        ctk.CTkRadioButton(
            control_frame, text="Supplier", 
            variable=self.search_type, value="supplier",
            fg_color=self.purple_primary,
            hover_color=self.purple_light
        ).grid(row=1, column=3, sticky="w", padx=5)
        
        ctk.CTkLabel(control_frame, text="Search Term:").grid(row=2, column=0, sticky="w", pady=5, padx=10)
        self.search_entry = ctk.CTkEntry(control_frame, width=400)
        self.search_entry.grid(row=2, column=1, columnspan=2, pady=5, padx=5, sticky="ew")
        
        ctk.CTkButton(
            control_frame, text="Search", 
            command=self.search_products,
            fg_color=self.purple_primary,
            hover_color=self.purple_light,
            width=100
        ).grid(row=2, column=3, padx=5)
        
        # Results frame with scrollable content
        results_frame = ctk.CTkFrame(search_frame, fg_color=self.bg_medium)
        results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(
            results_frame, 
            text="Search Results",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.purple_light
        ).pack(pady=(10, 5))
        
        self.search_scroll = ctk.CTkScrollableFrame(
            results_frame, 
            fg_color=self.bg_dark,
            height=350
        )
        self.search_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create table header for search results
        headers = ["SKU", "Name", "Category", "Price", "Quantity", "Supplier"]
        header_widths = [100, 200, 120, 100, 100, 150]
        
        for col, (header, width) in enumerate(zip(headers, header_widths)):
            label = ctk.CTkLabel(
                self.search_scroll, 
                text=header, 
                font=ctk.CTkFont(weight="bold", size=12),
                fg_color=self.purple_dark,
                width=width
            )
            label.grid(row=0, column=col, padx=2, pady=2, sticky="ew")
        
        # Store search result rows
        self.search_rows = []
    
    def create_reports_tab(self):
        """Create the reports tab."""
        self.tabview.add("Reports")
        reports_frame = self.tabview.tab("Reports")
        
        # Buttons frame
        button_frame = ctk.CTkFrame(reports_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(
            button_frame, text="Generate Full Report", 
            command=self.generate_report,
            fg_color=self.purple_primary,
            hover_color=self.purple_light,
            width=150
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame, text="View Low Stock", 
            command=self.show_low_stock_in_report,
            fg_color=self.purple_primary,
            hover_color=self.purple_light,
            width=150
        ).pack(side="left", padx=5)
        
        # Text area for report
        self.report_text = ctk.CTkTextbox(
            reports_frame, 
            wrap="word", 
            width=1000, 
            height=500,
            fg_color=self.bg_dark,
            font=ctk.CTkFont(family="Courier", size=11)
        )
        self.report_text.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Action methods
    
    def refresh_products_list(self):
        """Refresh the products list in the table."""
        # Clear existing items
        for row_widgets in self.product_rows:
            for widget in row_widgets:
                widget.destroy()
        self.product_rows = []
        
        # Get all products and populate
        products = self.manager.get_all_products()
        for idx, product in enumerate(products):
            row = idx + 1  # +1 for header row
            status = "LOW" if product.is_low_stock() else "OK"
            status_color = "#FF6B6B" if status == "LOW" else "#51CF66"
            
            # Create checkbox for selection
            var = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(
                self.products_scroll, text="", variable=var, width=30,
                fg_color=self.purple_primary,
                hover_color=self.purple_light
            )
            checkbox.grid(row=row, column=0, padx=2, pady=2)
            
            # Create labels for each column
            values = [
                product.sku,
                product.name,
                product.category,
                f"${product.price:.2f}",
                str(product.quantity),
                f"${product.total_value():.2f}",
                status
            ]
            
            widths = [100, 200, 120, 100, 100, 120, 80]
            row_widgets = [checkbox]
            
            for col, (value, width) in enumerate(zip(values, widths), start=1):
                fg_color = status_color if col == 7 else "transparent"
                label = ctk.CTkLabel(
                    self.products_scroll, 
                    text=value,
                    width=width,
                    fg_color=fg_color,
                    corner_radius=5
                )
                label.grid(row=row, column=col, padx=2, pady=2, sticky="ew")
                row_widgets.append(label)
            
            # Store the row with its data
            self.product_rows.append(row_widgets)
            # Store the SKU with the checkbox variable for later reference
            checkbox.sku = product.sku
            checkbox.var = var
    
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
        self.add_name_entry.delete(0, "end")
        self.add_category_entry.delete(0, "end")
        self.add_price_entry.delete(0, "end")
        self.add_quantity_entry.delete(0, "end")
        self.add_description_entry.delete(0, "end")
        self.add_reorder_entry.delete(0, "end")
        self.add_reorder_entry.insert(0, "10")
        self.add_supplier_entry.delete(0, "end")
        self.add_sku_entry.delete(0, "end")
    
    def get_selected_product_sku(self):
        """Get the SKU of the selected product from checkboxes."""
        for row_widgets in self.product_rows:
            checkbox = row_widgets[0]
            if hasattr(checkbox, 'var') and checkbox.var.get():
                return checkbox.sku
        return None
    
    def view_product_details(self):
        """View detailed information about selected product."""
        sku = self.get_selected_product_sku()
        if not sku:
            messagebox.showwarning("Warning", "Please select a product first!")
            return
        
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
        sku = self.get_selected_product_sku()
        if not sku:
            messagebox.showwarning("Warning", "Please select a product first!")
            return
        
        product = self.manager.get_product(sku)
        
        if not product:
            messagebox.showerror("Error", "Product not found!")
            return
        
        # Create update dialog
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(f"Update Product - {product.name}")
        dialog.geometry("500x500")
        dialog.configure(fg_color=self.bg_dark)
        
        # Create scrollable form
        scroll = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create form
        ctk.CTkLabel(scroll, text="Name:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        name_entry = ctk.CTkEntry(scroll, width=300)
        name_entry.insert(0, product.name)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(scroll, text="Category:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        category_entry = ctk.CTkEntry(scroll, width=300)
        category_entry.insert(0, product.category)
        category_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(scroll, text="Price ($):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        price_entry = ctk.CTkEntry(scroll, width=300)
        price_entry.insert(0, str(product.price))
        price_entry.grid(row=2, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(scroll, text="Quantity:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        quantity_entry = ctk.CTkEntry(scroll, width=300)
        quantity_entry.insert(0, str(product.quantity))
        quantity_entry.grid(row=3, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(scroll, text="Description:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        description_entry = ctk.CTkEntry(scroll, width=300)
        description_entry.insert(0, product.description or "")
        description_entry.grid(row=4, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(scroll, text="Reorder Level:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        reorder_entry = ctk.CTkEntry(scroll, width=300)
        reorder_entry.insert(0, str(product.reorder_level))
        reorder_entry.grid(row=5, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(scroll, text="Supplier:").grid(row=6, column=0, sticky="w", padx=10, pady=5)
        supplier_entry = ctk.CTkEntry(scroll, width=300)
        supplier_entry.insert(0, product.supplier or "")
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
        
        button_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        ctk.CTkButton(
            button_frame, text="Save", 
            command=save_update,
            fg_color=self.purple_primary,
            hover_color=self.purple_light,
            width=100
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame, text="Cancel", 
            command=dialog.destroy,
            fg_color=self.purple_dark,
            hover_color=self.purple_primary,
            width=100
        ).pack(side="left", padx=10)
    
    def delete_product(self):
        """Delete the selected product."""
        sku = self.get_selected_product_sku()
        if not sku:
            messagebox.showwarning("Warning", "Please select a product first!")
            return
        
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
                self.add_stock_sku_entry.delete(0, "end")
                self.add_stock_qty_entry.delete(0, "end")
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
                self.remove_stock_sku_entry.delete(0, "end")
                self.remove_stock_qty_entry.delete(0, "end")
                self.refresh_products_list()
            else:
                messagebox.showerror("Error", message)
                
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity!")
    
    def search_products(self):
        """Search for products."""
        # Clear existing results
        for row_widgets in self.search_rows:
            for widget in row_widgets:
                widget.destroy()
        self.search_rows = []
        
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
            for idx, product in enumerate(results):
                row = idx + 1  # +1 for header row
                values = [
                    product.sku,
                    product.name,
                    product.category,
                    f"${product.price:.2f}",
                    str(product.quantity),
                    product.supplier or "N/A"
                ]
                
                widths = [100, 200, 120, 100, 100, 150]
                row_widgets = []
                
                for col, (value, width) in enumerate(zip(values, widths)):
                    label = ctk.CTkLabel(
                        self.search_scroll, 
                        text=value,
                        width=width,
                        fg_color=self.bg_medium
                    )
                    label.grid(row=row, column=col, padx=2, pady=2, sticky="ew")
                    row_widgets.append(label)
                
                self.search_rows.append(row_widgets)
        else:
            messagebox.showinfo("Search Results", "No products found matching your search.")
    
    def generate_report(self):
        """Generate and display inventory report."""
        report = self.manager.generate_inventory_report()
        self.report_text.delete("0.0", "end")
        self.report_text.insert("0.0", report)
    
    def show_low_stock_in_report(self):
        """Show low stock items in the report tab."""
        low_stock = self.manager.get_low_stock_products()
        
        self.report_text.delete("0.0", "end")
        
        if not low_stock:
            self.report_text.insert("0.0", "No products are low on stock.")
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
            
            self.report_text.insert("0.0", "\n".join(report_lines))
    
    def show_low_stock(self):
        """Show low stock items in a popup."""
        low_stock = self.manager.get_low_stock_products()
        
        if not low_stock:
            messagebox.showinfo("Low Stock", "No products are low on stock.")
        else:
            message = f"Found {len(low_stock)} low stock item(s):\n\n"
            for product in low_stock[:MAX_LOW_STOCK_DISPLAY]:
                message += f"• {product.name} (SKU: {product.sku}): {product.quantity} units\n"
            
            if len(low_stock) > MAX_LOW_STOCK_DISPLAY:
                message += f"\n... and {len(low_stock) - MAX_LOW_STOCK_DISPLAY} more"
            
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
        from datetime import datetime
        current_year = datetime.now().year
        
        about_text = f"""
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

© {current_year} - Cost & Management Accounting Course
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
