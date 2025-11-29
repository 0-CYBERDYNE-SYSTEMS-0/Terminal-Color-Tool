#!/usr/bin/env python3
"""
Terminal Color Theme Creator - Demo Script

This script demonstrates the core functionality of the Terminal Color Theme Creator
without requiring a GUI. It shows how image color extraction and theme generation work.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.image_processor import ImageProcessor
import json

def demo_color_extraction():
    """Demonstrate color extraction from images."""
    print("=" * 60)
    print("Terminal Color Theme Creator - Demo")
    print("=" * 60)
    print()
    
    processor = ImageProcessor()
    
    print("1. COLOR EXTRACTION DEMO")
    print("-" * 30)
    
    # Check if we can use the image processor
    print("ImageProcessor initialized successfully!")
    print(f"Supported formats: {processor.supported_formats}")
    print()
    
    # Create some sample color data for demonstration
    sample_colors = [
        "#1a1b26",  # Dark blue (good for background)
        "#a9b1d6",  # Light blue (good for foreground)
        "#f7768e",  # Pink/red
        "#9ece6a",  # Green
        "#e0af68",  # Orange/yellow
        "#7aa2f7",  # Blue
        "#bb9af7",  # Purple/magenta
        "#7dcfff",  # Cyan
        "#414868",  # Dark gray (bright black)
        "#ff6b6b",  # Light red
        "#51cf66",  # Light green
        "#ffd43b",  # Light yellow
        "#74c0fc",  # Light blue
        "#da77f2",  # Light purple
        "#22b8cf",  # Light cyan
        "#e9ecef"   # Light gray (bright white)
    ]
    
    print("2. THEME GENERATION")
    print("-" * 30)
    
    # Simulate the theme data structure
    theme_data = {
        'name': 'Demo Theme',
        'description': 'A theme created from sample colors',
        'colors': {}
    }
    
    # Map sample colors to terminal color names
    terminal_colors = [
        'background', 'foreground', 'cursor',
        'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white',
        'bright_black', 'bright_red', 'bright_green', 'bright_yellow', 
        'bright_blue', 'bright_magenta', 'bright_cyan', 'bright_white'
    ]
    
    # Assign colors (first few for dark colors, rest for bright)
    theme_data['colors']['background'] = sample_colors[0]  # Darkest
    theme_data['colors']['foreground'] = sample_colors[1]  # Lightest
    theme_data['colors']['cursor'] = sample_colors[1]      # Same as foreground
    
    # Standard colors
    theme_data['colors']['black'] = sample_colors[2]
    theme_data['colors']['red'] = sample_colors[2]
    theme_data['colors']['green'] = sample_colors[3]
    theme_data['colors']['yellow'] = sample_colors[4]
    theme_data['colors']['blue'] = sample_colors[5]
    theme_data['colors']['magenta'] = sample_colors[6]
    theme_data['colors']['cyan'] = sample_colors[7]
    theme_data['colors']['white'] = sample_colors[8]
    
    # Bright colors
    theme_data['colors']['bright_black'] = sample_colors[9]
    theme_data['colors']['bright_red'] = sample_colors[10]
    theme_data['colors']['bright_green'] = sample_colors[11]
    theme_data['colors']['bright_yellow'] = sample_colors[12]
    theme_data['colors']['bright_blue'] = sample_colors[13]
    theme_data['colors']['bright_magenta'] = sample_colors[14]
    theme_data['colors']['bright_cyan'] = sample_colors[15]
    theme_data['colors']['bright_white'] = sample_colors[15]
    
    print(f"Generated theme: {theme_data['name']}")
    print(f"Description: {theme_data['description']}")
    print()
    
    print("3. COLOR MAPPING")
    print("-" * 30)
    
    for color_name, color_value in theme_data['colors'].items():
        print(f"{color_name:15}: {color_value}")
    
    print()
    
    print("4. EXPORT FORMATS")
    print("-" * 30)
    
    # Show different export formats (simplified version without Tkinter)
    print("\n4.1 ANSI Export Format:")
    print("-" * 25)
    # Simple ANSI export without importing Tkinter components
    ansi_lines = []
    ansi_lines.append(f"# Terminal Color Theme: {theme_data['name']}")
    ansi_lines.append("# ANSI escape codes for terminal colors")
    ansi_lines.append("# Copy these colors to your shell configuration (e.g., .bashrc, .zshrc)")
    ansi_lines.append("")
    
    # Export colors
    for color_name, color_value in theme_data['colors'].items():
        if color_name not in ['background', 'foreground', 'cursor']:
            ansi_lines.append(f"export COLOR_{color_name.upper()}='{color_value}'")
    
    ansi_lines.append("")
    ansi_lines.append("# Special colors")
    ansi_lines.append(f"# Background: {theme_data['colors']['background']}")
    ansi_lines.append(f"# Foreground: {theme_data['colors']['foreground']}")
    ansi_lines.append(f"# Cursor: {theme_data['colors']['cursor']}")
    
    ansi_content = "\n".join(ansi_lines)
    print(ansi_content)
    
    print("\n4.2 JSON Export Format:")
    print("-" * 25)
    json_content = json.dumps(theme_data, indent=2)
    print(json_content)
    
    print("\n4.3 Xresources Export Format:")
    print("-" * 30)
    xr_lines = []
    xr_lines.append(f"! Terminal Color Theme: {theme_data['name']}")
    xr_lines.append("! Xresources format for X11 terminals")
    xr_lines.append("! Add these to your ~/.Xresources file")
    xr_lines.append("! xrdb -merge ~/.Xresources")
    xr_lines.append("")
    
    xr_lines.append(f"*background: {theme_data['colors']['background']}")
    xr_lines.append(f"*foreground: {theme_data['colors']['foreground']}")
    xr_lines.append(f"*cursorColor: {theme_data['colors']['cursor']}")
    xr_lines.append("")
    
    # Standard ANSI colors
    xr_lines.append("!! Black")
    xr_lines.append(f"*color0: {theme_data['colors']['black']}")
    xr_lines.append(f"*color8: {theme_data['colors']['bright_black']}")
    xr_lines.append("")
    
    xr_lines.append("!! Red")
    xr_lines.append(f"*color1: {theme_data['colors']['red']}")
    xr_lines.append(f"*color9: {theme_data['colors']['bright_red']}")
    xr_lines.append("")
    
    xr_lines.append("!! Green")
    xr_lines.append(f"*color2: {theme_data['colors']['green']}")
    xr_lines.append(f"*color10: {theme_data['colors']['bright_green']}")
    xr_lines.append("")
    
    xr_lines.append("!! Yellow")
    xr_lines.append(f"*color3: {theme_data['colors']['yellow']}")
    xr_lines.append(f"*color11: {theme_data['colors']['bright_yellow']}")
    xr_lines.append("")
    
    xr_lines.append("!! Blue")
    xr_lines.append(f"*color4: {theme_data['colors']['blue']}")
    xr_lines.append(f"*color12: {theme_data['colors']['bright_blue']}")
    xr_lines.append("")
    
    xr_lines.append("!! Magenta")
    xr_lines.append(f"*color5: {theme_data['colors']['magenta']}")
    xr_lines.append(f"*color13: {theme_data['colors']['bright_magenta']}")
    xr_lines.append("")
    
    xr_lines.append("!! Cyan")
    xr_lines.append(f"*color6: {theme_data['colors']['cyan']}")
    xr_lines.append(f"*color14: {theme_data['colors']['bright_cyan']}")
    xr_lines.append("")
    
    xr_lines.append("!! White")
    xr_lines.append(f"*color7: {theme_data['colors']['white']}")
    xr_lines.append(f"*color15: {theme_data['colors']['bright_white']}")
    
    xr_content = "\n".join(xr_lines)
    print(xr_content)
    
    print()
    print("5. USAGE EXAMPLES")
    print("-" * 30)
    
    print("To use the full application with GUI:")
    print("1. Ensure Tkinter is installed: sudo apt-get install python3-tk (Ubuntu/Debian)")
    print("2. Install dependencies: pip install pillow scikit-learn numpy")
    print("3. Run: python main.py")
    print()
    
    print("For headless usage, you can:")
    print("1. Load an image and extract colors programmatically")
    print("2. Generate theme files in various formats")
    print("3. Integrate with shell scripts or CI/CD pipelines")
    print()
    
    print("6. PROJECT STRUCTURE")
    print("-" * 30)
    
    structure = """
