#!/usr/bin/env python3
"""
Main entry point for the Inventory Management System.

Run this file to start the interactive command-line interface.

Usage:
    python main.py [storage_file]
    
Arguments:
    storage_file: Optional path to the JSON file for data storage.
                  Defaults to 'inventory_data.json' in the current directory.
"""

from inventory_management.cli import main

if __name__ == "__main__":
    main()
