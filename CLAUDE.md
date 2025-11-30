# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🚀 Quick Start Commands

### Setup
```bash
# Initial setup (installs uv and dependencies)
./setup.sh

# Alternative: Manual setup
uv sync
```

### Running the Application

**Web UI (Primary Interface - FastAPI)**
```bash
uv run python main.py
# Server starts on http://127.0.0.1:8000
```

**Command-line Demo**
```bash
uv run python demo.py
```

**Run Tests**
```bash
uv run python test_theme_generator.py
```

### Development

The project uses **uv** for Python package management. All commands should be run with `uv run` to ensure proper virtual environment isolation.

**Key Development Tasks:**
- **Add new export format**: Edit `app/api/export.py` and add generator function
- **Modify web UI**: Update `app/templates/index.html` and corresponding JS files in `app/static/js/`
- **Enhance color extraction**: Modify `app/image_processor.py`
- **Add API endpoints**: Create new routers in `app/api/` and include in `main.py`

## 📁 Project Architecture

This is a **Terminal Color Theme Creator** with a modern web-based interface (FastAPI + Vanilla JS) for creating and exporting terminal color themes from images or custom palettes.

### Technology Stack
- **Backend**: FastAPI (Python web framework)
- **Frontend**: Vanilla JavaScript + Tailwind CSS (CDN)
- **Image Processing**: Pillow + scikit-learn (K-means clustering)
- **Package Manager**: uv (Python)
- **Legacy GUI**: tkinter (see `app/main_window.py` - historical version)

### Core Application Flow

1. **User uploads image** → API `/api/extract-colors` → K-means clustering extracts dominant colors
2. **Colors mapped** to terminal color scheme (background, foreground, 16 ANSI colors)
3. **Real-time preview** updates as user adjusts sliders
4. **Export** via API `/api/export` → Generates theme files (shell scripts, JSON, Xresources, iTerm2, Windows Terminal, WezTerm, etc.)

### Directory Structure

```
theme-viz/
├── main.py                     # FastAPI app entry point (Web UI server)
├── demo.py                     # Command-line demonstration
├── test_theme_generator.py     # Test suite
├── pyproject.toml             # Project config (uv dependencies)
├── requirements.txt           # Python dependencies (legacy)
├── setup.sh                   # Setup script (installs uv + sync)
│
├── app/
│   ├── api/                   # FastAPI endpoints
│   │   ├── colors.py         # POST /api/extract-colors
│   │   └── export.py         # POST /api/export (8 formats supported)
│   │
│   ├── static/
│   │   ├── js/
│   │   │   ├── app.js        # Main application logic
│   │   │   ├── colorPicker.js # Color slider controls
│   │   │   ├── preview.js    # Terminal preview rendering
│   │   │   └── export.js     # Export modal handlers
│   │   └── css/
│   │       └── styles.css    # Custom styles
│   │
│   ├── templates/
│   │   └── index.html        # Main web UI (Tailwind CSS + vanilla JS)
│   │
│   ├── image_processor.py    # Core: Color extraction from images (K-means)
│   ├── export.py             # Legacy export logic (tkinter version)
│   ├── main_window.py        # Legacy tkinter GUI
│   ├── color_picker.py       # Legacy color controls
│   └── preview.py            # Legacy terminal preview
│
└── README.md                  # User documentation
├── USER_WORKFLOW.md          # Step-by-step usage guide
└── UX_IMPROVEMENTS.md        # UI/UX enhancement history
```

### Key Modules

**`app/image_processor.py`**
- Image color extraction using K-means clustering (scikit-learn)
- Maps extracted colors to terminal color scheme (16 ANSI colors + background/foreground/cursor)
- Supported formats: PNG, JPG, JPEG, GIF, BMP, TIFF, WebP

**`app/api/colors.py`**
- FastAPI endpoint: `POST /api/extract-colors`
- Accepts image upload, returns color palette as JSON

