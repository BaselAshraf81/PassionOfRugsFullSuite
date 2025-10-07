# Passion Of Rugs Advanced Dialer v4.1 - Code Map

## Core Source Files

### 1. launcher.py (145 lines)
**Purpose:** Main entry point - Mode selector

**Classes:**
- `LauncherGUI` - Main launcher window

**Key Functions:**
- `__init__()` - Initialize launcher
- `create_ui()` - Create mode selection UI
- `start_mode1()` - Launch Bulk Processing Mode
- `start_mode2()` - Launch Professional Dialer Mode

---

### 2. dialer_gui.py (~2800 lines)
**Purpose:** Professional Dialer Mode - Main application

**Classes:**
- `CloudTalkAPI` - CloudTalk API integration for calling
- `ExcelCache` - Excel-based cache for processed data
- `DialerGUI` - Main dialer interface

**Key Functions:**

#### Setup & Initialization
- `__init__()` - Initialize dialer
- `show_setup_screen()` - Configuration screen
- `start_dialer()` - Initialize and start dialer
- `load_settings()` / `save_settings()` - Settings management

#### Data Loading & Processing
- `load_person()` - Load person data (checks cache first)
- `perform_lookups()` - Perform API lookups with auto settings
- `process_lookup_data()` - Process raw API responses into results
- `extract_people_from_data()` - Recursive extraction of people/phones/addresses

#### Manual API Calls
- `manual_phone_lookup()` - Manual phone API call (always from API)
- `manual_address_lookup()` - Manual address API call (always from API)
- `accumulate_phone_results()` - Add phone data to existing results
- `accumulate_address_results()` - Add address data to existing results

#### Navigation
- `next_person()` / `prev_person()` - Navigate between people
- `next_result()` / `prev_result()` - Navigate between results
- `next_phone()` / `prev_phone()` - Navigate between phone numbers

#### Display
- `display_current_result()` - Display current result data
- `show_full_response()` - Show full API response viewer
- `generate_visual_html()` - Generate HTML for visual view

#### Call Management
- `make_call()` - Initiate CloudTalk call
- `call_worker()` - Background call worker
- `flash_status_dropdown()` - Flash status after call
- `add_to_call_history()` - Add/update call history entry
- `save_pending_call_history()` - Save history when navigating

#### Data Persistence
- `save_results_to_excel()` - Save results to Excel (prevents duplicates)
- `update_data_in_excel()` - Update status/notes in Excel
- `on_status_change()` - Handle status changes
- `on_notes_change()` - Handle notes changes

#### Cache Management
- `show_cache_stats()` - Display cache statistics
- `clear_cache_confirm()` - Clear cache with confirmation

---

### 3. bulk_processor_gui.py (348 lines)
**Purpose:** Bulk Processing Mode

**Classes:**
- `BulkProcessorGUI` - Bulk processing interface

**Key Functions:**
- `__init__()` - Initialize bulk processor
- `create_ui()` - Create UI
- `start_processing()` - Start batch processing
- `process_worker()` - Background processing worker
- `update_progress()` - Update progress bar

---

### 4. lead_processor_v2.py (783 lines)
**Purpose:** Core API processing logic

**Classes:**
- `LeadProcessor` - Main processing engine

**Key Functions:**
- `__init__()` - Initialize with API key and cache
- `parse_address()` - Parse address strings into components
- `clean_phone()` - Clean and format phone numbers
- `phone_lookup()` - TrestleIQ reverse phone lookup
- `address_lookup()` - TrestleIQ reverse address lookup
- `extract_age()` - Extract age from person data
- `format_address()` - Format address from data
- `process_row()` - Process single row (with caching)
- `process_excel_file_bulk()` - Bulk Excel processing
- `create_excel_output()` - Create formatted Excel output

---

### 5. cache_manager.py (283 lines)
**Purpose:** Permanent cache management

**Classes:**
- `CacheManager` - Persistent cache for API responses

**Key Functions:**
- `__init__()` - Initialize cache
- `normalize_phone()` - Normalize phone to E.164 format
- `load_cache()` / `save_cache()` - Load/save cache from disk
- `get_cached_lookup()` - Get cached API responses
- `store_lookup()` - Store API responses (only if has results)
- `clear_cache()` - Clear all cached data
- `get_statistics()` - Get cache statistics

---

### 6. ai_assistant.py (~200 lines)
**Purpose:** AI-powered address correction and person filtering

**Classes:**
- `AIAssistant` - OpenAI GPT-4o-mini integration

**Key Functions:**
- `__init__()` - Initialize with API key
- `test_connection()` - Test OpenAI API connection
- `correct_address()` - Correct malformed addresses using AI
- `filter_and_rank_contacts()` - Intelligently filter and rank contacts

**Features:**
- Automatic address correction with retry
- Intelligent person matching from API responses
- Confidence scoring (High/Medium/Low)
- Actionable insights and recommendations
- Cost-effective using GPT-4o-mini

---

### 7. config.py (28 lines)
**Purpose:** Configuration file (optional)

**Variables:**
- `API_KEY` - TrestleIQ API key
- `BASE_URL` - TrestleIQ API base URL
- CloudTalk configuration
- File paths
- Column mappings

---

## Build Files

### 8. build_v4.1.py
**Purpose:** PyInstaller build script

