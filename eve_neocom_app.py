"""Main entry point for EVE Online Neocom 2.0 Mobile App."""

import sys
import os

# Add eve_app to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from eve_app.ui.main_app import main

if __name__ == "__main__":
    main()
