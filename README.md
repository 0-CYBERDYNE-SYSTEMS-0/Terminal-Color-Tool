# Terminal Color Tool

A web-based application for creating, visualizing, and exporting terminal color themes. Extract colors from images, customize with interactive controls, and export to multiple terminal formats.

Built for developers who live in the terminal. Perfect for vibe coders and AI agent builders who want their terminals to match their aesthetic.

<img width="1313" height="801" alt="Screenshot 2025-11-30 at 02 07 29" src="https://github.com/user-attachments/assets/e43ac7c0-aff1-4b93-a99d-ef79df57e81a" />


<img width="1316" height="816" alt="Screenshot 2025-11-30 at 02 02 00" src="https://github.com/user-attachments/assets/ff746581-db2e-49c2-b868-b5b00d6cd6a5" />



## Overview

Terminal Color Tool provides a modern interface for designing terminal color schemes. The application supports image-based color extraction using K-means clustering, real-time preview, and export to 8 different terminal formats including WezTerm, iTerm2, Windows Terminal, and Xresources.

## Features

### Core Functionality
- [img] Image-based color extraction using K-means clustering algorithm
- [ctl] Interactive color controls with RGB sliders and hex input
- [eye] Real-time terminal preview
- [out] Export to 8 terminal formats
- [auto] WezTerm auto-installation support

### Built-in Themes
- Tokyo Night
- Solarized Dark & Light
- Dracula
- Monokai
- Nord
- Gruvbox
- One Dark

### Technical Specifications
- Backend: Python 3.8+, FastAPI, uvicorn
- Frontend: Vanilla JavaScript, Tailwind CSS
- Image Processing: Pillow, scikit-learn
- Package Manager: uv (Python)

## Installation

### Prerequisites
- Python 3.8 or higher
- uv package manager (recommended) or pip

### Setup Steps

#### Option 1: Automated Setup
```bash
git clone https://github.com/0-CYBERDYNE-SYSTEMS-0/Terminal-Color-Tool.git
cd Terminal-Color-Tool
chmod +x setup.sh
./setup.sh
```

#### Option 2: Manual Setup
```bash
# Clone repository
git clone https://github.com/0-CYBERDYNE-SYSTEMS-0/Terminal-Color-Tool.git
cd Terminal-Color-Tool

# Install dependencies with uv
uv sync

# Or install with pip
pip install -r requirements.txt
```

## Usage

### Starting the Application
```bash
uv run python main.py
```

Navigate to `http://127.0.0.1:8000` in your browser.

### Creating a Theme

#### From an Image
1. [img] Upload an image via drag-and-drop or file selector
2. [ctl] Click "Extract Colors from Image" to generate palette
3. [ctl] Adjust colors using RGB sliders or hex input
4. [eye] Preview changes in real-time terminal view
5. [out] Export using "Export Theme" button

#### From Presets
1. [nav] Select a theme from the left sidebar
2. [ctl] Customize colors as needed
3. [out] Export theme

### Export Formats

| Format | Description | Use Case |
|--------|-------------|----------|
| Shell Script | Bash/Zsh compatible color variables | General use |
| JSON | Theme data file | Backup & sharing |
| WezTerm | WezTerm Lua configuration | WezTerm terminal |
| iTerm2 | iTerm2 color profile | macOS iTerm2 |
| Windows Terminal | Windows Terminal JSON | Windows Terminal |
| Xresources | X11 resource database | Linux X11 terminals |

## Development

### Project Structure
```
Terminal-Color-Tool/
├── main.py                    # FastAPI application entry point
├── demo.py                    # CLI demonstration script
├── test_theme_generator.py    # Test suite
├── pyproject.toml            # Python project configuration
├── setup.sh                  # Automated setup script
├── app/
│   ├── api/                  # FastAPI endpoints
│   │   ├── colors.py         # Color extraction endpoint
│   │   └── export.py         # Theme export endpoints
│   ├── static/               # Static web assets
│   │   ├── js/               # JavaScript modules
│   │   └── css/              # Stylesheets
│   ├── templates/
│   │   └── index.html        # Main application page
│   ├── image_processor.py    # Color extraction logic
│   ├── preview.py            # Terminal preview rendering
│   └── export.py             # Legacy export functionality
```

### Running Tests
```bash
uv run python test_theme_generator.py
```

### Key Components

#### Color Extraction (image_processor.py)
- Uses K-means clustering (scikit-learn) to extract dominant colors
- Maps extracted colors to terminal color scheme
- Supports PNG, JPG, JPEG, GIF, BMP, TIFF, WebP

#### Web API (app/api/)
- `/api/extract-colors` - POST endpoint for image color extraction
- `/api/export` - POST endpoint for theme export in various formats

#### Frontend (app/static/)
- Vanilla JavaScript modules for application logic
- Tailwind CSS for styling
- Real-time terminal preview using CSS

## Configuration

### Default Port
The application runs on port 8000 by default. To change:
```python
uvicorn.run("main:app", host="127.0.0.1", port=YOUR_PORT)
```

### Theme Data Structure
Themes are stored as dictionaries with the following structure:
```python
{
    'name': 'Theme Name',
    'colors': {
        'background': '#000000',
        'foreground': '#ffffff',
        'cursor': '#ffffff',
        'black': '#000000',
        'red': '#ff0000',
        'green': '#00ff00',
        'yellow': '#ffff00',
        'blue': '#0000ff',
        'magenta': '#ff00ff',
        'cyan': '#00ffff',
        'white': '#ffffff',
        'bright_black': '#808080',
        'bright_red': '#ff8080',
        'bright_green': '#80ff80',
        'bright_yellow': '#ffff80',
        'bright_blue': '#8080ff',
        'bright_magenta': '#ff80ff',
        'bright_cyan': '#80ffff',
        'bright_white': '#ffffff'
    }
}
```

## API Reference

### POST /api/extract-colors
Extract colors from uploaded image.

**Request:**
- Content-Type: multipart/form-data
- Body: image file

**Response:**
```json
{
    "colors": {
        "background": "#000000",
        "foreground": "#ffffff",
        ...
    }
}
```

### POST /api/export
Export theme in specified format.

**Request:**
```json
{
    "format": "wezterm",
    "theme_data": {
        "name": "Theme Name",
        "colors": { ... }
    },
    "wezterm_mode": "complete"
}
```

**Response:**
- File content based on format parameter

## Troubleshooting

### Common Issues

#### Missing Tkinter
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS (included with Python)
# Already available

# Windows (included with Python)
# Already available
```

#### Port 8000 Occupied
```bash
# Kill existing processes
pkill -f "uvicorn"

# Use alternative port
uvicorn.run("main:app", host="127.0.0.1", port=8001)
```

#### Color Display Issues
- Verify terminal supports 24-bit color
- Use Shell Script export for maximum compatibility
- Check terminal emulator color settings

## Dependencies

### Core Dependencies
- Python 3.8+
- fastapi >= 0.100.0
- uvicorn >= 0.23.0
- pillow >= 9.0.0
- scikit-learn >= 1.0.0
- numpy >= 1.20.0
- python-multipart >= 0.0.6
- jinja2 >= 3.1.0

### Development Dependencies
- pytest >= 6.0 (for testing)

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/feature-name`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/feature-name`)
5. Submit pull request

## References

- [Solarized Color Scheme](http://ethanschoonover.com/solarized)
- [WezTerm Terminal](https://wezfurlong.org/wezterm/)
- [scikit-learn KMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)
