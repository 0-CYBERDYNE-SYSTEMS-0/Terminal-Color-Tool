"""Export API endpoint."""

import json
import os
from pathlib import Path
from typing import Literal
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

router = APIRouter()


class ExportRequest(BaseModel):
    format: Literal["ansi", "json", "xresources", "shell", "registry", "iterm2", "winterm", "wezterm"]
    theme_data: dict


class InstallWeztermRequest(BaseModel):
    theme_name: str
    colors: dict


@router.post("/export")
async def export_theme(req: ExportRequest):
    """Export theme in the specified format."""
    colors = req.theme_data.get("colors", {})
    theme_name = req.theme_data.get("name", "My Theme")
    
    generators = {
        "ansi": _generate_ansi,
        "json": _generate_json,
        "xresources": _generate_xresources,
        "shell": _generate_shell,
        "registry": _generate_registry,
        "iterm2": _generate_iterm2,
        "winterm": _generate_winterm,
        "wezterm": _generate_wezterm,
    }
    
    extensions = {
        "ansi": ".sh",
        "json": ".json",
        "xresources": ".Xresources",
        "shell": ".sh",
        "registry": ".reg",
        "iterm2": ".itermcolors",
        "winterm": ".json",
        "wezterm": ".lua",
    }
    
    content_types = {
        "ansi": "text/x-shellscript",
        "json": "application/json",
        "xresources": "text/plain",
        "shell": "text/x-shellscript",
        "registry": "text/plain",
        "iterm2": "text/plain",
        "winterm": "application/json",
        "wezterm": "text/plain",
    }
    
    if req.format not in generators:
        raise HTTPException(status_code=400, detail=f"Unsupported format: {req.format}")
    
    content = generators[req.format](colors, theme_name)
    filename = f"{theme_name.replace(' ', '_')}{extensions[req.format]}"
    
    return Response(
        content=content,
        media_type=content_types[req.format],
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.post("/install-wezterm")
async def install_wezterm_theme(req: InstallWeztermRequest):
    """Install WezTerm theme directly to user's .wezterm.lua file."""
    # Find WezTerm config location
    home_dir = Path.home()
    possible_locations = [
        home_dir / ".wezterm.lua",
        home_dir / ".config" / "wezterm" / "wezterm.lua"
    ]
    
    config_path = None
    for location in possible_locations:
        if location.exists() or location.parent.exists():
            config_path = location
            break
    
    if not config_path:
        # Create default location if none exists
        config_path = home_dir / ".wezterm.lua"
        config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Generate the theme content
    theme_content = _generate_wezterm(req.colors, req.theme_name)
    
    try:
        # Read existing config if it exists
        existing_config = ""
        if config_path.exists():
            existing_config = config_path.read_text()
        
        # Check if the theme already exists
        sanitized_name = req.theme_name.replace('-', '_').replace(' ', '_').lower()
        theme_pattern = f"config.color_schemes['{sanitized_name}']"
        
        if theme_pattern in existing_config:
            raise HTTPException(
                status_code=400, 
                detail=f"Theme '{req.theme_name}' already exists in {config_path}"
            )
        
        # Ensure the file has the basic structure
        if not existing_config.strip():
            # Create new config file
            new_config = f"""local wezterm = require 'wezterm'
local config = wezterm.config_builder()

{theme_content}

return config
"""
        else:
            # Add to existing config
            if "config.color_schemes = config.color_schemes or {{}}" not in existing_config:
                # Insert before 'return config' or at end
                if "return config" in existing_config:
                    insertion_point = existing_config.find("return config")
                    new_config = (
                        existing_config[:insertion_point] + 
                        "\n" + theme_content.strip() + "\n\n" + 
                        existing_config[insertion_point:]
                    )
                else:
                    new_config = existing_config.rstrip() + "\n\n" + theme_content.strip() + "\n"
            else:
                # Just add the theme
                new_config = existing_config.rstrip() + "\n" + theme_content.strip() + "\n"
        
        # Write the updated config
        config_path.write_text(new_config)
        
        return {
            "success": True,
            "message": f"Theme '{req.theme_name}' installed successfully",
            "config_path": str(config_path),
            "theme_name": sanitized_name,
            "instructions": f"Theme installed! Reload WezTerm with Ctrl+Shift+R and then use the theme picker with Ctrl+Shift+P to select '{sanitized_name}'."
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to install theme: {str(e)}"
        )


def _generate_ansi(colors: dict, theme_name: str) -> str:
    """Generate ANSI escape sequence script."""
    script = f"""#!/bin/bash
# {theme_name} - ANSI Color Theme

"""
    for color_name, hex_color in colors.items():
        rgb = _hex_to_rgb(hex_color)
        script += f"echo -e '\\033]4;{color_name};rgb:{rgb[0]}/{rgb[1]}/{rgb[2]}\\007'\n"
    
    script += """
# Background and foreground
"""
    bg_rgb = _hex_to_rgb(colors.get('background', '#000000'))
    fg_rgb = _hex_to_rgb(colors.get('foreground', '#ffffff'))
    
    script += f"echo -e '\\033]10;rgb:{fg_rgb[0]}/{fg_rgb[1]}/{fg_rgb[2]}\\007'\n"
    script += f"echo -e '\\033]11;rgb:{bg_rgb[0]}/{bg_rgb[1]}/{bg_rgb[2]}\\007'\n"
    
    return script


def _generate_json(colors: dict, theme_name: str) -> str:
    """Generate JSON theme configuration."""
    return json.dumps({
        "name": theme_name,
        "colors": colors
    }, indent=2)


def _generate_xresources(colors: dict, theme_name: str) -> str:
    """Generate Xresources theme."""
    content = f"""! {theme_name} - Xresources Theme

! Terminal colors
"""
    # Map color names to Xresources names
    color_map = {
        'background': '*.background',
        'foreground': '*.foreground',
        'cursor': '*.cursorColor',
        'black': '*.color0',
        'red': '*.color1',
        'green': '*.color2',
        'yellow': '*.color3',
        'blue': '*.color4',
        'magenta': '*.color5',
        'cyan': '*.color6',
        'white': '*.color7',
        'bright_black': '*.color8',
        'bright_red': '*.color9',
        'bright_green': '*.color10',
        'bright_yellow': '*.color11',
        'bright_blue': '*.color12',
        'bright_magenta': '*.color13',
        'bright_cyan': '*.color14',
        'bright_white': '*.color15',
    }
    
    for color_name, hex_color in colors.items():
        xresources_name = color_map.get(color_name, f'*.{color_name}')
        content += f"{xresources_name}: {hex_color}\n"
    
    return content


def _generate_shell(colors: dict, theme_name: str) -> str:
    """Generate shell script to set terminal colors."""
    script = f"""#!/bin/bash
# {theme_name} - Shell Color Theme

export TERM_COLOR_BACKGROUND="{colors.get('background', '#000000')}"
export TERM_COLOR_FOREGROUND="{colors.get('foreground', '#ffffff')}"
"""
    for color_name, hex_color in colors.items():
        var_name = f"TERM_COLOR_{color_name.upper()}"
        script += f'export {var_name}="{hex_color}"\n'
    
    return script


def _generate_registry(colors: dict, theme_name: str) -> str:
    """Generate Windows Registry (.reg) theme."""
    content = f"""Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\\Console\\{theme_name}]
"""
    for color_name, hex_color in colors.items():
        reg_color = hex_color.lstrip('#')
        content += f'"{color_name}"="{reg_color}"\n'
    
    return content


def _generate_iterm2(colors: dict, theme_name: str) -> str:
    """Generate iTerm2 colors."""
    import plistlib
    from io import BytesIO
    
    # Convert colors to iTerm2 format
    iterm_colors = {}
    for color_name, hex_color in colors.items():
        rgb = _hex_to_rgb(hex_color)
        # Normalize RGB values to 0-1 range
        iterm_colors[color_name] = {
            'Red Component': rgb[0] / 255,
            'Green Component': rgb[1] / 255,
            'Blue Component': rgb[2] / 255,
            'Alpha Component': 1.0
        }
    
    # Create plist structure
    theme_dict = {
        'Ansi 0 Color': iterm_colors.get('black', {}),
        'Ansi 1 Color': iterm_colors.get('red', {}),
        'Ansi 2 Color': iterm_colors.get('green', {}),
        'Ansi 3 Color': iterm_colors.get('yellow', {}),
        'Ansi 4 Color': iterm_colors.get('blue', {}),
        'Ansi 5 Color': iterm_colors.get('magenta', {}),
        'Ansi 6 Color': iterm_colors.get('cyan', {}),
        'Ansi 7 Color': iterm_colors.get('white', {}),
        'Ansi 8 Color': iterm_colors.get('bright_black', {}),
        'Ansi 9 Color': iterm_colors.get('bright_red', {}),
        'Ansi 10 Color': iterm_colors.get('bright_green', {}),
        'Ansi 11 Color': iterm_colors.get('bright_yellow', {}),
        'Ansi 12 Color': iterm_colors.get('bright_blue', {}),
        'Ansi 13 Color': iterm_colors.get('bright_magenta', {}),
        'Ansi 14 Color': iterm_colors.get('bright_cyan', {}),
        'Ansi 15 Color': iterm_colors.get('bright_white', {}),
        'Background Color': iterm_colors.get('background', {}),
        'Foreground Color': iterm_colors.get('foreground', {}),
        'Cursor Color': iterm_colors.get('cursor', {}),
    }
    
    # Convert to plist XML
    buffer = BytesIO()
    plistlib.dump(theme_dict, buffer)
    return buffer.getvalue().decode('utf-8')


def _generate_winterm(colors: dict, theme_name: str) -> str:
    """Generate Windows Terminal theme."""
    theme = {
        "name": theme_name,
        "background": colors.get('background', '#000000'),
        "foreground": colors.get('foreground', '#ffffff'),
        "cursor": colors.get('cursor', '#ffffff'),
        "black": colors.get('black', '#000000'),
        "red": colors.get('red', '#ff0000'),
        "green": colors.get('green', '#00ff00'),
        "yellow": colors.get('yellow', '#ffff00'),
        "blue": colors.get('blue', '#0000ff'),
        "purple": colors.get('magenta', '#ff00ff'),
        "cyan": colors.get('cyan', '#00ffff'),
        "white": colors.get('white', '#ffffff'),
        "brightBlack": colors.get('bright_black', '#808080'),
        "brightRed": colors.get('bright_red', '#ff8080'),
        "brightGreen": colors.get('bright_green', '#80ff80'),
        "brightYellow": colors.get('bright_yellow', '#ffff80'),
        "brightBlue": colors.get('bright_blue', '#8080ff'),
        "brightPurple": colors.get('bright_magenta', '#ff80ff'),
        "brightCyan": colors.get('bright_cyan', '#80ffff'),
        "brightWhite": colors.get('bright_white', '#ffffff'),
    }
    
    return json.dumps(theme, indent=2)


def _generate_wezterm(colors: dict, theme_name: str) -> str:
    """Generate WezTerm color scheme."""
    # Sanitize theme name for use in Lua
    sanitized_name = theme_name.replace('-', '_').replace(' ', '_').lower()
    
    content = f"""-- Add {theme_name} color scheme
config.color_schemes = config.color_schemes or {{}}
config.color_schemes['{sanitized_name}'] = {{
  foreground = '{colors.get('foreground', '#ffffff')}',
  background = '{colors.get('background', '#000000')}',
  cursor_bg = '{colors.get('cursor', colors.get('foreground', '#ffffff'))}',
  cursor_fg = '{colors.get('background', '#000000')}',
  cursor_border = '{colors.get('cursor', colors.get('foreground', '#ffffff'))}',
  selection_fg = '{colors.get('foreground', '#ffffff')}',
  selection_bg = '{colors.get('selection_bg', colors.get('blue', '#0000ff'))}',
  split = '{colors.get('split', colors.get('bright_yellow', '#ffff00'))}',
  ansi = {{
    '{colors.get('black', '#000000')}',
    '{colors.get('red', '#ff0000')}',
    '{colors.get('green', '#00ff00')}',
    '{colors.get('yellow', '#ffff00')}',
    '{colors.get('blue', '#0000ff')}',
    '{colors.get('magenta', '#ff00ff')}',
    '{colors.get('cyan', '#00ffff')}',
    '{colors.get('white', '#ffffff')}'
  }},
  brights = {{
    '{colors.get('bright_black', '#808080')}',
    '{colors.get('bright_red', '#ff8080')}',
    '{colors.get('bright_green', '#80ff80')}',
    '{colors.get('bright_yellow', '#ffff80')}',
    '{colors.get('bright_blue', '#8080ff')}',
    '{colors.get('bright_magenta', '#ff80ff')}',
    '{colors.get('bright_cyan', '#80ffff')}',
    '{colors.get('bright_white', '#ffffff')}'
  }}
}}
"""

    return content


def _hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    
    try:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        return (0, 0, 0)  # Default to black if conversion fails
