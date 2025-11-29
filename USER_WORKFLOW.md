# 🎨 Terminal Color Theme Creator - User Workflow Guide

## 🚀 Quick Start - The Simple 3-Step Process

### Step 1: Launch the Application
```bash
uv run python main.py
```

### Step 2: Create Your Theme
Choose one of three simple methods:

#### Method A: From an Image (Recommended for Beginners)
1. **📸 Upload Image**: Click the upload area in the left panel
2. **🎨 Extract Colors**: Click "Extract Colors from Image" 
3. **🔧 Adjust**: Fine-tune using the center color sliders
4. **💾 Export**: Click "Export Theme" → Choose "Terminal Setup Script"

#### Method B: From a Preset (Easiest Customization)
1. **🎯 Select Preset**: Use the dropdown at the bottom → Choose "Tokyo Night", "Solarized", etc.
2. **🔧 Tweak**: Adjust any sliders to customize the colors
3. **💾 Export**: Click "Export Theme" → Select your preferred format

#### Method C: From Scratch (Full Control)
1. **🎨 Start Fresh**: Begin with the default colors
2. **🔧 Build**: Use the RGB sliders to build your perfect theme
3. **💾 Export**: Click the big "Export Theme" button

### Step 3: Apply Your Theme

#### For Terminal Setup Script (Easiest!):
```bash
# Save the exported script as 'my_theme.sh'
# Then run:
source my_theme.sh

# That's it! Your terminal is now themed!
```

#### For Specific Terminal Apps:
- **Windows Terminal**: Import the .json file via Settings → Profiles
- **iTerm2**: Import the .itermcolors file via Preferences → Profiles → Colors
- **Linux Xterm**: Use the Xresources file with `xrdb -merge ~/.Xresources`

## 🎯 Export Options - Clear & Simple

### 🖥️ Terminal Setup Script (RECOMMENDED)
- **Perfect for**: Beginners, most users
- **What it does**: Creates a shell script you can source
- **How to use**: `source setup_your_theme.sh`
- **Why it's great**: Works with bash, zsh, fish - just copy-paste!

### 💾 Theme JSON File
- **Perfect for**: Saving, sharing, editing later
- **What it does**: Saves your theme as a JSON file
- **How to use**: Load it back into the app anytime
- **Why it's great**: Easy to share with friends, backup your creations

### 🎨 Other Formats (Advanced Users)
- **Xresources**: For Linux X11 terminals
- **Windows Registry**: For Windows Terminal setup
- **iTerm2 Theme**: For macOS Terminal
- **ANSI Codes**: Raw color codes for scripting

## 🔧 Advanced Features

### Saving & Loading Themes
1. **Save**: Enter theme name/description → Click "Save Theme" (in File menu)
2. **Load**: File → Load Theme → Select your JSON file

### Menu Options
- **File → New Theme**: Start fresh (prompts to save changes)
- **File → Save Theme**: Save current theme as JSON
- **File → Load Theme**: Load a previously saved theme
- **File → Export**: Open export dialog (same as "Export Theme" button)
- **Help → About**: See app information

### Pro Tips for Better Themes

#### Color Harmony
- **Start with presets**: Tokyo Night and Solarized are professionally designed
- **Use photos**: Nature photos have natural color harmony
- **Contrast is key**: Ensure text is readable against your background

#### Terminal Best Practices
- **Dark backgrounds**: Easier on eyes for long coding sessions
- **Bright foregrounds**: Text should pop against background
- **Consistent scheme**: Use similar color families across all 16 colors
- **Test in real terminals**: See how colors look in your actual terminal

### Troubleshooting

#### Common Issues

**"Tkinter not found" error**:
- You need to install tkinter for your Python version
- macOS: Reinstall Python with tkinter support
- Linux: `sudo apt-get install python3-tk`
- Windows: Usually included with Python

**Colors don't look right in terminal**:
- Some terminals have limited color support (8-bit vs 24-bit)
- Try the Terminal Setup Script format for better compatibility
- Check your terminal's color support settings

**Export file not working**:
- Make sure you saved the file in the correct location
- Check file permissions
- Try the Terminal Setup Script format first

#### Getting Help

1. **Check the README**: Detailed documentation and examples
2. **Run the demo**: `uv run python demo.py` to see command-line usage
3. **Run tests**: `uv run python test_theme_generator.py` to verify everything works
4. **File bug reports**: Include your system info and error messages

## 🎨 Example Theme Creation Workflow

### Creating a "Ocean Breeze" Theme

1. **Upload Image**: Find a beautiful ocean photo
2. **Extract Colors**: Click "Extract Colors from Image"
3. **Adjust Colors**: 
   - Make background a bit darker: `#0a1628`
   - Increase foreground contrast: `#e0f2fe`
   - Tune blues: `#60a5fa` → `#3b82f6`
4. **Name Your Theme**: "Ocean Breeze"
5. **Export**: Choose "Terminal Setup Script"
6. **Apply**: `source setup_ocean_breeze.sh`
7. **Enjoy**: Your terminal now has a beautiful ocean theme!

## 🔄 Tips & Tricks

### Speed Up Your Workflow
- **Use presets** as starting points - much faster than building from scratch
- **Keyboard shortcuts** in the app (when available)
- **Batch export** multiple formats for testing
- **Save frequently** to avoid losing your work

### Sharing Themes
- **JSON files** are perfect for sharing - just send the .json file
- **Terminal Setup Scripts** work for most users - easy to apply
- **Include instructions** for specific terminal setups

### Backup & Organization
- **Save themes regularly** using the File → Save Theme option
- **Organize by purpose** (e.g., "Daytime", "Night", "Coding", "Writing")
- **Date your themes** if you're experimenting with different versions
- **Export backups** in multiple formats

---

🎉 **You're ready to create amazing terminal themes!**

Remember: The app is designed to be simple and intuitive. Start with presets or images, tweak what you like, and export in the format that works best for you. Happy theming! 🌈