**Configuration:**
- Executable name: PassionOfRugs_Dialer_v4.1.exe
- Build type: Onedir (faster startup)
- Includes: All dependencies
- Excludes: Unnecessary modules (matplotlib, numpy, etc.)
- Optimizations: Enabled

---

## Data Files

### Runtime Files (Created by Application)
- `call_history.json` - Call history tracking
- `dialer_settings.json` - User settings
- `lead_processor_cache.json` - Permanent API cache
- `processed_leads.xlsx` - Output Excel file

### Input Files
- Excel files with columns: name, phone, address, city, state, zip, age

---

## Key Features by File

### dialer_gui.py
- ✅ CloudTalk integration
- ✅ TrestleIQ API integration
- ✅ **NEW: AI Overview & Filtering tab**
- ✅ **NEW: AI-powered address correction**
- ✅ **NEW: Intelligent person matching**
- ✅ Dual caching (Excel + permanent)
- ✅ Call history (one entry per phone)
- ✅ Manual API buttons (always call API)
- ✅ Auto API settings (phone/address)
- ✅ Data accumulation
- ✅ Full response viewer with Visual View
- ✅ Google Maps integration
- ✅ Fixed layout (no jumping)
- ✅ Status dropdown flashing

### lead_processor_v2.py
- ✅ Address parsing (intelligent)
- ✅ Phone normalization
- ✅ API integration (phone & address)
- ✅ **NEW: AI address correction with automatic retry**
- ✅ Caching support
- ✅ Excel output with formatting
- ✅ Color coding (green/red)
- ✅ Dropdown validation

### cache_manager.py
- ✅ Permanent storage (JSON)
- ✅ Phone normalization (E.164)
- ✅ Statistics tracking
- ✅ Cost savings calculation
- ✅ Atomic writes (safe)

### ai_assistant.py
- ✅ OpenAI GPT-4o-mini integration
- ✅ Address correction with reasoning
- ✅ Person filtering and ranking
- ✅ Confidence scoring
- ✅ Actionable insights generation
- ✅ Cost-effective token usage

---

## Data Flow

### Loading a Person
```
1. load_person(index)
2. Check permanent cache (cache_manager)
3. If cached with results:
   - Load raw API responses
   - Process through process_lookup_data()
   - Extract people/phones/addresses
   - Display results
4. If not cached:
   - perform_lookups() based on auto settings
   - Call API if auto_phone_lookup ON
   - Call API if auto_address_lookup ON
   - Store in cache (only if has results)
   - Process and display
```

### Manual API Call
```
1. User clicks manual phone/address button
2. Always call API (bypass cache)
3. Get existing data from cache (to preserve)
4. accumulate_phone_results() or accumulate_address_results()
5. Extract and merge with existing data
6. Update cache with combined data
7. Save to Excel
8. Display updated results
```

### Call History
```
1. User makes call
2. Track: last_called_phone, last_called_name
3. Flash status dropdown
4. User sets status/notes (saved to Excel only)
5. User navigates to next person
6. save_pending_call_history() called
7. Check if entry exists for phone
8. Update existing or create new entry
9. Save to call_history.json
10. Clear tracking variables
```

### Caching Strategy
```
API Call → Check if has results (owners/residents)
         → YES: Store in cache
         → NO: Don't store (empty response)

Load Person → Check cache
           → Has data: Use cached responses
           → No data: Call API
           → Empty cache: Call API (don't use empty)
```

---

## Settings

### Auto API Settings (2 checkboxes)
- `auto_phone_lookup` - Auto phone API when loading person
- `auto_address_lookup` - Auto address API when loading person

### Other Settings (Always Enabled)
- CloudTalk integration
- Caching system
- Call history tracking

---

## Dependencies

### Required
- pandas - Excel file handling
- openpyxl - Excel formatting
- requests - API calls
- tkinter - GUI (built-in)

### Optional
- tkinterweb - Visual HTML view

### Build
- pyinstaller - Create executable

---

## File Sizes
- dialer_gui.py: ~2800 lines (main application)
- lead_processor_v2.py: 783 lines (core logic)
- bulk_processor_gui.py: 348 lines (bulk mode)
- cache_manager.py: 283 lines (caching)
- launcher.py: 145 lines (entry point)
- config.py: 28 lines (configuration)

**Total: ~4,387 lines of Python code**

---

## Version Information

**Application:** Passion Of Rugs Advanced Dialer  
**Version:** 4.1  
**Date:** 2025-10-06  
**Python:** 3.11+  
**Platform:** Windows 10/11  

---

## Quick Reference

### Start Application
```bash
python launcher.py
```

### Build Executable
```bash
python build_v4.1.py
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Dialer Directly
```bash
python dialer_gui.py
```

### Run Bulk Processor Directly
```bash
python bulk_processor_gui.py
```

---

## Common Patterns

### Error Handling
- Try-except blocks for file operations
- API error handling with status codes
- Graceful degradation when cache fails
- Thread-safe UI updates

### Threading
- Background workers for API calls
- Non-blocking UI with daemon threads
- UI updates via root.after()

### Caching
- Check cache before API call
- Store only if has results
- Update cache on manual calls
- Preserve existing data when accumulating

### UI Updates
- Fixed heights for sections (grid_propagate(False))
- Scrollable addresses (max 150px)
- Color-coded status messages
- Flashing status dropdown after calls

---

This code map provides a complete overview of the Passion Of Rugs Advanced Dialer v4.1 codebase.