theme-viz/
├── main.py              # Entry point (requires Tkinter)
├── app/
│   ├── __init__.py
│   ├── main_window.py   # Main GUI application
│   ├── color_picker.py # Interactive color controls
│   ├── image_processor.py # Image color extraction
│   ├── preview.py       # Terminal preview panel
│   └── export.py       # Export functionality
├── themes/
│   ├── presets.json     # Default themes
│   └── user_themes/     # User saved themes
├── demo.py              # This demo script
├── requirements.txt     # Python dependencies
└── README.md            # Documentation
"""
    
    print(structure)
    
    print()
    print("7. PRESET THEMES")
    print("-" * 30)
    
    presets = {
        "Tokyo Night": {
            'background': '#1a1b26',
            'foreground': '#a9b1d6',
            'cursor': '#ffffff',
            'black': '#1a1b26',
            'red': '#f7768e',
            'green': '#9ece6a',
            'yellow': '#e0af68',
            'blue': '#7aa2f7',
            'magenta': '#bb9af7',
            'cyan': '#7dcfff',
            'white': '#a9b1d6',
            'bright_black': '#414868',
            'bright_red': '#f7768e',
            'bright_green': '#9ece6a',
            'bright_yellow': '#e0af68',
            'bright_blue': '#7aa2f7',
            'bright_magenta': '#bb9af7',
            'bright_cyan': '#7dcfff',
            'bright_white': '#c0caf5'
        },
        "Solarized Dark": {
            'background': '#002b36',
            'foreground': '#839496',
            'cursor': '#ffffff',
            'black': '#073642',
            'red': '#dc322f',
            'green': '#586e75',
            'yellow': '#657b83',
            'blue': '#268bd2',
            'magenta': '#d33682',
            'cyan': '#2aa198',
            'white': '#839496',
            'bright_black': '#002b36',
            'bright_red': '#cb4b16',
            'bright_green': '#93a1a1',
            'bright_yellow': '#839496',
            'bright_blue': '#6c71c4',
            'bright_magenta': '#dc322f',
            'bright_cyan': '#2aa198',
            'bright_white': '#fdf6e3'
        }
    }
    
    for theme_name, colors in presets.items():
        print(f"\n{theme_name}:")
        for color_key, color_value in colors.items():
            print(f"  {color_key:15}: {color_value}")
    
    print()
    print("=" * 60)
    print("Demo completed successfully!")
    print("For the full GUI experience, ensure Tkinter is installed.")
    print("=" * 60)

if __name__ == "__main__":
    try:
        demo_color_extraction()
    except Exception as e:
        print(f"Error running demo: {e}")
        print("\nMake sure all dependencies are installed:")
        print("pip install pillow scikit-learn numpy")
