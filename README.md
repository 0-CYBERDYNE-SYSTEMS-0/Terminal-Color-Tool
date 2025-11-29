# Terminal Color Theme Creator 🎨

A simple, intuitive application for creating and exporting terminal color themes from images or custom palettes.

## Features

- **🖼️ Image-based color extraction**: Upload images to automatically generate color palettes
- **🎛️ Interactive UI**: Color sliders and intuitive controls for fine-tuning themes
- **📤 Multiple export formats**: ANSI escape codes, JSON, Xresources, Windows Terminal, iTerm2, and more
- **👀 Real-time preview**: See how themes look in a simulated terminal
- **🎨 Preset themes**: Includes popular themes like Tokyo Night, Solarized, Dracula, Monokai
- **🔄 Cross-platform**: Works on macOS, Windows, and Linux

## 🚀 Quick Start - 3 Steps to Amazing Terminal Themes!

### Step 1: Setup (One-time only)
```bash
# Make the setup script executable
chmod +x setup.sh

# Run the setup script
./setup.sh
```

### Step 2: Launch
```bash
# Launch the beautiful GUI app
uv run python main.py
```

### Step 3: Create Your Theme!
Follow the simple 3-step process in the app:
1. **Upload Reference Image** (Optional) - Click the left panel to upload an image for color inspiration
2. **Fine-tune Colors** - Use the center sliders to perfect your color scheme  
3. **Export Instantly** - Click "Export Theme" and choose your preferred format

## ✨ Simple & Intuitive User Journey

### For Image-Based Themes:
1. **📸 Upload Image** - Click the upload area in the left panel
2. **🎨 Extract Colors** - Click "Extract Colors from Image" 
3. **🔧 Adjust Colors** - Fine-tune using the color sliders
4. **💾 Export Theme** - Click "Export Theme" and choose "Terminal Setup Script"

### For Preset Themes:
1. **🎯 Select Preset** - Use the dropdown at the bottom to choose "Tokyo Night", "Solarized", etc.
2. **🔧 Tweak Colors** - Adjust sliders to customize the preset
3. **💾 Export Theme** - Click "Export Theme" and select your preferred format

### For Custom Themes from Scratch:
1. **🎨 Start Sliders** - Begin with the default colors
2. **🔧 Adjust Colors** - Use the intuitive RGB sliders to build your theme
3. **💾 Export Theme** - Click the big "Export Theme" button

## 🎯 Export Made Simple - No More Confusion!

The export dialog now gives you crystal-clear options:

**🖥️ Terminal Setup Script (Recommended)**
- **Perfect for beginners** - Just copy-paste commands
- **Works with most terminals** - Bash, Zsh, Fish, etc.
- **One-click setup** - Source the script and you're done

**💾 Theme JSON File** 
- **Save for later** - Load and edit anytime
- **Share themes** - Easy to share with friends
- **Backup your creations** - Never lose your themes

**🎨 Other Formats** (Advanced users)
- Xresources, Windows Terminal, iTerm2, etc.
- Choose based on your specific terminal setup

## 📖 How to Use Exported Themes

### Terminal Setup Script (Easiest!)
```bash
# Save the exported script as 'my_theme.sh'
# Then run:
source my_theme.sh

# That's it! Your terminal is now themed!
```

### For Terminal-Specific Apps:
- **Windows Terminal**: Import the .json file in settings
- **iTerm2**: Import the .itermcolors file via Preferences → Profiles → Colors
- **Linux Xterm**: Use the Xresources file with `xrdb -merge ~/.Xresources`

## 🎨 Creating Perfect Themes - Pro Tips

### Color Harmony:
- **Start with presets** - Tokyo Night and Solarized are professionally designed
- **Use photos as inspiration** - Nature photos have natural color harmony
- **Keep contrast high** - Ensure text is readable against your background

### Terminal Best Practices:
- **Dark backgrounds work best** - Easier on the eyes for long coding sessions
- **Bright foreground colors** - Text should pop against the background
- **Consistent color scheme** - Use similar color families across all 16 colors

## Manual Setup (Optional)

If you prefer not to use uv, you can still use pip:

```bash
# Install dependencies
pip install pillow scikit-learn numpy

# Install tkinter if needed (varies by OS):
# Ubuntu/Debian: sudo apt-get install python3-tk
# macOS: Usually included with Python
# Windows: Usually included with Python

# Run the application
python main.py
```

## Usage

### GUI Version

1. Run `uv run python main.py`
2. Upload an image or select a preset theme
3. Adjust colors using the RGB sliders or hex input
4. Preview the theme in the terminal panel
5. Export in your preferred format

### Demo Version

Run `uv run python demo.py` to see the command-line interface:
- Extract colors from sample images
- Generate theme files
- Export in multiple formats

## Export Formats

The application supports exporting themes for:

- **Shell scripts** (ANSI escape codes)
- **JSON themes** (various terminal emulators)
- **Xresources** (X11 terminals)
- **Windows Terminal** themes
- **iTerm2** themes
- **Windows Registry** files
- **Shell profile generators**

## Project Structure

```
theme-viz/
├── main.py                 # Entry point
├── pyproject.toml          # Project configuration
├── setup.sh               # Setup script
├── demo.py                # Command-line demo
├── test_theme_generator.py # Test suite
├── app/                   # Application modules
│   ├── main_window.py     # Main GUI
│   ├── color_picker.py    # Color controls
│   ├── image_processor.py # Color extraction
│   ├── preview.py         # Terminal preview
│   └── export.py          # Export functionality
└── themes/               # Theme presets
    └── presets.json       # Default themes
```

## Why uv?

Using uv provides several benefits:

- **Fast dependency resolution** - Much faster than pip
- **Automatic virtual environments** - No need to manually create/manage venv
- **Consistent environments** - Ensures reproducible setups across systems
- **Modern Python packaging** - Uses current Python packaging standards
- **Simplified workflow** - Single command to run the application

## Requirements

- Python 3.8+
- uv (optional, but recommended)
- tkinter (for GUI version)

## Development

### Running Tests

```bash
uv run python test_theme_generator.py
```

### Adding New Export Formats

Add export functionality in `app/export.py`:
- Follow the existing pattern in existing export functions
- Add corresponding tests in `test_theme_generator.py`
- Update the export menu in the main window if GUI-related

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the test suite
5. Submit a pull request

## License

MIT License - feel free to use and modify this project!
