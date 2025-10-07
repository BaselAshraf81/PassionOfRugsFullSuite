# Passion Of Rugs Advanced Dialer v4.1

Professional dialer application with TrestleIQ API integration, CloudTalk calling, and AI-powered features.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
Edit `config.py` and add your API keys:
- TrestleIQ API key (required)
- CloudTalk credentials (optional)
- OpenAI API key (optional, for AI features)

### 3. Run Application
```bash
python launcher.py
```

### 4. Build Executable (Optional)
```bash
python build_v4.1.py
```

## Core Features

### Professional Dialer Mode
- CloudTalk integration for one-click calling
- TrestleIQ reverse phone/address lookups
- Smart dual caching system (Excel + permanent)
- Call history tracking (one entry per phone)
- Manual and automatic API lookups
- Excel input/output with color coding
- Visual response viewer with HTML rendering
- Google Maps integration

### AI Features (Optional)
- **Automatic address correction** - Fixes malformed addresses and retries API calls
- **Intelligent person filtering** - Identifies original customer from multiple residents
- **Confidence scoring** - High/Medium/Low rankings for contacts
- **Actionable insights** - Best time to call, acceptance probability, recommendations
- **Cost:** ~$0.0005 per person (0.05 cents) using GPT-5 nano

### Bulk Processing Mode
- Batch process Excel files
- Progress tracking
- Caching for efficiency
- Formatted Excel output

## Source Files

### Main Application
- **launcher.py** (145 lines) - Entry point, mode selector
- **dialer_gui.py** (4280 lines) - Professional dialer interface
- **bulk_processor_gui.py** (348 lines) - Bulk processing interface
- **lead_processor_v2.py** (877 lines) - Core API processing logic
- **cache_manager.py** (283 lines) - Permanent cache management
- **ai_assistant.py** (200 lines) - AI address correction & person filtering
- **config.py** (28 lines) - Configuration file

### Build & Documentation
- **build_v4.1.py** - PyInstaller build script
- **requirements.txt** - Python dependencies
- **FUNCTION_REFERENCE.md** - Complete function reference (all functions documented)
- **SETUP.md** - Setup instructions

## Documentation

### Essential Reading
- **FUNCTION_REFERENCE.md** - Complete reference of all functions with locations and descriptions
- **SETUP.md** - Configuration and setup instructions

### For Users
All user documentation has been consolidated into the application's built-in help and tooltips.

### For Developers
- **FUNCTION_REFERENCE.md** contains all function descriptions organized by file
- Each function includes: location (line number), purpose, parameters, return values, and actions

## Requirements

- Python 3.11+
- Windows 10/11
- TrestleIQ API key (required)
- CloudTalk credentials (optional, for calling)
- OpenAI API key (optional, for AI features)

## Data Files (Created at Runtime)

- `call_history.json` - Call history tracking
- `dialer_settings.json` - User preferences
- `lead_processor_cache.json` - Permanent API cache
- `*.xlsx` - Excel input/output files

## Version

**v4.1** - 2025-10-07

**Total Code:** ~6,251 lines across 7 Python files  
**Total Functions:** 100+  
**Features:** Dialer, Bulk Processing, AI Integration, Caching, Call History
