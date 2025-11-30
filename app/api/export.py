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
    format: Literal["ansi", "json", "xresources", "shell", "registry", "iterm2", "winterm", "wezterm", "alacritty", "kitty", "hyper", "ghostty", "terminal"]
    theme_data: dict
    wezterm_mode: Literal["complete", "theme-only"] | None = None


class InstallWeztermRequest(BaseModel):
    theme_name: str
    colors: dict


def _validate_colors(colors: dict) -> dict:
    """Validate and add missing required color fields with fallbacks."""
    # Required colors with their fallbacks
    required_colors = {
        'foreground': {'default': '#ffffff', 'fallback': None},
        'background': {'default': '#000000', 'fallback': None},
        'cursor': {'default': None, 'fallback': 'foreground'},
        'black': {'default': '#000000', 'fallback': 'background'},
        'red': {'default': '#ff0000', 'fallback': None},
        'green': {'default': '#00ff00', 'fallback': None},
        'yellow': {'default': '#ffff00', 'fallback': None},
        'blue': {'default': '#0000ff', 'fallback': None},
        'magenta': {'default': '#ff00ff', 'fallback': None},
        'cyan': {'default': '#00ffff', 'fallback': None},
        'white': {'default': '#ffffff', 'fallback': 'foreground'},
        'bright_black': {'default': '#808080', 'fallback': 'black'},
        'bright_red': {'default': '#ff8080', 'fallback': 'red'},
        'bright_green': {'default': '#80ff80', 'fallback': 'green'},
        'bright_yellow': {'default': '#ffff80', 'fallback': 'yellow'},
        'bright_blue': {'default': '#8080ff', 'fallback': 'blue'},
        'bright_magenta': {'default': '#ff80ff', 'fallback': 'magenta'},
        'bright_cyan': {'default': '#80ffff', 'fallback': 'cyan'},
        'bright_white': {'default': '#ffffff', 'fallback': 'white'},
    }
    
    # Create a copy to work with
    validated_colors = colors.copy()
    
    # Fill in missing colors
    for color_name, config in required_colors.items():
        if color_name not in validated_colors or not validated_colors[color_name]:
            if config['fallback'] and config['fallback'] in validated_colors:
                validated_colors[color_name] = validated_colors[config['fallback']]
            elif config['default']:
                validated_colors[color_name] = config['default']
    
    return validated_colors


