#!/usr/bin/env python3
"""
Main entry point for the Inventory Management System.

Run this file to start the inventory management system.
By default, it launches the GUI. Use --cli flag to use the command-line interface.

Usage:
    python main.py              # Launch GUI
    python main.py --cli        # Launch CLI
    python main.py --gui        # Launch GUI (explicit)
    python main.py [--cli|--gui] [storage_file]
    
Arguments:
    --cli:        Use command-line interface
    --gui:        Use graphical interface (default)
    storage_file: Optional path to the JSON file for data storage.
                  Defaults to 'inventory_data.json' in the current directory.
"""

import sys


def main():
    """Main entry point - choose between CLI and GUI."""
    # Parse command-line arguments
    args = sys.argv[1:]  # Don't modify sys.argv directly
    
    # Check if CLI mode is requested
    use_cli = '--cli' in args
    use_gui = '--gui' in args
    
    # Remove mode flags from arguments
    filtered_args = [arg for arg in args if arg not in ('--cli', '--gui')]
    
    # Reconstruct sys.argv with filtered arguments
    sys.argv = [sys.argv[0]] + filtered_args
    
    # Default to GUI if not specified
    if not use_cli and not use_gui:
        use_gui = True
    
    if use_cli:
        from inventory_management.cli import main as cli_main
        cli_main()
    else:
        from inventory_management.gui import main as gui_main
        gui_main()


if __name__ == "__main__":
    main()
