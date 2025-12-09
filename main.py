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
    # Check if CLI mode is requested
    use_cli = '--cli' in sys.argv
    use_gui = '--gui' in sys.argv
    
    # Remove mode flags from argv
    sys.argv = [arg for arg in sys.argv if arg not in ('--cli', '--gui')]
    
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
