# Passion Of Rugs Advanced Dialer v4.1

Professional dialer application with TrestleIQ API integration and CloudTalk calling.

## Quick Start

### Setup Configuration
**Option 1: Use setup script (recommended)**
```bash
python setup.py
```

**Option 2: Manual setup**
1. Copy the template config file:
   ```bash
   copy config.template.py config.py
   ```
2. Edit `config.py` and add your API keys:
   - TrestleIQ API key
   - CloudTalk credentials (optional)

### Run Application
```bash
python launcher.py
```

### Build Executable
```bash
pip install -r requirements.txt
python build_v4.1.py
```

## Files

### Source Code
- `launcher.py` - Main entry point (mode selector)
- `dialer_gui.py` - Professional Dialer Mode
- `bulk_processor_gui.py` - Bulk Processing Mode
- `lead_processor_v2.py` - Core API processing logic
- `cache_manager.py` - Permanent cache management
- `config.py` - Configuration (optional)

### Build
- `build_v4.1.py` - PyInstaller build script
- `requirements.txt` - Python dependencies

### Documentation
- `CODE_MAP_v4.1.md` - Complete code reference
- `AI_FEATURES.md` - AI features guide

### Data Files (Created at Runtime)
- `call_history.json` - Call history
- `dialer_settings.json` - User settings
- `lead_processor_cache.json` - API cache
- `*.xlsx` - Excel input/output files

### Reference
- `Names+phones+address.html` - HTML extraction reference

## Features

- Professional Dialer with CloudTalk integration
- TrestleIQ API for reverse phone/address lookups
- **NEW: AI-powered address correction (GPT-5 nano - cheapest)**
- **NEW: Intelligent person filtering & insights**
- Smart caching system (reduces API costs)
- Call history tracking
- Excel input/output with formatting
- Visual response viewer
- Google Maps integration

## Requirements

- Python 3.11+
- Windows 10/11
- TrestleIQ API key
- CloudTalk credentials (optional)

## Version

**v4.1** - 2025-10-06
