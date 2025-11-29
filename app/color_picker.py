"""
Color Picker Widget for the Terminal Color Theme Creator

This module provides interactive color controls with sliders for each terminal color.
"""

import tkinter as tk
from tkinter import ttk
import colorsys


class ColorPicker(tk.Frame):
    """Widget for controlling terminal colors with interactive sliders."""
    
    def __init__(self, parent, initial_colors):
        super().__init__(parent)
        self.colors = initial_colors.copy()
        self.color_vars = {}
        self.color_labels = {}
        self.slider_moved = False  # Track if any slider has been moved
        self.setup_ui()
        
    def setup_ui(self):
        """Create the color picker UI components."""
        # Define the color order for terminals
        self.color_order = [
            ('background', 'Background'),
            ('foreground', 'Foreground'),
            ('cursor', 'Cursor'),
            ('black', 'Black'),
            ('red', 'Red'),
            ('green', 'Green'),
            ('yellow', 'Yellow'),
            ('blue', 'Blue'),
            ('magenta', 'Magenta'),
            ('cyan', 'Cyan'),
            ('white', 'White'),
            ('bright_black', 'Bright Black'),
            ('bright_red', 'Bright Red'),
            ('bright_green', 'Bright Green'),
            ('bright_yellow', 'Bright Yellow'),
            ('bright_blue', 'Bright Blue'),
            ('bright_magenta', 'Bright Magenta'),
            ('bright_cyan', 'Bright Cyan'),
            ('bright_white', 'Bright White')
        ]
        
        for color_key, color_label in self.color_order:
            self.create_color_row(color_key, color_label)
            
    def create_color_row(self, color_key, color_label):
        """Create a row for a single color control."""
        frame = ttk.Frame(self)
        frame.pack(fill=tk.X, pady=5, padx=5)
        
        # Color name
        name_label = ttk.Label(frame, text=color_label, width=15, anchor=tk.W)
        name_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Color preview box
        preview_frame = tk.Frame(frame, width=30, height=20, relief=tk.RIDGE, borderwidth=1)
        preview_frame.pack(side=tk.LEFT, padx=(0, 10))
        preview_frame.pack_propagate(False)
        
        preview_label = tk.Label(preview_frame, bg=self.colors[color_key])
        preview_label.pack(fill=tk.BOTH, expand=True)
        
        # Color value label
        value_label = ttk.Label(frame, text=self.colors[color_key], width=9, anchor=tk.W)
        value_label.pack(side=tk.LEFT, padx=(0, 10))
        self.color_labels[color_key] = value_label
        
        # RGB sliders frame
        sliders_frame = ttk.Frame(frame)
        sliders_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Create RGB sliders
        r_var = tk.DoubleVar(value=self.hex_to_rgb(self.colors[color_key])[0])
        g_var = tk.DoubleVar(value=self.hex_to_rgb(self.colors[color_key])[1])
        b_var = tk.DoubleVar(value=self.hex_to_rgb(self.colors[color_key])[2])
        
        self.color_vars[color_key] = {'r': r_var, 'g': g_var, 'b': b_var}
        
        # Red slider
        r_frame = ttk.Frame(sliders_frame)
        r_frame.pack(fill=tk.X, pady=1)
        ttk.Label(r_frame, text="R:", width=2).pack(side=tk.LEFT)
        r_slider = ttk.Scale(r_frame, from_=0, to=255, variable=r_var, 
                            orient=tk.HORIZONTAL, command=lambda v, ck=color_key: self.update_color(ck))
        r_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        r_value = ttk.Label(r_frame, text=f"{int(r_var.get()):.0f}", width=3)
        r_value.pack(side=tk.LEFT, padx=(5, 0))
        
        # Green slider
        g_frame = ttk.Frame(sliders_frame)
        g_frame.pack(fill=tk.X, pady=1)
        ttk.Label(g_frame, text="G:", width=2).pack(side=tk.LEFT)
        g_slider = ttk.Scale(g_frame, from_=0, to=255, variable=g_var, 
                            orient=tk.HORIZONTAL, command=lambda v, ck=color_key: self.update_color(ck))
        g_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        g_value = ttk.Label(g_frame, text=f"{int(g_var.get()):.0f}", width=3)
        g_value.pack(side=tk.LEFT, padx=(5, 0))
        
        # Blue slider
        b_frame = ttk.Frame(sliders_frame)
        b_frame.pack(fill=tk.X, pady=1)
        ttk.Label(b_frame, text="B:", width=2).pack(side=tk.LEFT)
        b_slider = ttk.Scale(b_frame, from_=0, to=255, variable=b_var, 
                            orient=tk.HORIZONTAL, command=lambda v, ck=color_key: self.update_color(ck))
        b_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        b_value = ttk.Label(b_frame, text=f"{int(b_var.get()):.0f}", width=3)
        b_value.pack(side=tk.LEFT, padx=(5, 0))
        
        # Update slider references
        self.color_vars[color_key]['r_slider'] = r_slider
        self.color_vars[color_key]['g_slider'] = g_slider
        self.color_vars[color_key]['b_slider'] = b_slider
        self.color_vars[color_key]['r_value'] = r_value
        self.color_vars[color_key]['g_value'] = g_value
        self.color_vars[color_key]['b_value'] = b_value
        
        # Hex input
        hex_frame = ttk.Frame(frame)
        hex_frame.pack(side=tk.LEFT, padx=(10, 0))
        ttk.Label(hex_frame, text="#", width=1).pack(side=tk.LEFT)
        
        hex_var = tk.StringVar(value=self.colors[color_key].upper())
        hex_entry = ttk.Entry(hex_frame, textvariable=hex_var, width=7)
        hex_entry.pack(side=tk.LEFT)
        hex_entry.bind('<Return>', lambda e, ck=color_key: self.update_from_hex(ck, hex_var.get()))
        
        self.color_vars[color_key]['hex_var'] = hex_var
        self.color_vars[color_key]['hex_entry'] = hex_entry
        
        # Add separator
        if color_key != 'bright_white':
            separator = ttk.Separator(self, orient='horizontal')
            separator.pack(fill=tk.X, pady=5, padx=5)
            
    def update_color(self, color_key):
        """Update color when slider changes."""
        r = self.color_vars[color_key]['r'].get()
        g = self.color_vars[color_key]['g'].get()
        b = self.color_vars[color_key]['b'].get()
        
        # Update value labels
        self.color_vars[color_key]['r_value'].configure(text=f"{int(r):.0f}")
        self.color_vars[color_key]['g_value'].configure(text=f"{int(g):.0f}")
        self.color_vars[color_key]['b_value'].configure(text=f"{int(b):.0f}")
        
        # Convert to hex
        hex_color = self.rgb_to_hex(int(r), int(g), int(b))
        
        # Update hex input
        self.color_vars[color_key]['hex_var'].set(hex_color.upper())
        
        # Update color in colors dictionary
        self.colors[color_key] = hex_color
        
        # Update color label
        self.color_labels[color_key].configure(text=hex_color)
        
        # Show preview if this is the first slider move
        if not self.slider_moved:
            self.slider_moved = True
            if hasattr(self, 'show_preview_callback'):
                self.show_preview_callback()
        
        # Trigger callback
        if hasattr(self, 'on_color_change'):
            self.on_color_change(color_key, hex_color)
            
    def update_from_hex(self, color_key, hex_value):
        """Update color from hex input."""
        if hex_value.startswith('#') and len(hex_value) == 7:
            try:
                # Validate hex color
                r = int(hex_value[1:3], 16)
                g = int(hex_value[3:5], 16)
                b = int(hex_value[5:7], 16)
                
                # Update variables
                self.color_vars[color_key]['r'].set(r)
                self.color_vars[color_key]['g'].set(g)
                self.color_vars[color_key]['b'].set(b)
                
                # Update the color
                self.update_color(color_key)
                
            except ValueError:
                # Invalid hex, revert to previous value
                self.color_vars[color_key]['hex_var'].set(self.colors[color_key].upper())
                
    def update_colors(self, new_colors):
        """Update all colors with new values."""
        for color_key, color_value in new_colors.items():
            if color_key in self.color_vars:
                # Convert hex to RGB
                r, g, b = self.hex_to_rgb(color_value)
                
                # Update variables
                self.color_vars[color_key]['r'].set(r)
                self.color_vars[color_key]['g'].set(g)
                self.color_vars[color_key]['b'].set(b)
                self.color_vars[color_key]['hex_var'].set(color_value.upper())
                
                # Update the color
                self.update_color(color_key)
                
    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB values."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
    def rgb_to_hex(self, r, g, b):
        """Convert RGB values to hex color."""
        return f"#{r:02x}{g:02x}{b:02x}"
        
    def get_colors(self):
        """Get the current color scheme."""
        return self.colors.copy()
        
    def set_color_change_callback(self, callback):
        """Set callback function for color changes."""
        self.on_color_change = callback
        
    def set_show_preview_callback(self, callback):
        """Set callback function to show preview."""
        self.show_preview_callback = callback
