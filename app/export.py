"""
Export Manager for the Terminal Color Theme Creator

This module provides functionality to export terminal color themes
in various formats including ANSI, JSON, Xresources, and shell scripts.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import os
from pathlib import Path


class ExportDialog:
    """Simplified dialog for exporting themes."""
    
    def __init__(self, parent, theme_data):
        self.theme_data = theme_data
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Export Theme - Simple")
        self.dialog.geometry("700x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Export settings
        self.export_format = tk.StringVar(value="shell")  # Default to most useful format
        self.save_location = tk.StringVar(value=str(Path.home()))
        
        self.create_ui()
        
    def create_ui(self):
        """Create the simplified export dialog UI."""
        # Main container
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Export Your Theme", font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Theme info
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Label(info_frame, text=f"Theme: {self.theme_data['name']}", 
                 font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        # Format selection with clear descriptions
        format_frame = ttk.LabelFrame(main_frame, text="Choose Export Format", padding="10")
        format_frame.pack(fill=tk.X, pady=(0, 15))
        
        formats = [
            ("🖥️ Terminal Setup Script (Recommended)", "shell", "Easy copy-paste setup"),
            ("💾 Theme JSON File", "json", "Save theme for later use"),
            ("⚙️ Xresources Configuration", "xresources", "For Linux terminals"),
            ("🪟 Windows Registry", "registry", "For Windows Terminal"),
            ("🎨 iTerm2 Theme", "iterm2", "For macOS Terminal"),
            ("📄 ANSI Escape Codes", "ansi", "Raw color codes")
        ]
        
        for text, value, desc in formats:
            frame = ttk.Frame(format_frame)
            frame.pack(fill=tk.X, pady=2)
            
            ttk.Radiobutton(frame, text=text, variable=self.export_format, 
                           value=value, command=self.update_preview).pack(anchor=tk.W)
            ttk.Label(frame, text=desc, font=('Arial', 8)).pack(anchor=tk.W, padx=(20, 0))
        
        # Save location
        location_frame = ttk.Frame(main_frame)
        location_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(location_frame, text="Save Location:").pack(anchor=tk.W)
        
        loc_frame = ttk.Frame(location_frame)
        loc_frame.pack(fill=tk.X, pady=5)
        
        ttk.Entry(loc_frame, textvariable=self.save_location).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(loc_frame, text="Browse", command=self.browse_location).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Preview section
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.preview_text = scrolledtext.ScrolledText(preview_frame, height=10, wrap=tk.WORD)
        self.preview_text.pack(fill=tk.BOTH, expand=True)
        
        # Instructions
        instructions = ttk.Label(main_frame, text="💡 Tip: For most users, 'Terminal Setup Script' is the easiest option!", 
                               font=('Arial', 10), foreground='blue')
        instructions.pack(pady=(0, 10))
        
        # Simplified buttons
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X)
        
        ttk.Button(buttons_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.RIGHT)
        ttk.Button(buttons_frame, text="Export Theme", command=self.export_theme).pack(side=tk.RIGHT, padx=(10, 0))
        
        # Update preview on load
        self.update_preview()
        
    def browse_location(self):
        """Browse for save location."""
        folder = filedialog.askdirectory(initialdir=self.save_location.get())
        if folder:
            self.save_location.set(folder)
            self.update_preview()
        
    def update_preview(self):
        """Update the preview with a more user-friendly display."""
        format_type = self.export_format.get()
        self.preview_text.delete(1.0, tk.END)
        
        # Generate preview content
        content = self.get_export_content(format_type, include_comments=True)
        
        # Add helpful context
        if format_type == "shell":
            preview = f"# Terminal Theme: {self.theme_data['name']}\n"
            preview += f"# Save this as 'setup_{self.theme_data['name'].lower().replace(' ', '_')}.sh'\n"
            preview += f"# Then run: source setup_{self.theme_data['name'].lower().replace(' ', '_')}.sh\n\n"
            preview += content
        elif format_type == "json":
            preview = f"# JSON Theme File\n"
            preview += f"# Save as: {self.theme_data['name'].lower().replace(' ', '_')}.json\n"
            preview += f"# You can load this file later in the application\n\n"
            preview += content
        else:
            preview = f"## {self.theme_data['name']} Theme\n"
            preview += f"Format: {format_type.upper()}\n\n"
            preview += content
        
        self.preview_text.insert(1.0, preview)
        
    def get_export_content(self, format_type, include_comments=True):
        """Get the export content for the selected format."""
        colors = self.theme_data['colors']
        theme_name = self.theme_data['name']
        
        if format_type == "ansi":
            content = self._generate_ansi_export(colors, theme_name, include_comments)
        elif format_type == "json":
            content = self._generate_json_export(colors, theme_name, include_comments)
        elif format_type == "xresources":
            content = self._generate_xresources_export(colors, theme_name, include_comments)
        elif format_type == "shell":
            content = self._generate_shell_export(colors, theme_name, include_comments)
        elif format_type == "registry":
            content = self._generate_registry_export(colors, theme_name, include_comments)
        elif format_type == "iterm2":
            content = self._generate_iterm2_export(colors, theme_name, include_comments)
        elif format_type == "winterm":
            content = self._generate_winterm_export(colors, theme_name, include_comments)
        else:
            content = "# Unsupported format"
            
        return content
        
    def _generate_ansi_export(self, colors, theme_name, include_comments=True):
        """Generate ANSI escape codes export."""
        lines = []
        
        if include_comments:
            lines.append(f"# Terminal Color Theme: {theme_name}")
            lines.append("# ANSI escape codes for terminal colors")
            lines.append("# Copy these colors to your shell configuration (e.g., .bashrc, .zshrc)")
            lines.append("")
        
        # Basic ANSI colors
        ansi_map = {
            'black': 0,
            'red': 1,
            'green': 2,
            'yellow': 3,
            'blue': 4,
            'magenta': 5,
            'cyan': 6,
            'white': 7
        }
        
        bright_map = {
            'bright_black': 8,
            'bright_red': 9,
            'bright_green': 10,
            'bright_yellow': 11,
            'bright_blue': 12,
            'bright_magenta': 13,
            'bright_cyan': 14,
            'bright_white': 15
        }
        
        for color_name, ansi_code in ansi_map.items():
            if include_comments:
                lines.append(f"# {color_name.upper()}: {colors[color_name]}")
            lines.append(f"export COLOR_{color_name.upper()}='{colors[color_name]}'")
            
        for color_name, ansi_code in bright_map.items():
            if include_comments:
                lines.append(f"# {color_name.upper()}: {colors[color_name]}")
            lines.append(f"export COLOR_{color_name.upper()}='{colors[color_name]}'")
            
        if include_comments:
            lines.append("")
            lines.append("# Special colors")
            lines.append(f"# Background: {colors['background']}")
            lines.append(f"# Foreground: {colors['foreground']}")
            lines.append(f"# Cursor: {colors['cursor']}")
            
        return "\n".join(lines)
        
    def _generate_json_export(self, colors, theme_name, include_comments=True):
        """Generate JSON export."""
        content = json.dumps(self.theme_data, indent=2)
        
        if include_comments:
            header = f"# Terminal Color Theme: {theme_name}\n"
            header += "# JSON format for easy sharing and loading\n\n"
            return header + content
        else:
            return content
            
    def _generate_xresources_export(self, colors, theme_name, include_comments=True):
        """Generate Xresources export."""
        lines = []
        
        if include_comments:
            lines.append(f"! Terminal Color Theme: {theme_name}")
            lines.append("! Xresources format for X11 terminals")
            lines.append("! Add these to your ~/.Xresources file")
            lines.append("! xrdb -merge ~/.Xresources")
            lines.append("")
        
        # Base colors
        lines.append(f"*background: {colors['background']}")
        lines.append(f"*foreground: {colors['foreground']}")
        lines.append(f"*cursorColor: {colors['cursor']}")
        lines.append("")
        
        # Standard ANSI colors
        lines.append("!! Black")
        lines.append(f"*color0: {colors['black']}")
        lines.append(f"*color8: {colors['bright_black']}")
        lines.append("")
        
        lines.append("!! Red")
        lines.append(f"*color1: {colors['red']}")
        lines.append(f"*color9: {colors['bright_red']}")
        lines.append("")
        
        lines.append("!! Green")
        lines.append(f"*color2: {colors['green']}")
        lines.append(f"*color10: {colors['bright_green']}")
        lines.append("")
        
        lines.append("!! Yellow")
        lines.append(f"*color3: {colors['yellow']}")
        lines.append(f"*color11: {colors['bright_yellow']}")
        lines.append("")
        
        lines.append("!! Blue")
        lines.append(f"*color4: {colors['blue']}")
        lines.append(f"*color12: {colors['bright_blue']}")
        lines.append("")
        
        lines.append("!! Magenta")
        lines.append(f"*color5: {colors['magenta']}")
        lines.append(f"*color13: {colors['bright_magenta']}")
        lines.append("")
        
        lines.append("!! Cyan")
        lines.append(f"*color6: {colors['cyan']}")
        lines.append(f"*color14: {colors['bright_cyan']}")
        lines.append("")
        
        lines.append("!! White")
        lines.append(f"*color7: {colors['white']}")
        lines.append(f"*color15: {colors['bright_white']}")
        
        return "\n".join(lines)
        
    def _generate_shell_export(self, colors, theme_name, include_comments=True):
        """Generate shell script export."""
        lines = []
        
        if include_comments:
            lines.append(f"# Terminal Color Theme: {theme_name}")
            lines.append("# Shell script to apply colors to various terminals")
            lines.append("")
        
        # Function to set colors
        lines.append("set_terminal_colors() {")
        lines.append("    # ANSI color variables")
        lines.append(f"    local background='{colors['background']}'")
        lines.append(f"    local foreground='{colors['foreground']}'")
        lines.append(f"    local cursor='{colors['cursor']}'")
        lines.append("")
        
        # Color variables
        color_vars = [
            ('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'),
            ('bright_black', 'bright_red', 'bright_green', 'bright_yellow', 
             'bright_blue', 'bright_magenta', 'bright_cyan', 'bright_white')
        ]
        
        for brightness in color_vars:
            for color in brightness:
                lines.append(f"    local {color}='{colors[color]}'")
                
        lines.append("")
        lines.append("    # Export colors")
        lines.append("    export background")
        lines.append("    export foreground")
        lines.append("    export cursor")
        
        for color in color_vars[0] + color_vars[1]:
            lines.append(f"    export {color}")
            
        lines.append("}")
        lines.append("")
        
        # Terminal-specific settings
        if include_comments:
            lines.append("# Apply colors to specific terminals")
            lines.append("")
        
        # Xterm/XTerm-compatible
        lines.append("# For Xterm-like terminals:")
        lines.append("if [[ \"$COLORTERM\" == *truecolor* || \"$COLORTERM\" == *24bit* ]]; then")
        lines.append("    # Truecolor support")
        lines.append("    printf \"\\e]4;0;%s\\\"\\\"\\\\\" \"$black\"")
        lines.append("    printf \"\\e]4;1;%s\\\"\\\"\\\\\" \"$red\"")
        lines.append("    printf \"\\e]4;2;%s\\\"\\\"\\\\\" \"$green\"")
        lines.append("    printf \"\\e]4;3;%s\\\"\\\"\\\\\" \"$yellow\"")
        lines.append("    printf \"\\e]4;4;%s\\\"\\\"\\\\\" \"$blue\"")
        lines.append("    printf \"\\e]4;5;%s\\\"\\\"\\\\\" \"$magenta\"")
        lines.append("    printf \"\\e]4;6;%s\\\"\\\"\\\\\" \"$cyan\"")
        lines.append("    printf \"\\e]4;7;%s\\\"\\\"\\\\\" \"$white\"")
        lines.append("    printf \"\\e]4;8;%s\\\"\\\"\\\\\" \"$bright_black\"")
        lines.append("    printf \"\\e]4;9;%s\\\"\\\"\\\\\" \"$bright_red\"")
        lines.append("    printf \"\\e]4;10;%s\\\"\\\"\\\\\" \"$bright_green\"")
        lines.append("    printf \"\\e]4;11;%s\\\"\\\"\\\\\" \"$bright_yellow\"")
        lines.append("    printf \"\\e]4;12;%s\\\"\\\"\\\\\" \"$bright_blue\"")
        lines.append("    printf \"\\e]4;13;%s\\\"\\\"\\\\\" \"$bright_magenta\"")
        lines.append("    printf \"\\e]4;14;%s\\\"\\\"\\\\\" \"$bright_cyan\"")
        lines.append("    printf \"\\e]4;15;%s\\\"\\\"\\\\\" \"$bright_white\"")
        lines.append("")
        lines.append("    # Set background and foreground")
        lines.append("    printf \"\\e]10;%s\\\"\\\"\\\\\" \"$foreground\"")
        lines.append("    printf \"\\e]11;%s\\\"\\\"\\\\\" \"$background\"")
        lines.append("    printf \"\\e]12;%s\\\"\\\"\\\\\" \"$cursor\"")
        lines.append("fi")
        
        return "\n".join(lines)
        
    def _generate_registry_export(self, colors, theme_name, include_comments=True):
        """Generate Windows Registry export."""
        lines = []
        
        if include_comments:
            lines.append(f"; Terminal Color Theme: {theme_name}")
            lines.append("; Windows Registry Editor Version 5.00")
            lines.append("; Import into Registry to apply theme (Windows Terminal)")
            lines.append("")
        
        lines.append("[HKEY_CURRENT_USER\\Software\\Microsoft\\Terminal\\Profiles\\\\]")
        lines.append(f"; Terminal Color Theme: {theme_name}")
        lines.append("")
        
        # Add color mappings
        color_map = {
            'background': 'background',
            'foreground': 'foreground',
            'black': 'black',
            'red': 'red',
            'green': 'green',
            'yellow': 'yellow',
            'blue': 'blue',
            'magenta': 'purple',
            'cyan': 'cyan',
            'white': 'white',
            'bright_black': 'blackBright',
            'bright_red': 'redBright',
            'bright_green': 'greenBright',
            'bright_yellow': 'yellowBright',
            'bright_blue': 'blueBright',
            'bright_magenta': 'purpleBright',
            'bright_cyan': 'cyanBright',
            'bright_white': 'whiteBright'
        }
        
        for color_key, reg_key in color_map.items():
            lines.append(f'["{reg_key}"]')
            lines.append(f'@="{colors[color_key]}"')
            lines.append("")
            
        return "\n".join(lines)
        
    def _generate_iterm2_export(self, colors, theme_name, include_comments=True):
        """Generate iTerm2 theme export."""
        lines = []
        
        if include_comments:
            lines.append(f"# Terminal Color Theme: {theme_name}")
            lines.append("# iTerm2 theme")
            lines.append("# Import this file in iTerm2 → Preferences → Profiles → Colors → Color Presets")
            lines.append("")
        
        lines.append("{")
        lines.append('  "Ansi 0 Color": "' + colors['black'] + '",')
        lines.append('  "Ansi 1 Color": "' + colors['red'] + '",')
        lines.append('  "Ansi 2 Color": "' + colors['green'] + '",')
        lines.append('  "Ansi 3 Color": "' + colors['yellow'] + '",')
        lines.append('  "Ansi 4 Color": "' + colors['blue'] + '",')
        lines.append('  "Ansi 5 Color": "' + colors['magenta'] + '",')
        lines.append('  "Ansi 6 Color": "' + colors['cyan'] + '",')
        lines.append('  "Ansi 7 Color": "' + colors['white'] + '",')
        lines.append('  "Ansi 8 Color": "' + colors['bright_black'] + '",')
        lines.append('  "Ansi 9 Color": "' + colors['bright_red'] + '",')
        lines.append('  "Ansi 10 Color": "' + colors['bright_green'] + '",')
        lines.append('  "Ansi 11 Color": "' + colors['bright_yellow'] + '",')
        lines.append('  "Ansi 12 Color": "' + colors['bright_blue'] + '",')
        lines.append('  "Ansi 13 Color": "' + colors['bright_magenta'] + '",')
        lines.append('  "Ansi 14 Color": "' + colors['bright_cyan'] + '",')
        lines.append('  "Ansi 15 Color": "' + colors['bright_white'] + '",')
        lines.append('  "Background Color": "' + colors['background'] + '",')
        lines.append('  "Foreground Color": "' + colors['foreground'] + '",')
        lines.append('  "Cursor Color": "' + colors['cursor'] + '",')
        lines.append('  "Cursor Text Color": "' + colors['foreground'] + '",')
        lines.append('  "Selection Color": "' + colors['bright_black'] + '",')
        lines.append('  "Bold Color": "' + colors['foreground'] + '",')
        lines.append('  "Cursor Guide Color": "' + colors['bright_black'] + '"')
        lines.append("}")
        
        return "\n".join(lines)
        
    def _generate_winterm_export(self, colors, theme_name, include_comments=True):
        """Generate Windows Terminal theme export."""
        lines = []
        
        if include_comments:
            lines.append(f"# Terminal Color Theme: {theme_name}")
            lines.append("# Windows Terminal theme")
            lines.append("# Add this to your profiles.json in Windows Terminal settings")
            lines.append("")
        
        lines.append('{')
        lines.append('  "name": "' + theme_name + '",')
        lines.append('  "cursorColor": "' + colors['cursor'] + '",')
        lines.append('  "cursorShape": "bar",')
        lines.append('  "background": "' + colors['background'] + '",')
        lines.append('  "foreground": "' + colors['foreground'] + '",')
        lines.append('  "selectionBackground": "' + colors['bright_black'] + '",')
        lines.append('  "colorScheme": "' + theme_name.lower().replace(' ', '_') + '",')
        lines.append('  "acrylicOpacity": 0.8,')
        lines.append('  "useAcrylic": false,')
        lines.append('  "fontFace": "Consolas",')
        lines.append('  "fontSize": 12,')
        lines.append('  "antialiasing": "greyscale",')
        lines.append('')
        
        # Color schemes
        lines.append('  "schemes": [')
        lines.append('    {')
        lines.append('      "name": "' + theme_name.lower().replace(' ', '_') + '",')
        lines.append('      "background": "' + colors['background'] + '",')
        lines.append('      "foreground": "' + colors['foreground'] + '",')
        lines.append('      "cursorColor": "' + colors['cursor'] + '",')
        lines.append('      "selectionBackground": "' + colors['bright_black'] + '",')
        lines.append('      "black": "' + colors['black'] + '",')
        lines.append('      "red": "' + colors['red'] + '",')
        lines.append('      "green": "' + colors['green'] + '",')
        lines.append('      "yellow": "' + colors['yellow'] + '",')
        lines.append('      "blue": "' + colors['blue'] + '",')
        lines.append('      "purple": "' + colors['magenta'] + '",')
        lines.append('      "cyan": "' + colors['cyan'] + '",')
        lines.append('      "white": "' + colors['white'] + '",')
        lines.append('      "brightBlack": "' + colors['bright_black'] + '",')
        lines.append('      "brightRed": "' + colors['bright_red'] + '",')
        lines.append('      "brightGreen": "' + colors['bright_green'] + '",')
        lines.append('      "brightYellow": "' + colors['bright_yellow'] + '",')
        lines.append('      "brightBlue": "' + colors['bright_blue'] + '",')
        lines.append('      "brightPurple": "' + colors['bright_magenta'] + '",')
        lines.append('      "brightCyan": "' + colors['bright_cyan'] + '",')
        lines.append('      "brightWhite": "' + colors['bright_white'] + '"')
        lines.append('    }')
        lines.append('  ]')
        lines.append('}')
        
        return "\n".join(lines)
        
    def export_theme(self):
        """Export the theme to a file."""
        format_type = self.export_format.get()
        
        # Determine file extension
        extensions = {
            "ansi": ".sh",
            "json": ".json",
            "xresources": ".xr",
            "shell": ".sh",
            "registry": ".reg",
            "iterm2": ".itermcolors",
            "winterm": ".json"
        }
        
        ext = extensions.get(format_type, ".txt")
        default_filename = f"{self.custom_filename.get()}{ext}"
        
        # Ask user for save location
        file_path = filedialog.asksaveasfilename(
            title="Save Theme File",
            defaultextension=ext,
            initialfile=default_filename,
            filetypes=[(f"{format_type.upper()} files", f"*{ext}"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                # Get export content
                content = self.get_export_content(format_type, include_comments=self.include_comments.get())
                
                # Write to file
                with open(file_path, 'w') as f:
                    f.write(content)
                    
                messagebox.showinfo("Export Complete", f"Theme exported successfully to:\n{file_path}")
                self.dialog.destroy()
                
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export theme:\n{str(e)}")


class ExportManager:
    """Manages theme exports."""
    
    def __init__(self):
        pass
        
    def export_ansi(self, colors, theme_name, file_path):
        """Export theme as ANSI codes."""
        dialog = ExportDialog(None, {'name': theme_name, 'colors': colors})
        dialog.export_format.set("ansi")
        dialog.custom_filename.set(theme_name.lower().replace(' ', '_'))
        dialog.export_theme()
        
    def export_json(self, colors, theme_name, file_path):
        """Export theme as JSON."""
        dialog = ExportDialog(None, {'name': theme_name, 'colors': colors})
        dialog.export_format.set("json")
        dialog.custom_filename.set(theme_name.lower().replace(' ', '_'))
        dialog.export_theme()
