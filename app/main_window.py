"""
Main Window for the Terminal Color Theme Creator

This module contains the main application window that brings together all components
of the color theme creator.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
from pathlib import Path

from .color_picker import ColorPicker
from .image_processor import ImageProcessor
from .preview import PreviewPanel
from .export import ExportManager


class ThemeCreatorApp:
    """Main application window for creating terminal color themes."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Terminal Color Theme Creator")
        self.root.geometry("1200x800")
        
        # Configure grid weights for responsive design
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_columnconfigure(2, weight=1)
        
        # Initialize theme data
        self.theme_data = {
            'name': 'My New Theme',
            'description': '',
            'colors': {
                'background': '#1e1e1e',
                'foreground': '#d4d4d4',
                'cursor': '#ffffff',
                'black': '#000000',
                'red': '#cd3131',
                'green': '#0dbc79',
                'yellow': '#e5e510',
                'blue': '#2472c8',
                'magenta': '#bc3fbc',
                'cyan': '#11a8cd',
                'white': '#e5e5e5',
                'bright_black': '#666666',
                'bright_red': '#f14c4c',
                'bright_green': '#23d18b',
                'bright_yellow': '#f5f543',
                'bright_blue': '#3b8eea',
                'bright_magenta': '#d670d6',
                'bright_cyan': '#29b8db',
                'bright_white': '#e5e5e5'
            }
        }
        
        # UI state variables
        self.preview_collapsed = False
        self.color_controls_collapsed = False
        self.preview_visible = False  # Track if preview should be visible
        
        # Create UI components
        self.create_menu()
        self.create_main_layout()
        self.create_theme_presets()
        
        # Initialize managers
        self.image_processor = ImageProcessor()
        self.export_manager = ExportManager()
        
    def create_menu(self):
        """Create the application menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Theme", command=self.new_theme)
        file_menu.add_command(label="Save Theme", command=self.save_theme)
        file_menu.add_command(label="Load Theme", command=self.load_theme)
        file_menu.add_separator()
        file_menu.add_command(label="Export", command=self.show_export_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def create_main_layout(self):
        """Create the main application layout."""
        # Create main frames
        self.create_left_panel()
        self.create_center_panel()
        self.create_right_panel()
        
    def create_left_panel(self):
        """Create the left panel with image upload and color extraction."""
        left_frame = ttk.Frame(self.root, padding="10")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Image upload section
        image_container = ttk.Frame(left_frame)
        image_container.pack(fill=tk.BOTH, expand=True)
        
        # Image upload header with collapse button
        image_header = ttk.Frame(image_container)
        image_header.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(image_header, text="Reference Image", font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        self.collapse_image_btn = ttk.Button(image_header, text="−", width=3, 
                                            command=self.toggle_image_section)
        self.collapse_image_btn.pack(side=tk.RIGHT)
        
        self.image_frame = ttk.Frame(image_container, relief=tk.GROOVE, borderwidth=2)
        self.image_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Image placeholder
        self.image_label = ttk.Label(self.image_frame, text="Click to upload image", 
                                   background='#f0f0f0', relief=tk.SUNKEN)
        self.image_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.image_label.bind('<Button-1>', self.upload_image)
        
        # Color extraction button
        ttk.Button(left_frame, text="Extract Colors from Image", 
                  command=self.extract_colors).pack(fill=tk.X, pady=5)
        
        # Store reference for collapsing
        self.image_container = image_container
        
    def create_center_panel(self):
        """Create the center panel with color controls."""
        center_frame = ttk.Frame(self.root, padding="10")
        center_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create scrollable container for center panel content
        canvas = tk.Canvas(center_frame)
        scrollbar = ttk.Scrollbar(center_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Color controls container
        self.color_container = ttk.Frame(scrollable_frame)
        self.color_container.pack(fill=tk.BOTH, expand=True)
        
        # Color picker header with collapse button
        color_header = ttk.Frame(self.color_container)
        color_header.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(color_header, text="Color Controls", font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        self.collapse_color_btn = ttk.Button(color_header, text="−", width=3, 
                                            command=self.toggle_color_section)
        self.collapse_color_btn.pack(side=tk.RIGHT)
        
        # Color picker widget directly in the scrollable frame
        self.color_picker = ColorPicker(scrollable_frame, self.theme_data['colors'])
        self.color_picker.pack(fill=tk.BOTH, expand=True)
        
        # Set callback for showing preview when sliders are moved
        self.color_picker.set_show_preview_callback(self.show_preview)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_right_panel(self):
        """Create the right panel with preview and export options."""
        right_frame = ttk.Frame(self.root, padding="10")
        right_frame.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create scrollable container for all right panel content
        canvas = tk.Canvas(right_frame)
        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Theme name and description
        ttk.Label(scrollable_frame, text="Theme Details", font=('Arial', 12, 'bold')).pack(pady=(0, 10))
        
        name_frame = ttk.Frame(scrollable_frame)
        name_frame.pack(fill=tk.X, pady=5)
        ttk.Label(name_frame, text="Name:").pack(side=tk.LEFT)
        self.name_entry = ttk.Entry(name_frame)
        self.name_entry.insert(0, self.theme_data['name'])
        self.name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        desc_frame = ttk.Frame(scrollable_frame)
        desc_frame.pack(fill=tk.X, pady=5)
        ttk.Label(desc_frame, text="Description:").pack(anchor=tk.W)
        self.desc_text = tk.Text(desc_frame, height=3, wrap=tk.WORD)
        self.desc_text.pack(fill=tk.X, pady=(5, 0))
        
        # Preview container with collapse functionality
        self.preview_container = ttk.Frame(scrollable_frame)
        self.preview_container.pack(fill=tk.BOTH, expand=True)
        
        # Preview header with collapse button
        preview_header = ttk.Frame(self.preview_container)
        preview_header.pack(fill=tk.X, pady=(20, 10))
        
        ttk.Label(preview_header, text="Terminal Preview", font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        self.collapse_preview_btn = ttk.Button(preview_header, text="−", width=3, 
                                              command=self.toggle_preview_section)
        self.collapse_preview_btn.pack(side=tk.RIGHT)
        
        # Preview content frame
        self.preview_frame = ttk.Frame(self.preview_container)
        # Initially don't show preview frame
        # self.preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create single preview panel but don't pack it initially
        self.preview = PreviewPanel(self.preview_frame, self.theme_data['colors'])
        # self.preview.pack(fill=tk.BOTH, expand=True)
        
        # Fixed Export button at bottom - make it prominent
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill=tk.X, pady=(20, 10))
        
        # Create a prominent export button with styling
        export_button = ttk.Button(button_frame, text="🚀 EXPORT THEME", 
                                 command=self.show_export_dialog, style='Export.TButton')
        export_button.pack(fill=tk.X, pady=5)
        
        # Add style for the export button
        style = ttk.Style()
        style.configure('Export.TButton', font=('Arial', 12, 'bold'))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_theme_presets(self):
        """Create theme presets dropdown."""
        preset_frame = ttk.Frame(self.root, padding="10")
        preset_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(preset_frame, text="Quick Themes:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 5))
        
        self.preset_var = tk.StringVar()
        self.preset_combo = ttk.Combobox(preset_frame, textvariable=self.preset_var, 
                                        values=["Custom", "Tokyo Night", "Solarized Dark", "Solarized Light", "Dracula", "Monokai", "Nord", "Ocean"],
                                        state="readonly", width=15)
        self.preset_combo.pack(side=tk.LEFT)
        self.preset_combo.bind('<<ComboboxSelected>>', self.load_preset)
        
        # Add theme info button
        ttk.Button(preset_frame, text="?", width=3, 
                  command=self.show_preset_info).pack(side=tk.RIGHT, padx=(10, 0))
        
    def upload_image(self, event=None):
        """Open file dialog to upload an image."""
        file_path = filedialog.askopenfilename(
            title="Select Reference Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        
        if file_path:
            # Display the image (placeholder for now)
            self.image_label.configure(text=f"Image loaded: {os.path.basename(file_path)}")
            self.current_image_path = file_path
            
    def extract_colors(self):
        """Extract colors from the uploaded image."""
        if hasattr(self, 'current_image_path'):
            colors = self.image_processor.extract_colors(self.current_image_path)
            if colors:
                self.color_picker.update_colors(colors)
                self.preview.update_colors(colors)
                self.show_preview()
                messagebox.showinfo("Success", "Colors extracted successfully!")
            else:
                messagebox.showwarning("Warning", "Could not extract colors from image")
        else:
            messagebox.showwarning("Warning", "Please upload an image first")
            
    def load_preset(self, event=None):
        """Load a preset theme."""
        preset = self.preset_var.get()
        
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
            },
            "Solarized Light": {
                'background': '#fdf6e3',
                'foreground': '#657b83',
                'cursor': '#268bd2',
                'black': '#073642',
                'red': '#dc322f',
                'green': '#586e75',
                'yellow': '#657b83',
                'blue': '#268bd2',
                'magenta': '#d33682',
                'cyan': '#2aa198',
                'white': '#fdf6e3',
                'bright_black': '#002b36',
                'bright_red': '#cb4b16',
                'bright_green': '#93a1a1',
                'bright_yellow': '#839496',
                'bright_blue': '#6c71c4',
                'bright_magenta': '#dc322f',
                'bright_cyan': '#2aa198',
                'bright_white': '#fdf6e3'
            },
            "Dracula": {
                'background': '#282a36',
                'foreground': '#f8f8f2',
                'cursor': '#f8f8f2',
                'black': '#21222c',
                'red': '#ff5555',
                'green': '#50fa7b',
                'yellow': '#f1fa8c',
                'blue': '#bd93f9',
                'magenta': '#ff79c6',
                'cyan': '#8be9fd',
                'white': '#f8f8f2',
                'bright_black': '#6272a4',
                'bright_red': '#ff5555',
                'bright_green': '#50fa7b',
                'bright_yellow': '#f1fa8c',
                'bright_blue': '#bd93f9',
                'bright_magenta': '#ff79c6',
                'bright_cyan': '#8be9fd',
                'bright_white': '#f8f8f2'
            },
            "Monokai": {
                'background': '#272822',
                'foreground': '#f8f8f2',
                'cursor': '#f8f8f2',
                'black': '#272822',
                'red': '#f92672',
                'green': '#a6e22e',
                'yellow': '#f4bf75',
                'blue': '#66d9ef',
                'magenta': '#ae81ff',
                'cyan': '#a1efe4',
                'white': '#f8f8f2',
                'bright_black': '#75715e',
                'bright_red': '#f92672',
                'bright_green': '#a6e22e',
                'bright_yellow': '#f4bf75',
                'bright_blue': '#66d9ef',
                'bright_magenta': '#ae81ff',
                'bright_cyan': '#a1efe4',
                'bright_white': '#f8f8f2'
            },
            "Nord": {
                'background': '#2e3440',
                'foreground': '#d8dee9',
                'cursor': '#d8dee9',
                'black': '#2e3440',
                'red': '#bf616a',
                'green': '#a3be8c',
                'yellow': '#ebcb8b',
                'blue': '#81a1c1',
                'magenta': '#b48ead',
                'cyan': '#88c0d0',
                'white': '#d8dee9',
                'bright_black': '#4c566a',
                'bright_red': '#bf616a',
                'bright_green': '#a3be8c',
                'bright_yellow': '#ebcb8b',
                'bright_blue': '#81a1c1',
                'bright_magenta': '#b48ead',
                'bright_cyan': '#88c0d0',
                'bright_white': '#eceff4'
            },
            "Ocean": {
                'background': '#001b33',
                'foreground': '#76c4de',
                'cursor': '#76c4de',
                'black': '#001b33',
                'red': '#ff5458',
                'green': '#62d196',
                'yellow': '#ffd866',
                'blue': '#65b7ff',
                'magenta': '#c297ff',
                'cyan': '#6ae4e4',
                'white': '#76c4de',
                'bright_black': '#003366',
                'bright_red': '#ff5458',
                'bright_green': '#62d196',
                'bright_yellow': '#ffd866',
                'bright_blue': '#65b7ff',
                'bright_magenta': '#c297ff',
                'bright_cyan': '#6ae4e4',
                'bright_white': '#c8e6ff'
            }
        }
        
        if preset in presets:
            self.color_picker.update_colors(presets[preset])
            self.preview.update_colors(presets[preset])
            self.show_preview()
            
    def new_theme(self):
        """Create a new theme."""
        if messagebox.askyesno("New Theme", "Create a new theme? Unsaved changes will be lost."):
            self.theme_data['colors'] = {
                'background': '#1e1e1e',
                'foreground': '#d4d4d4',
                'cursor': '#ffffff',
                'black': '#000000',
                'red': '#cd3131',
                'green': '#0dbc79',
                'yellow': '#e5e510',
                'blue': '#2472c8',
                'magenta': '#bc3fbc',
                'cyan': '#11a8cd',
                'white': '#e5e5e5',
                'bright_black': '#666666',
                'bright_red': '#f14c4c',
                'bright_green': '#23d18b',
                'bright_yellow': '#f5f543',
                'bright_blue': '#3b8eea',
                'bright_magenta': '#d670d6',
                'bright_cyan': '#29b8db',
                'bright_white': '#e5e5e5'
            }
            self.color_picker.update_colors(self.theme_data['colors'])
            self.preview.update_colors(self.theme_data['colors'])
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, "New Theme")
            self.desc_text.delete(1.0, tk.END)
            
    def save_theme(self):
        """Save the current theme."""
        theme_name = self.name_entry.get() or "Untitled Theme"
        theme_description = self.desc_text.get(1.0, tk.END).strip()
        
        self.theme_data['name'] = theme_name
        self.theme_data['description'] = theme_description
        
        # Create themes directory if it doesn't exist
        themes_dir = Path(__file__).parent.parent / "themes"
        themes_dir.mkdir(exist_ok=True)
        
        # Save theme as JSON
        theme_path = themes_dir / "user_themes" / f"{theme_name.lower().replace(' ', '_')}.json"
        
        try:
            with open(theme_path, 'w') as f:
                json.dump(self.theme_data, f, indent=2)
            messagebox.showinfo("Success", f"Theme saved as {theme_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save theme: {str(e)}")
            
    def load_theme(self):
        """Load a saved theme."""
        file_path = filedialog.askopenfilename(
            title="Load Theme",
            filetypes=[("JSON files", "*.json")],
            initialdir=Path(__file__).parent.parent / "themes" / "user_themes"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    loaded_data = json.load(f)
                
                self.theme_data.update(loaded_data)
                self.color_picker.update_colors(self.theme_data['colors'])
                self.preview.update_colors(self.theme_data['colors'])
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, self.theme_data['name'])
                self.desc_text.delete(1.0, tk.END)
                self.desc_text.insert(1.0, self.theme_data.get('description', ''))
                
                self.show_preview()
                messagebox.showinfo("Success", f"Theme loaded: {self.theme_data['name']}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load theme: {str(e)}")
                
    def show_preview(self):
        """Show the terminal preview when colors are set."""
        if hasattr(self, 'preview_frame') and not self.preview_visible:
            # Pack the preview frame and child widgets
            self.preview_frame.pack(fill=tk.BOTH, expand=True)
            self.preview.pack(fill=tk.BOTH, expand=True)
            self.preview_visible = True
        
    def show_export_dialog(self):
        """Show the export dialog."""
        from .export import ExportDialog
        dialog = ExportDialog(self.root, self.theme_data)
        self.root.wait_window(dialog.dialog)
        
    def show_about(self):
        """Show the about dialog."""
        messagebox.showinfo("About", 
                          "Terminal Color Theme Creator\n\n"
                          "A simple, intuitive application for creating and exporting terminal color themes.\n\n"
                          "Features:\n"
                          "• Extract colors from images\n"
                          "• Interactive color sliders\n"
                          "• Real-time preview\n"
                          "• Export to multiple formats")
    
    def toggle_image_section(self):
        """Toggle image upload section visibility."""
        if hasattr(self, 'image_frame'):
            if self.image_frame.winfo_viewable():
                # Collapse
                self.image_frame.pack_forget()
                self.collapse_image_btn.configure(text="+")
            else:
                # Expand
                self.image_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
                self.collapse_image_btn.configure(text="−")
    
    def toggle_color_section(self):
        """Toggle color controls section visibility."""
        if hasattr(self, 'color_container'):
            if self.color_container.winfo_viewable():
                # Collapse
                self.color_container.pack_forget()
                self.collapse_color_btn.configure(text="+")
            else:
                # Expand
                self.color_container.pack(fill=tk.BOTH, expand=True)
                self.collapse_color_btn.configure(text="−")
    
    def toggle_preview_section(self):
        """Toggle preview section visibility."""
        if hasattr(self, 'preview_frame'):
            if self.preview_frame.winfo_viewable():
                # Collapse
                self.preview_frame.pack_forget()
                self.collapse_preview_btn.configure(text="+")
                self.preview_visible = False
            else:
                # Expand
                self.preview_frame.pack(fill=tk.BOTH, expand=True)
                self.preview.pack(fill=tk.BOTH, expand=True)
                self.collapse_preview_btn.configure(text="−")
                self.preview_visible = True
    
    def show_preset_info(self):
        """Show preset theme information."""
        info_text = """Popular Terminal Themes:

• Tokyo Night: Modern dark theme with blue accents
• Solarized Dark: Balanced low-contrast theme
• Solarized Light: Light alternative to Solarized
• Dracula: High contrast dark theme
• Monokai: Vibrant dark theme
• Nord: Cold color palette
• Ocean: Ocean-inspired colors

Click a theme name to load it as a starting point!"""
        
        messagebox.showinfo("Theme Presets", info_text)
