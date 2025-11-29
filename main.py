#!/usr/bin/env python3
"""
Terminal Color Theme Creator

A simple, intuitive application for creating and exporting terminal color themes.
"""

import tkinter as tk
from app.main_window import ThemeCreatorApp

def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = ThemeCreatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