@router.post("/export")
async def export_theme(req: ExportRequest):
    """Export theme in the specified format."""
    colors = _validate_colors(req.theme_data.get("colors", {}))
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
        "alacritty": _generate_alacritty,
        "kitty": _generate_kitty,
        "hyper": _generate_hyper,
        "ghostty": _generate_ghostty,
        "terminal": _generate_terminal,
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
        "alacritty": ".yml",
        "kitty": ".conf",
        "hyper": ".js",
        "ghostty": ".toml",
        "terminal": ".terminal",
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
        "alacritty": "text/yaml",
        "kitty": "text/plain",
        "hyper": "application/javascript",
        "ghostty": "text/plain",
        "terminal": "text/xml",
    }
    
    if req.format not in generators:
        raise HTTPException(status_code=400, detail=f"Unsupported format: {req.format}")
    
    if req.format == 'wezterm':
        theme_only = (req.wezterm_mode == 'theme-only')
        content = generators[req.format](colors, theme_name, theme_only)
    else:
        content = generators[req.format](colors, theme_name)
    filename = f"{theme_name.replace(' ', '_')}{extensions[req.format]}"
    
    return Response(
        content=content,
        media_type=content_types[req.format],
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.post("/install-wezterm")
async def install_wezterm_theme(req: InstallWeztermRequest):
    """Install WezTerm theme directly to user's .wezterm.lua file.
    
    This does TWO things (both required for themes to work):
    1. Adds theme definition to get_builtin_color_schemes() override
    2. Adds handler in color picker callback to apply the theme
    """
    colors = _validate_colors(req.colors)
    
    home_dir = Path.home()
    possible_locations = [
        home_dir / ".wezterm.lua",
        home_dir / ".config" / "wezterm" / "wezterm.lua"
    ]
    
    config_path = None
    for location in possible_locations:
        if location.exists():
            config_path = location
            break
    
    if not config_path:
        raise HTTPException(
            status_code=400,
            detail="No .wezterm.lua config found. Please create one first with the color picker pattern."
        )
    
    sanitized_name = req.theme_name.replace('-', '_').replace(' ', '_').lower()
    
    # Theme definition to add before "return schemes"
    theme_definition = f"""
  -- Theme: {req.theme_name}
  schemes['{sanitized_name}'] = {{
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
    
    # Handler to add in color picker callback (before the else clause)
    handler_code = f"elseif id == '{sanitized_name}' then\n                win:set_config_overrides {{ colors = wezterm.get_builtin_color_schemes().{sanitized_name} }}"
    
    try:
        existing_config = config_path.read_text()
        
        # Check if theme already exists
        if f"schemes['{sanitized_name}']" in existing_config:
            raise HTTPException(
                status_code=400, 
                detail=f"Theme '{req.theme_name}' already exists in {config_path}"
            )
        
        # Verify required patterns exist
        if "return schemes" not in existing_config:
            raise HTTPException(
                status_code=400,
                detail="Config missing 'return schemes' - needs get_builtin_color_schemes override pattern."
            )
        
        # STEP 1: Insert theme definition before "return schemes"
        lines = existing_config.split('\n')
        theme_inserted = False
        
        for i, line in enumerate(lines):
            if "return schemes" in line and not theme_inserted:
                theme_lines = theme_definition.strip().split('\n')
                for j, theme_line in enumerate(theme_lines):
                    lines.insert(i + j, theme_line)
                theme_inserted = True
                break
        
        if not theme_inserted:
            raise HTTPException(status_code=400, detail="Failed to insert theme definition.")
        
        new_config = '\n'.join(lines)
        
        # STEP 2: Insert handler in color picker callback
        # Find the "else" clause that handles built-in schemes and insert before it
        # Pattern: look for "else" after custom theme handlers like "if id == 'farm'"
        
        # Find the color picker callback section
        import re
        
        # Look for the pattern: existing elseif or if for custom themes, then else for built-in
        # We need to insert our elseif before the final "else" in the theme selection callback
        
        # Find "-- Built-in scheme" or the else that leads to color_scheme = id
        else_pattern = r"(\s+)(else\s*\n\s*-- Built-in)"
        match = re.search(else_pattern, new_config)
        
        if match:
            indent = match.group(1)
            # Insert our handler before the else
            insert_pos = match.start()
            new_config = (
                new_config[:insert_pos] + 
                f"{indent}{handler_code}\n" + 
                new_config[insert_pos:]
            )
        else:
            # Try alternate pattern: just "else" followed by color_scheme = id
            else_pattern2 = r"(\s+)(else\s*\n\s*.*color_scheme\s*=\s*id)"
            match2 = re.search(else_pattern2, new_config)
            
            if match2:
                indent = match2.group(1)
                insert_pos = match2.start()
                new_config = (
                    new_config[:insert_pos] + 
                    f"{indent}{handler_code}\n" + 
                    new_config[insert_pos:]
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Could not find color picker callback else clause. Config may need manual handler addition."
                )
        
        # Write the updated config
        config_path.write_text(new_config)
        
        return {
            "success": True,
            "message": f"Theme '{req.theme_name}' installed successfully",
            "config_path": str(config_path),
            "theme_name": sanitized_name,
            "instructions": f"Theme installed! Reload WezTerm (Ctrl+Shift+R) and use theme picker (Cmd+Shift+P) to select '{sanitized_name}'."
        }
        
    except HTTPException:
        raise
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


def _generate_wezterm(colors: dict, theme_name: str, theme_only: bool = False) -> str:
    """Generate WezTerm color scheme with complete template including color picker functionality."""
    # Sanitize theme name for use in Lua
    sanitized_name = theme_name.replace('-', '_').replace(' ', '_').lower()
    
    if theme_only:
        # Only generate the theme data, not the complete config
        return _generate_wezterm_theme_only(colors, theme_name, sanitized_name)
    else:
        # Generate complete config with color picker functionality
        return _generate_wezterm_complete_config(colors, theme_name, sanitized_name)


def _generate_wezterm_theme_only(colors: dict, theme_name: str, sanitized_name: str) -> str:
    """Generate WezTerm theme data only for manual integration."""
    # Extract colors with proper fallbacks
    foreground = colors.get('foreground', '#ffffff')
    background = colors.get('background', '#000000')
    cursor_bg = colors.get('cursor', foreground)
    cursor_fg = background
    cursor_border = colors.get('cursor', foreground)
    selection_fg = colors.get('foreground', foreground)
    selection_bg = colors.get('selection_bg', colors.get('blue', '#0000ff'))
    split_color = colors.get('split', colors.get('bright_yellow', '#ffff00'))
    
    # ANSI colors with fallbacks
    ansi_colors = [
        colors.get('black', '#000000'),      # black
        colors.get('red', '#ff0000'),        # red
        colors.get('green', '#00ff00'),      # green
        colors.get('yellow', '#ffff00'),     # yellow
        colors.get('blue', '#0000ff'),       # blue
        colors.get('magenta', '#ff00ff'),    # magenta
        colors.get('cyan', '#00ffff'),       # cyan
        colors.get('white', '#ffffff')       # white
    ]
    
    # Bright colors with fallbacks
    bright_colors = [
        colors.get('bright_black', '#808080'),    # bright black
        colors.get('bright_red', '#ff8080'),      # bright red
        colors.get('bright_green', '#80ff80'),    # bright green
        colors.get('bright_yellow', '#ffff80'),   # bright yellow
        colors.get('bright_blue', '#8080ff'),     # bright blue
        colors.get('bright_magenta', '#ff80ff'),  # bright magenta
        colors.get('bright_cyan', '#80ffff'),     # bright cyan
        colors.get('bright_white', '#ffffff')     # bright white
    ]
    
    content = f"""-- WezTerm Theme: {theme_name}
-- Add this to your wezterm.get_builtin_color_schemes() override function
-- and make sure to handle it in the color picker action callback

config.color_schemes = config.color_schemes or {{}}
config.color_schemes['{sanitized_name}'] = {{
  foreground = '{foreground}',
  background = '{background}',
  cursor_bg = '{cursor_bg}',
  cursor_fg = '{cursor_fg}',
  cursor_border = '{cursor_border}',
  selection_fg = '{selection_fg}',
  selection_bg = '{selection_bg}',
  split = '{split_color}',
  ansi = {{
    '{ansi_colors[0]}', -- black
    '{ansi_colors[1]}', -- red
    '{ansi_colors[2]}', -- green
    '{ansi_colors[3]}', -- yellow
    '{ansi_colors[4]}', -- blue
    '{ansi_colors[5]}', -- magenta
    '{ansi_colors[6]}', -- cyan
    '{ansi_colors[7]}', -- white
  }},
  brights = {{
    '{bright_colors[0]}', -- bright black
    '{bright_colors[1]}', -- bright red
    '{bright_colors[2]}', -- bright green
    '{bright_colors[3]}', -- bright yellow
    '{bright_colors[4]}', -- bright blue
    '{bright_colors[5]}', -- bright magenta
    '{bright_colors[6]}', -- bright cyan
    '{bright_colors[7]}', -- bright white
  }}
}}

-- IMPORTANT: Add this to your color picker action callback:
-- if id == '{sanitized_name}' then
--   win:set_config_overrides {{ colors = schemes['{sanitized_name}'] }}
-- end
"""

    return content


def _generate_wezterm_complete_config(colors: dict, theme_name: str, sanitized_name: str) -> str:
    """Generate complete WezTerm config with color picker functionality."""
    # Extract colors with proper fallbacks
    foreground = colors.get('foreground', '#ffffff')
    background = colors.get('background', '#000000')
    cursor_bg = colors.get('cursor', foreground)
    cursor_fg = background
    cursor_border = colors.get('cursor', foreground)
    selection_fg = colors.get('foreground', foreground)
    selection_bg = colors.get('selection_bg', colors.get('blue', '#0000ff'))
    split_color = colors.get('split', colors.get('bright_yellow', '#ffff00'))
    
    # ANSI colors with fallbacks
    ansi_colors = [
        colors.get('black', '#000000'),      # black
        colors.get('red', '#ff0000'),        # red
        colors.get('green', '#00ff00'),      # green
        colors.get('yellow', '#ffff00'),     # yellow
        colors.get('blue', '#0000ff'),       # blue
        colors.get('magenta', '#ff00ff'),    # magenta
        colors.get('cyan', '#00ffff'),       # cyan
        colors.get('white', '#ffffff')       # white
    ]
    
    # Bright colors with fallbacks
    bright_colors = [
        colors.get('bright_black', '#808080'),    # bright black
        colors.get('bright_red', '#ff8080'),      # bright red
        colors.get('bright_green', '#80ff80'),    # bright green
        colors.get('bright_yellow', '#ffff80'),   # bright yellow
        colors.get('bright_blue', '#8080ff'),     # bright blue
        colors.get('bright_magenta', '#ff80ff'),  # bright magenta
        colors.get('bright_cyan', '#80ffff'),     # bright cyan
        colors.get('bright_white', '#ffffff')     # bright white
    ]
    
    content = f"""-- Add {theme_name} color scheme with complete implementation
local wezterm = require 'wezterm'

-- Override get_builtin_color_schemes to add custom themes to picker
local original_get_builtin_color_schemes = wezterm.get_builtin_color_schemes
wezterm.get_builtin_color_schemes = function()
  local schemes = original_get_builtin_color_schemes()
  
  -- Add {theme_name} theme
  schemes['{sanitized_name}'] = {{
    foreground = '{foreground}',
    background = '{background}',
    cursor_bg = '{cursor_bg}',
    cursor_fg = '{cursor_fg}',
    cursor_border = '{cursor_border}',
    selection_fg = '{selection_fg}',
    selection_bg = '{selection_bg}',
    split = '{split_color}',
    ansi = {{
      '{ansi_colors[0]}', -- black
      '{ansi_colors[1]}', -- red
      '{ansi_colors[2]}', -- green
      '{ansi_colors[3]}', -- yellow
      '{ansi_colors[4]}', -- blue
      '{ansi_colors[5]}', -- magenta
      '{ansi_colors[6]}', -- cyan
      '{ansi_colors[7]}', -- white
    }},
    brights = {{
      '{bright_colors[0]}', -- bright black
      '{bright_colors[1]}', -- bright red
      '{bright_colors[2]}', -- bright green
      '{bright_colors[3]}', -- bright yellow
      '{bright_colors[4]}', -- bright blue
      '{bright_colors[5]}', -- bright magenta
      '{bright_colors[6]}', -- bright cyan
      '{bright_colors[7]}', -- bright white
    }}
  }}
  
  return schemes
end

-- Add color picker key binding and action
return {{
  -- Theme picker shortcut (Ctrl+Shift+P)
  keys = {{
    key = 'P',
    mods = 'CMD|SHIFT',
    action = wezterm.action_callback(function(window, pane)
      local schemes = wezterm.get_builtin_color_schemes()
      local choices = {{}}
      for name, scheme in pairs(schemes) do
        -- Generate color swatches for picker
        local label_parts = {{}}
        if scheme.ansi then
          for i = 1, #scheme.ansi do
            table.insert(label_parts, {{ Background = {{ Color = scheme.ansi[i] }} }})
            table.insert(label_parts, {{ Text = '  ' }})
            table.insert(label_parts, 'ResetAttributes')
            table.insert(label_parts, {{ Text = ' ' }})
          end
        end
        if scheme.brights then
          for i = 1, #scheme.brights do
            table.insert(label_parts, {{ Background = {{ Color = scheme.brights[i] }} }})
            table.insert(label_parts, {{ Text = '  ' }})
            table.insert(label_parts, 'ResetAttributes')
            table.insert(label_parts, {{ Text = ' ' }})
          end
        end
        table.insert(label_parts, {{ Text = '  ' .. name }})
        table.insert(choices, {{ label = wezterm.format(label_parts), id = name }})
      end
      table.sort(choices, function(a, b) return a.id < b.id end)
      
      window:perform_action(
        wezterm.action.InputSelector {{
          title = 'Choose Color Scheme',
          choices = choices,
          fuzzy = true,
          action = wezterm.action_callback(function(win, _, id, label)
            if id then
              if id == '{sanitized_name}' then
                -- Custom theme: use colors override for actual application
                win:set_config_overrides {{ colors = schemes['{sanitized_name}'] }}
              else
                -- Built-in themes: use normal color_scheme method
                win:set_config_overrides {{ color_scheme = id }}
              end
            end
          end),
        }},
        pane
      )
    end),
  }},
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


def _generate_alacritty(colors: dict, theme_name: str) -> str:
    """Generate Alacritty YAML configuration."""
    content = f"""# {theme_name} - Alacritty Color Scheme
colors:
  primary:
    background: '{colors.get('background', '#000000')}'
    foreground: '{colors.get('foreground', '#ffffff')}'
  cursor: '{colors.get('cursor', '#ffffff')}'
  normal:
    black: '{colors.get('black', '#000000')}'
    red: '{colors.get('red', '#ff0000')}'
    green: '{colors.get('green', '#00ff00')}'
    yellow: '{colors.get('yellow', '#ffff00')}'
    blue: '{colors.get('blue', '#0000ff')}'
    magenta: '{colors.get('magenta', '#ff00ff')}'
    cyan: '{colors.get('cyan', '#00ffff')}'
    white: '{colors.get('white', '#ffffff')}'
  bright:
    black: '{colors.get('bright_black', '#808080')}'
    red: '{colors.get('bright_red', '#ff8080')}'
    green: '{colors.get('bright_green', '#80ff80')}'
    yellow: '{colors.get('bright_yellow', '#ffff80')}'
    blue: '{colors.get('bright_blue', '#8080ff')}'
    magenta: '{colors.get('bright_magenta', '#ff80ff')}'
    cyan: '{colors.get('bright_cyan', '#80ffff')}'
    white: '{colors.get('bright_white', '#ffffff')}'
"""

    return content


def _generate_kitty(colors: dict, theme_name: str) -> str:
    """Generate Kitty configuration."""
    content = f"""# {theme_name} - Kitty Color Scheme

background {colors.get('background', '#000000')}
foreground {colors.get('foreground', '#ffffff')}
cursor {colors.get('cursor', '#ffffff')}
selection_background {colors.get('selection_bg', '#3e3e3e')}
selection_foreground {colors.get('foreground', '#ffffff')}

color0 {colors.get('black', '#000000')}
color1 {colors.get('red', '#ff0000')}
color2 {colors.get('green', '#00ff00')}
color3 {colors.get('yellow', '#ffff00')}
color4 {colors.get('blue', '#0000ff')}
color5 {colors.get('magenta', '#ff00ff')}
color6 {colors.get('cyan', '#00ffff')}
color7 {colors.get('white', '#ffffff')}

color8 {colors.get('bright_black', '#808080')}
color9 {colors.get('bright_red', '#ff8080')}
color10 {colors.get('bright_green', '#80ff80')}
color11 {colors.get('bright_yellow', '#ffff80')}
color12 {colors.get('bright_blue', '#8080ff')}
color13 {colors.get('bright_magenta', '#ff80ff')}
color14 {colors.get('bright_cyan', '#80ffff')}
color15 {colors.get('bright_white', '#ffffff')}
"""

    return content


def _generate_hyper(colors: dict, theme_name: str) -> str:
    """Generate Hyper JavaScript configuration."""
    content = f"""// {theme_name} - Hyper Color Theme
exports.config = {{
  termCSS: `
    * {{
      backgroundColor: {colors.get('background', '#000000')} !important;
    }}
    .terminal .xterm-viewport {{
      background-color: {colors.get('background', '#000000')} !important;
      color: {colors.get('foreground', '#ffffff')} !important;
    }}
    .cursor {{
      background-color: {colors.get('cursor', '#ffffff')} !important;
      border-color: {colors.get('cursor', '#ffffff')} !important;
    }}
    .selection {{
      background-color: {colors.get('selection_bg', '#3e3e3e')} !important;
    }}
  `,
  colors: {{
    black: '{colors.get('black', '#000000')}',
    red: '{colors.get('red', '#ff0000')}',
    green: '{colors.get('green', '#00ff00')}',
    yellow: '{colors.get('yellow', '#ffff00')}',
    blue: '{colors.get('blue', '#0000ff')}',
    magenta: '{colors.get('magenta', '#ff00ff')}',
    cyan: '{colors.get('cyan', '#00ffff')}',
    white: '{colors.get('white', '#ffffff')}',
    brightBlack: '{colors.get('bright_black', '#808080')}',
    brightRed: '{colors.get('bright_red', '#ff8080')}',
    brightGreen: '{colors.get('bright_green', '#80ff80')}',
    brightYellow: '{colors.get('bright_yellow', '#ffff80')}',
    brightBlue: '{colors.get('bright_blue', '#8080ff')}',
    brightMagenta: '{colors.get('bright_magenta', '#ff80ff')}',
    brightCyan: '{colors.get('bright_cyan', '#80ffff')}',
    brightWhite: '{colors.get('bright_white', '#ffffff')}',
  }},
}};
"""

    return content


def _generate_ghostty(colors: dict, theme_name: str) -> str:
    """Generate Ghostty TOML configuration."""
    content = f"""# {theme_name} - Ghostty Color Theme

[theme]
name = "{theme_name}"

background = "{colors.get('background', '#000000')}"
foreground = "{colors.get('foreground', '#ffffff')}"
cursor = "{colors.get('cursor', '#ffffff')}"
selection-background = "{colors.get('selection_bg', '#3e3e3e')}"
selection-foreground = "{colors.get('foreground', '#ffffff')}"

0 = "{colors.get('black', '#000000')}"      # black
1 = "{colors.get('red', '#ff0000')}"        # red
2 = "{colors.get('green', '#00ff00')}"      # green
3 = "{colors.get('yellow', '#ffff00')}"     # yellow
4 = "{colors.get('blue', '#0000ff')}"       # blue
5 = "{colors.get('magenta', '#ff00ff')}"    # magenta
6 = "{colors.get('cyan', '#00ffff')}"       # cyan
7 = "{colors.get('white', '#ffffff')}"      # white
8 = "{colors.get('bright_black', '#808080')}"      # bright black
9 = "{colors.get('bright_red', '#ff8080')}"        # bright red
10 = "{colors.get('bright_green', '#80ff80')}"     # bright green
11 = "{colors.get('bright_yellow', '#ffff80')}"    # bright yellow
12 = "{colors.get('bright_blue', '#8080ff')}"      # bright blue
13 = "{colors.get('bright_magenta', '#ff80ff')}"   # bright magenta
14 = "{colors.get('bright_cyan', '#80ffff')}"      # bright cyan
15 = "{colors.get('bright_white', '#ffffff')}"     # bright white
"""

    return content


def _generate_terminal(colors: dict, theme_name: str) -> str:
    """Generate Mac Terminal.app plist configuration."""
    import plistlib
    from io import BytesIO

    def hex_to_rgb_plist(hex_color):
        """Convert hex color to RGB tuple for plist (0-65535 range)."""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return (r * 257, g * 257, b * 257)

    plist_dict = {
        'BackgroundColor': hex_to_rgb_plist(colors.get('background', '#000000')),
        'CursorColor': hex_to_rgb_plist(colors.get('cursor', '#ffffff')),
        'SelectionColor': hex_to_rgb_plist(colors.get('selection_bg', '#3e3e3e')),
        'Ansi0Color': hex_to_rgb_plist(colors.get('black', '#000000')),
        'Ansi1Color': hex_to_rgb_plist(colors.get('red', '#ff0000')),
        'Ansi2Color': hex_to_rgb_plist(colors.get('green', '#00ff00')),
        'Ansi3Color': hex_to_rgb_plist(colors.get('yellow', '#ffff00')),
        'Ansi4Color': hex_to_rgb_plist(colors.get('blue', '#0000ff')),
        'Ansi5Color': hex_to_rgb_plist(colors.get('magenta', '#ff00ff')),
        'Ansi6Color': hex_to_rgb_plist(colors.get('cyan', '#00ffff')),
        'Ansi7Color': hex_to_rgb_plist(colors.get('white', '#ffffff')),
        'Ansi8Color': hex_to_rgb_plist(colors.get('bright_black', '#808080')),
        'Ansi9Color': hex_to_rgb_plist(colors.get('bright_red', '#ff8080')),
        'Ansi10Color': hex_to_rgb_plist(colors.get('bright_green', '#80ff80')),
        'Ansi11Color': hex_to_rgb_plist(colors.get('bright_yellow', '#ffff80')),
        'Ansi12Color': hex_to_rgb_plist(colors.get('bright_blue', '#8080ff')),
        'Ansi13Color': hex_to_rgb_plist(colors.get('bright_magenta', '#ff80ff')),
        'Ansi14Color': hex_to_rgb_plist(colors.get('bright_cyan', '#80ffff')),
        'Ansi15Color': hex_to_rgb_plist(colors.get('bright_white', '#ffffff')),
    }

    buffer = BytesIO()
    plistlib.dump(plist_dict, buffer)
    return buffer.getvalue().decode('utf-8')