**`app/api/export.py`**
- FastAPI endpoint: `POST /api/export`
- Supports 8 export formats:
  - `ansi` - ANSI escape codes (shell)
  - `json` - Theme JSON file
  - `xresources` - X11 terminal config
  - `shell` - Shell setup script
  - `registry` - Windows Registry
  - `iterm2` - iTerm2 (macOS)
  - `winterm` - Windows Terminal
  - `wezterm` - WezTerm terminal (with auto-install support)

**`app/templates/index.html`**
- Main web UI (Tailwind CSS via CDN)
- 3-panel layout: Image upload | Color controls | Terminal preview
- Vanilla JavaScript (no frameworks)

## 🎨 Export Formats

The application exports terminal themes in multiple formats:

1. **Shell Script** (recommended) - Bash/Zsh script with color variables
2. **JSON** - Save/load theme files
3. **Xresources** - Linux X11 terminals
4. **iTerm2** - macOS Terminal.app replacement
5. **Windows Terminal** - Windows 10/11 terminal
6. **WezTerm** - Modern terminal with auto-install functionality
7. **Registry** - Windows legacy terminal
8. **ANSI Codes** - Raw escape sequences

### WezTerm Integration

Recent feature: WezTerm export includes auto-install functionality that:
- Generates theme definition (Lua format)
- Creates callback handler for theme switching
- Saves files to WezTerm config directory (~/.config/wezterm/)

## 🧪 Testing

**Run test suite:**
```bash
uv run python test_theme_generator.py
```

Tests cover:
- ImageProcessor initialization
- Color extraction logic
- Export format generation
- Color validation

**Test without GUI** (CI/CD friendly):
- `demo.py` - Command-line demonstration
- `test_theme_generator.py` - Automated tests

## 📦 Dependencies

**Core** (pyproject.toml):
- `Pillow` - Image processing
- `scikit-learn` - K-means clustering for color extraction
- `numpy` - Array operations
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `python-multipart` - File uploads
- `jinja2` - HTML templating

## 🔧 Common Development Patterns

### Adding New Export Format

1. Add format to `ExportRequest` model in `app/api/export.py` (line 15)
2. Create generator function `_generate_<format>()`
3. Add to `generators` and `extensions` dictionaries (lines 70-100)
4. Update `index.html` export modal with new option

### Modifying Web UI

- **HTML structure**: `app/templates/index.html`
- **Styling**: Tailwind classes in HTML + custom CSS in `app/static/css/styles.css`
- **JavaScript logic**: Files in `app/static/js/`
- **API calls**: Made to `/api/extract-colors` and `/api/export`

### Color Processing

Colors are stored as hex strings (`#RRGGBB`) and mapped to terminal color names:
- `background`, `foreground`, `cursor`
- 8 standard colors: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`
- 8 bright colors: `bright_black` through `bright_white`

## 🚢 Deployment Notes

- Web application runs on **FastAPI/uvicorn**
- Default: `127.0.0.1:8000` (localhost only)
- Static files served from `app/static/`
- Templates served from `app/templates/`
- No database - all state in client-side JavaScript

## 📚 Documentation

- **README.md** - User-focused documentation and usage guide
- **USER_WORKFLOW.md** - Step-by-step workflow guide with examples
- **UX_IMPROVEMENTS.md** - History of UI/UX enhancements and solutions

## 🔄 Version History

Recent significant changes (see `git log --oneline`):
- **bc1bcf2**: Refactored from tkinter GUI to FastAPI + Vanilla JS web UI
- **6967c05**: Added WezTerm export with auto-install functionality
- **295f989**: Fixed WezTerm auto-install (theme definition + callback handler)

## 💡 Tips

- Use `uv` for all Python commands (ensures proper venv)
- FastAPI server auto-reloads on code changes (development mode)
- Image processing optimizes to 150x150px for performance
- All color operations use hex strings (#RRGGBB format)
- WezTerm integration requires Lua configuration file generation
- Export API validates colors and provides fallbacks for missing values
