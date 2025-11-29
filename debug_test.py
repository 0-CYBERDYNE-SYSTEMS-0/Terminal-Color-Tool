#!/usr/bin/env python3
"""
Debug test for export formats
"""

import sys
import os
import json

# Test theme data
theme_data = {
    'name': 'Test Theme',
    'description': 'A test theme for verification',
    'colors': {
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
    }
}

print("Testing export formats...")

try:
    # Test JSON export
    json_output = json.dumps(theme_data, indent=2)
    json_test = 'name' in json_output and 'colors' in json_output
    print(f"JSON test: {'PASS' if json_test else 'FAIL'}")
    print(f"  JSON contains 'name': {'name' in json_output}")
    print(f"  JSON contains 'colors': {'colors' in json_output}")
    print(f"  Number of colors: {len(theme_data['colors'])}")
    
    # Test ANSI export
    ansi_lines = [
        f"# Terminal Color Theme: {theme_data['name']}",
        "# ANSI escape codes for terminal colors"
    ]
    for color_name, color_value in theme_data['colors'].items():
        if color_name not in ['background', 'foreground', 'cursor']:
            ansi_lines.append(f"export COLOR_{color_name.upper()}='{color_value}'")
    
    ansi_output = "\n".join(ansi_lines)
    ansi_test = 'export COLOR_BLACK' in ansi_output and 'export COLOR_RED' in ansi_output
    print(f"ANSI test: {'PASS' if ansi_test else 'FAIL'}")
    print(f"  ANSI contains COLOR_BLACK: {'export COLOR_BLACK' in ansi_output}")
    print(f"  ANSI contains COLOR_RED: {'export COLOR_RED' in ansi_output}")
    
    # Test Xresources export - full version
    xr_lines = [
        f"! Terminal Color Theme: {theme_data['name']}",
        f"*background: {theme_data['colors']['background']}",
        f"*foreground: {theme_data['colors']['foreground']}",
        f"*cursorColor: {theme_data['colors']['cursor']}",
        ""
    ]
    
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
    
    xr_output = "\n".join(xr_lines)
    xr_test = '*background' in xr_output and '*color0' in xr_output
    print(f"XR test: {'PASS' if xr_test else 'FAIL'}")
    print(f"  XR contains background: {'*background' in xr_output}")
    print(f"  XR contains color0: {'*color0' in xr_output}")
    
    print("\nAll tests passed!" if json_test and ansi_test and xr_test else "\nSome tests failed!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
