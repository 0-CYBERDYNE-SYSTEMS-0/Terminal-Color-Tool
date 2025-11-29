"""Export API endpoint."""

import json
from typing import Literal
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

router = APIRouter()


class ExportRequest(BaseModel):
    format: Literal["ansi", "json", "xresources", "shell", "registry", "iterm2", "winterm"]
    theme_data: dict


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
    }
    
    extensions = {
        "ansi": ".sh",
        "json": ".json",
        "xresources": ".Xresources",
        "shell": ".sh",
        "registry": ".reg",
        "iterm2": ".itermcolors",
        "winterm": ".json",
    }
    
    content_types = {
        "ansi": "text/x-shellscript",
        "json": "application/json",
        "xresources": "text/plain",
        "shell": "text/x-shellscript",
        "registry": "text/plain",
        "iterm2": "text/plain",
        "winterm": "application/json",
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


def _hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    
    try:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        return (0, 0, 0)  # Default to black if conversion fails
