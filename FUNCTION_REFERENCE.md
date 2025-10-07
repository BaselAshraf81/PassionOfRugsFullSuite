# Passion Of Rugs Advanced Dialer v4.1 - Complete Function Reference

## Overview
This document provides a complete reference of all functions in the application, organized by file and purpose.

---

## launcher.py (145 lines)
**Purpose:** Application entry point - Mode selector

### LauncherGUI Class

#### `__init__(self, root)`
- **Location:** Line ~15
- **Purpose:** Initialize launcher window
- **Parameters:** root (Tk window)
- **Actions:** Sets up window, colors, centers window, creates UI

#### `center_window(self)`
- **Location:** Line ~30
- **Purpose:** Center window on screen
- **Actions:** Calculates screen center and positions window

#### `create_ui(self)`
- **Location:** Line ~40
- **Purpose:** Create launcher UI with mode selection
- **Actions:** Creates title, mode buttons, version info

#### `start_mode1(self)`
- **Location:** Line ~120
- **Purpose:** Launch Bulk Processing Mode
- **Actions:** Destroys launcher, imports and runs bulk_processor_gui

#### `start_mode2(self)`
- **Location:** Line ~125
- **Purpose:** Launch Professional Dialer Mode
- **Actions:** Destroys launcher, imports and runs dialer_gui

#### `main()`
- **Location:** Line ~130
- **Purpose:** Main entry point
- **Actions:** Creates Tk root, initializes LauncherGUI, starts mainloop

---

## dialer_gui.py (~4280 lines)
**Purpose:** Professional Dialer Mode - Main application

### CloudTalkAPI Class (Lines 24-68)

#### `__init__(self, access_key_id, access_key_secret)`
- **Location:** Line ~25
- **Purpose:** Initialize CloudTalk API client
- **Parameters:** access_key_id, access_key_secret
- **Actions:** Sets up base URL, creates auth headers with Basic auth

#### `make_call(self, agent_id, callee_number)`
- **Location:** Line ~35
- **Purpose:** Initiate call via CloudTalk API
- **Parameters:** agent_id, callee_number
- **Returns:** Dict with success status and message
- **Actions:** Formats phone number, makes POST request, handles response codes

### ExcelCache Class (Lines 70-119)

#### `__init__(self, output_file)`
- **Location:** Line ~71
- **Purpose:** Initialize Excel cache manager
- **Parameters:** output_file path
- **Actions:** Sets output file, initializes cache dict, loads existing data

#### `load_cache(self)`
- **Location:** Line ~77
- **Purpose:** Load cached data from output Excel file
- **Actions:** Reads Excel, parses rows, stores in cache dict by phone number

#### `get(self, original_phone)`
- **Location:** Line ~110
- **Purpose:** Retrieve cached data for a phone number
- **Parameters:** original_phone
- **Returns:** Dict with cached data or None

#### `update(self, original_phone, data)`
- **Location:** Line ~115
- **Purpose:** Update cache with new data
- **Parameters:** original_phone, data dict
- **Actions:** Stores data in cache dict

### DialerGUI Class (Lines 122-4280)

#### Setup & Initialization

##### `__init__(self, root)`
- **Location:** Line ~123
- **Purpose:** Initialize dialer application
- **Parameters:** root (Tk window)
- **Actions:** Sets up window, initializes data structures, loads settings, shows setup screen

##### `load_call_history(self)`
- **Location:** Line ~203
- **Purpose:** Load call history from JSON file
- **Actions:** Reads call_history.json, parses JSON, stores in list

##### `save_call_history(self)`
- **Location:** Line ~213
- **Purpose:** Save call history to JSON file
- **Actions:** Writes call_history list to JSON file

##### `add_to_call_history(self, phone, name, status, notes="")`
- **Location:** Line ~220
- **Purpose:** Add or update call history entry (one per phone)
- **Parameters:** phone, name, status, notes
- **Actions:** Checks for existing entry, updates or creates new, saves to file

##### `show_setup_screen(self)`
- **Location:** Line ~245
- **Purpose:** Display setup configuration screen
- **Actions:** Creates scrollable form with API keys, file selection, settings

##### `use_default_cloudtalk_config(self)`
- **Location:** Line ~420
- **Purpose:** Load CloudTalk config from config.py
- **Actions:** Imports config values, fills form fields

##### `use_default_openai_config(self)`
- **Location:** Line ~435
- **Purpose:** Load OpenAI API key from config.py
- **Actions:** Imports OPENAI_API_KEY, fills form field

##### `test_ai_connection(self)`
- **Location:** Line ~448
- **Purpose:** Test OpenAI API connection
- **Actions:** Creates AIAssistant, calls test_connection(), shows result

#### Settings Management

##### `show_settings_window(self)`
- **Location:** Line ~465
- **Purpose:** Display settings configuration window
- **Actions:** Creates window with checkboxes for auto API settings and AI features

##### `save_settings(self, window)`
- **Location:** Line ~540
- **Purpose:** Save settings from settings window
- **Parameters:** window to close
- **Actions:** Updates settings dict, saves to JSON file, closes window

##### `load_settings(self)`
- **Location:** Line ~555
- **Purpose:** Load settings from JSON file
- **Actions:** Reads dialer_settings.json, updates settings dict

#### File Management

##### `browse_input_file(self)`
- **Location:** Line ~565
- **Purpose:** Browse for input Excel file
- **Actions:** Opens file dialog, stores selected file path, updates label

##### `start_dialer(self, setup_container)`
- **Location:** Line ~575
- **Purpose:** Initialize and start dialer after setup
- **Parameters:** setup_container to destroy
- **Actions:** Validates inputs, initializes APIs, loads data, shows dialer screen

#### Main Dialer Screen

##### `show_dialer_screen(self)`
- **Location:** Line ~645
- **Purpose:** Display main dialer interface
- **Actions:** Creates complete UI with navigation, results display, controls

##### `update_status(self, message, color=None)`
- **Location:** Line ~1100
- **Purpose:** Update status bar message
- **Parameters:** message text, optional color
- **Actions:** Updates status label text and color

#### Data Loading & Processing

##### `load_person(self, index)`
- **Location:** Line ~1309
- **Purpose:** Load person data at given index
- **Parameters:** index in original_data
- **Actions:** Checks cache, loads from cache or performs API lookups, displays results

##### `perform_lookups(self, row, force_refresh=False)`
- **Location:** Line ~1391
- **Purpose:** Perform API lookups based on auto settings
- **Parameters:** row data, force_refresh flag
- **Returns:** Tuple of (phone_data, address_data, ai_analysis)
- **Actions:** Calls APIs if auto settings enabled, stores in cache, returns results

##### `process_lookup_data(self, phone_data, address_data, ai_analysis=None)`
- **Location:** Line ~1543
- **Purpose:** Process raw API responses into structured results
- **Parameters:** phone_data, address_data, optional ai_analysis
- **Returns:** List of result dicts
- **Actions:** Extracts people/phones/addresses recursively, creates result dicts

##### `extract_people_from_data(self, phone_data, address_data, original_phone, original_address, original_name)`
- **Location:** Line ~1620
- **Purpose:** Recursively extract all people, phones, and addresses from API responses
- **Parameters:** API data, original data
- **Returns:** List of person dicts with phones and addresses
- **Actions:** Traverses nested structures, deduplicates, combines data

#### Manual API Calls

##### `manual_phone_lookup(self)`
- **Location:** Line ~2377
- **Purpose:** Manual phone lookup button handler
- **Actions:** Always calls API (bypasses cache), accumulates with existing data

##### `manual_address_lookup(self)`
- **Location:** Line ~2420
- **Purpose:** Manual address lookup button handler
- **Actions:** Always calls API (bypasses cache), accumulates with existing data

##### `accumulate_phone_results(self, new_phone_data)`
- **Location:** Line ~2470
- **Purpose:** Add phone lookup data to existing results
- **Parameters:** new_phone_data from API
- **Actions:** Merges with cached data, extracts people, updates cache and display

##### `accumulate_address_results(self, new_address_data)`
- **Location:** Line ~2520
- **Purpose:** Add address lookup data to existing results
- **Parameters:** new_address_data from API
- **Actions:** Merges with cached data, extracts people, updates cache and display

#### Navigation

##### `next_person(self)`
- **Location:** Line ~1720
- **Purpose:** Navigate to next person
- **Actions:** Saves pending call history, increments index, loads next person

##### `prev_person(self)`
- **Location:** Line ~1740
- **Purpose:** Navigate to previous person
- **Actions:** Saves pending call history, decrements index, loads previous person

##### `next_result(self)`
- **Location:** Line ~1760
- **Purpose:** Navigate to next result for current person
- **Actions:** Increments result index, displays result

##### `prev_result(self)`
- **Location:** Line ~1780
- **Purpose:** Navigate to previous result for current person
- **Actions:** Decrements result index, displays result

##### `next_phone(self)`
- **Location:** Line ~1800
- **Purpose:** Navigate to next phone number for current result
- **Actions:** Increments phone index, displays phone

##### `prev_phone(self)`
- **Location:** Line ~1820
- **Purpose:** Navigate to previous phone number for current result
- **Actions:** Decrements phone index, displays phone

#### Display Functions

##### `display_current_result(self)`
- **Location:** Line ~1840
- **Purpose:** Display current result in UI
- **Actions:** Updates all labels, buttons, and fields with current result data

##### `display_ai_results(self, ai_analysis)`
- **Location:** Line ~2100
- **Purpose:** Display AI analysis in AI Overview tab
- **Parameters:** ai_analysis dict from AI assistant
- **Actions:** Formats and displays filtered results, insights, recommendations

##### `show_full_response(self)`
- **Location:** Line ~2313
- **Purpose:** Show full API response viewer window
- **Actions:** Creates window with tabs for phone/address responses, visual view

##### `generate_visual_html(self, phone_data, address_data)`
- **Location:** Line ~2400
- **Purpose:** Generate HTML for visual response view
- **Parameters:** phone_data, address_data
- **Returns:** HTML string
- **Actions:** Creates formatted HTML with sections for all data

#### Call Management

##### `make_call(self)`
- **Location:** Line ~2570
- **Purpose:** Initiate CloudTalk call
- **Actions:** Validates phone, starts call worker thread, tracks call info

##### `call_worker(self, phone, name)`
- **Location:** Line ~2600
- **Purpose:** Background worker for making calls
- **Parameters:** phone, name
- **Actions:** Calls CloudTalk API, updates UI, flashes status dropdown

##### `flash_status_dropdown(self)`
- **Location:** Line ~2650
- **Purpose:** Flash status dropdown after call
- **Actions:** Changes background color 3 times to draw attention

##### `save_pending_call_history(self)`
- **Location:** Line ~2680
- **Purpose:** Save pending call history when navigating
- **Actions:** Checks for tracked call, gets status/notes, adds to history

#### Data Persistence

##### `save_results_to_excel(self)`
- **Location:** Line ~2700
- **Purpose:** Save current results to Excel (prevents duplicates)
- **Actions:** Checks for existing rows, updates or appends, saves Excel

##### `update_data_in_excel(self, original_phone, status, notes)`
- **Location:** Line ~2850
- **Purpose:** Update status/notes in Excel for a phone number
- **Parameters:** original_phone, status, notes
- **Actions:** Finds row in Excel, updates fields, saves file

##### `on_status_change(self, event)`
- **Location:** Line ~2900
- **Purpose:** Handle status dropdown change
- **Parameters:** event
- **Actions:** Gets selected status, updates Excel

##### `on_notes_change(self, event)`
- **Location:** Line ~2920
- **Purpose:** Handle notes text change
- **Parameters:** event
- **Actions:** Gets notes text, updates Excel

#### Cache Management

##### `show_cache_stats(self)`
- **Location:** Line ~2940
- **Purpose:** Display cache statistics window
- **Actions:** Gets stats from cache_manager, shows in message box

##### `clear_cache_confirm(self)`
- **Location:** Line ~2960
- **Purpose:** Clear cache with confirmation
- **Actions:** Shows confirmation dialog, clears cache if confirmed

#### Utility Functions

##### `copy_to_clipboard(self, text)`
- **Location:** Line ~2980
- **Purpose:** Copy text to clipboard
- **Parameters:** text to copy
- **Actions:** Clears clipboard, appends text, updates status

##### `open_google_maps(self, address)`
- **Location:** Line ~2995
- **Purpose:** Open address in Google Maps
- **Parameters:** address string
- **Actions:** URL encodes address, opens in browser

##### `open_in_browser(self, url)`
- **Location:** Line ~3010
- **Purpose:** Open URL in default browser
- **Parameters:** url
- **Actions:** Uses webbrowser module to open URL

---

## bulk_processor_gui.py (348 lines)
**Purpose:** Bulk Processing Mode

### BulkProcessorGUI Class

#### `__init__(self, root)`
- **Location:** Line ~15
- **Purpose:** Initialize bulk processor window
- **Parameters:** root (Tk window)
- **Actions:** Sets up window, initializes data, creates UI

#### `create_ui(self)`
- **Location:** Line ~40
- **Purpose:** Create bulk processor UI
- **Actions:** Creates configuration form, progress section, buttons

#### `browse_input(self)`
- **Location:** Line ~217
- **Purpose:** Browse for input Excel file
- **Actions:** Opens file dialog, stores path, updates label

#### `log(self, message)`
- **Location:** Line ~227
- **Purpose:** Add message to result text area
- **Parameters:** message string
- **Actions:** Inserts text, scrolls to end, updates UI

#### `update_progress(self, current, total)`
- **Location:** Line ~235
- **Purpose:** Update progress bar
- **Parameters:** current row, total rows
- **Actions:** Calculates percentage, updates progress bar and label

#### `update_status(self, message)`
- **Location:** Line ~245
- **Purpose:** Update status label
- **Parameters:** message string
- **Actions:** Updates status label text

#### `start_processing(self)`
- **Location:** Line ~253
- **Purpose:** Start processing in background thread
- **Actions:** Validates inputs, disables buttons, starts worker thread

#### `process_worker(self)`
- **Location:** Line ~300
- **Purpose:** Background worker for processing
- **Actions:** Creates LeadProcessor, processes Excel, updates UI

#### `stop_processing(self)`
- **Location:** Line ~337
- **Purpose:** Stop processing
- **Actions:** Sets processing flag to False, logs message

#### `main()`
- **Location:** Line ~343
- **Purpose:** Main entry point for bulk processor
- **Actions:** Creates Tk root, initializes BulkProcessorGUI, starts mainloop

---

## lead_processor_v2.py (877 lines)
**Purpose:** Core API processing logic

### LeadProcessor Class

#### `__init__(self, api_key, use_cache=True, ai_assistant=None)`
- **Location:** Line ~20
- **Purpose:** Initialize lead processor
- **Parameters:** api_key, use_cache flag, optional ai_assistant
- **Actions:** Sets up API client, cache manager, AI assistant

#### `parse_address(self, address_str)`
- **Location:** Line ~36
- **Purpose:** Parse full address string into components
- **Parameters:** address_str
- **Returns:** Dict with street, city, state, zip
- **Actions:** Uses regex to extract ZIP, state, city, street from various formats

#### `clean_phone(self, phone)`
- **Location:** Line ~250
- **Purpose:** Clean and format phone number to E.164
- **Parameters:** phone (string or number)
- **Returns:** Formatted phone string
- **Actions:** Removes non-digits, adds country code, formats to +1XXXXXXXXXX

#### `phone_lookup(self, phone)`
- **Location:** Line ~270
- **Purpose:** Perform reverse phone lookup via TrestleIQ API
- **Parameters:** phone number
- **Returns:** API response dict
- **Actions:** Makes GET request to /3.2/phone endpoint

#### `address_lookup(self, street, city, state, zip_code, enable_ai_correction=True, status_callback=None)`
- **Location:** Line ~285
- **Purpose:** Perform reverse address lookup with optional AI correction
- **Parameters:** address components, ai_correction flag, status_callback
- **Returns:** Tuple of (api_response, correction_info)
- **Actions:** Makes API call, retries with AI correction if fails, max 2 attempts

#### `extract_age(self, person_data)`
- **Location:** Line ~360
- **Purpose:** Extract age or age_range from person data
- **Parameters:** person_data dict
- **Returns:** Age string
- **Actions:** Checks for 'age' or 'age_range' keys

#### `get_last_name(self, full_name)`
- **Location:** Line ~370
- **Purpose:** Extract last name from full name
- **Parameters:** full_name string
- **Returns:** Last name in uppercase
- **Actions:** Splits on spaces, returns last part

#### `format_address(self, address_data)`
- **Location:** Line ~380
- **Purpose:** Format address from address data dict
- **Parameters:** address_data dict
- **Returns:** Formatted address string
- **Actions:** Joins street, city, state, ZIP with commas

#### `process_row(self, row, cached_data=None, force_refresh=False)`
- **Location:** Line ~395
- **Purpose:** Process a single row of data
- **Parameters:** row (Series), optional cached_data, force_refresh flag
- **Returns:** Tuple of (results list, address_lookup_failed flag)
- **Actions:** Checks cache, makes API calls, extracts people, creates result dicts

#### `process_excel_file_bulk(self, input_file, output_file, max_rows=None, progress_callback=None, status_callback=None)`
- **Location:** Line ~612
- **Purpose:** Bulk process Excel file (MODE 1)
- **Parameters:** input/output files, max_rows, callbacks
- **Returns:** Tuple of (total_results, cached_count, api_count)
- **Actions:** Reads Excel, processes rows with caching, creates formatted output

#### `_load_cache_from_excel(self, output_file)`
- **Location:** Line ~680
- **Purpose:** Load cache from existing output Excel
- **Parameters:** output_file path
- **Returns:** Dict of cached data by phone
- **Actions:** Reads Excel, parses rows, stores in dict

#### `create_excel_output(self, results, output_file, rows_with_address_errors)`
- **Location:** Line ~720
- **Purpose:** Create formatted Excel output file
- **Parameters:** results list, output_file path, error row indices
- **Actions:** Creates workbook, formats cells, adds dropdowns, colors rows

---

## cache_manager.py (283 lines)
**Purpose:** Permanent cache management

### CacheManager Class

#### `__init__(self, cache_file="lead_processor_cache.json")`
- **Location:** Line ~20
- **Purpose:** Initialize cache manager
- **Parameters:** cache_file path
- **Actions:** Sets up cache structure, loads from disk

#### `_get_timestamp(self)`
- **Location:** Line ~35
- **Purpose:** Get current timestamp in ISO format
- **Returns:** ISO timestamp string
- **Actions:** Uses datetime.utcnow()

#### `normalize_phone(self, phone)`
- **Location:** Line ~40
- **Purpose:** Normalize phone number to E.164 format
- **Parameters:** phone string
- **Returns:** Normalized phone string (+1XXXXXXXXXX)
- **Actions:** Removes non-digits, adds country code

#### `load_cache(self)`
- **Location:** Line ~62
- **Purpose:** Load cache from disk
- **Returns:** True if successful
- **Actions:** Reads JSON file, validates structure, loads into memory

#### `save_cache(self)`
- **Location:** Line ~90
- **Purpose:** Save cache to disk with atomic write
- **Returns:** True if successful
- **Actions:** Writes to temp file, renames to actual file (atomic)

#### `get_cached_lookup(self, phone)`
- **Location:** Line ~122
- **Purpose:** Get cached API responses for a phone number
- **Parameters:** phone string
- **Returns:** Tuple of (phone_data, address_data, ai_analysis) or None
- **Actions:** Normalizes phone, checks cache, returns data if found

#### `store_lookup(self, phone, reverse_phone_response, reverse_address_response, ai_analysis=None)`
- **Location:** Line ~145
- **Purpose:** Store API lookup results in cache
- **Parameters:** phone, API responses, optional ai_analysis
- **Returns:** True if stored successfully
- **Actions:** Normalizes phone, creates cache entry, saves to disk

#### `update_ai_analysis(self, phone, ai_analysis)`
- **Location:** Line ~180
- **Purpose:** Update AI analysis for existing cache entry
- **Parameters:** phone, ai_analysis dict
- **Returns:** True if updated successfully
- **Actions:** Finds entry, updates AI analysis, saves to disk

#### `clear_cache(self)`
- **Location:** Line ~199
- **Purpose:** Clear all cached entries
- **Returns:** Tuple of (entries_cleared, success)
- **Actions:** Empties lookups dict, saves to disk

#### `get_statistics(self)`
- **Location:** Line ~215
- **Purpose:** Get cache statistics
- **Returns:** Dict with statistics
- **Actions:** Calculates entries, file size, costs saved, hit rate

#### `get_cache_info_string(self)`
- **Location:** Line ~252
- **Purpose:** Get formatted cache information string
- **Returns:** Formatted string
- **Actions:** Calls get_statistics(), formats as readable text

---

## ai_assistant.py (~200 lines)
**Purpose:** AI-powered address correction and person filtering

### AIAssistant Class

#### `__init__(self, api_key=None, model="gpt-4o-mini")`
- **Location:** Line ~20
- **Purpose:** Initialize AI assistant
- **Parameters:** optional api_key, model name
- **Actions:** Sets up OpenAI client, checks if enabled

#### `test_connection(self)`
- **Location:** Line ~35
- **Purpose:** Test OpenAI API connection
- **Returns:** Tuple of (success bool, message)
- **Actions:** Makes test API call with minimal tokens

#### `correct_address(self, street_line_1, street_line_2, city, state_code, postal_code)`
- **Location:** Line ~50
- **Purpose:** Correct malformed address using AI
- **Parameters:** address components
- **Returns:** Dict with corrected address and reasoning, or None
- **Actions:** Sends prompt to GPT, parses JSON response, returns corrected address

#### `filter_and_rank_contacts(self, original_name, original_phone, original_address, reverse_phone_response, reverse_address_response)`
- **Location:** Line ~120
- **Purpose:** Intelligently filter and rank contacts
- **Parameters:** original data, API responses
- **Returns:** Dict with horizontal ranking and insights, or None
- **Actions:** Sends comprehensive prompt to GPT, parses structured response

---

## config.py (28 lines)
**Purpose:** Configuration file (optional)

### Configuration Variables

#### `API_KEY`
- **Location:** Line ~4
- **Purpose:** TrestleIQ API key
- **Type:** String

#### `BASE_URL`
- **Location:** Line ~5
- **Purpose:** TrestleIQ API base URL
- **Type:** String
- **Default:** "https://api.trestleiq.com"

#### `CLOUDTALK_ACCESS_KEY_ID`
- **Location:** Line ~8
- **Purpose:** CloudTalk access key ID
- **Type:** String

#### `CLOUDTALK_ACCESS_KEY_SECRET`
- **Location:** Line ~9
- **Purpose:** CloudTalk access key secret
- **Type:** String

#### `CLOUDTALK_AGENT_ID`
- **Location:** Line ~10
- **Purpose:** CloudTalk agent ID
- **Type:** String

#### `OPENAI_API_KEY`
- **Location:** Line ~13
- **Purpose:** OpenAI API key for AI features
- **Type:** String

#### `INPUT_FILE`
- **Location:** Line ~16
- **Purpose:** Default input Excel file path
- **Type:** String

#### `OUTPUT_FILE`
- **Location:** Line ~17
- **Purpose:** Default output file path
- **Type:** String

#### `ACTIVITY_SCORE_THRESHOLD`
- **Location:** Line ~20
- **Purpose:** Activity score threshold for filtering
- **Type:** Integer
- **Default:** 30

#### `RATE_LIMIT_DELAY`
- **Location:** Line ~21
- **Purpose:** Delay between API calls (seconds)
- **Type:** Float
- **Default:** 0.1

#### `COLUMN_MAPPING`
- **Location:** Line ~24
- **Purpose:** Excel column name mappings
- **Type:** Dict

---

## build_v4.1.py (~90 lines)
**Purpose:** PyInstaller build script

### Build Functions

#### `build_executable()`
- **Location:** Line ~10
- **Purpose:** Build executable using PyInstaller
- **Actions:** Configures PyInstaller args, runs build, displays results

---

## Summary Statistics

### Total Functions by File
- **launcher.py:** 6 functions
- **dialer_gui.py:** 60+ functions (main application)
- **bulk_processor_gui.py:** 10 functions
- **lead_processor_v2.py:** 15 functions
- **cache_manager.py:** 12 functions
- **ai_assistant.py:** 4 functions
- **config.py:** 10 configuration variables
- **build_v4.1.py:** 1 function

### Total Lines of Code
- **launcher.py:** 145 lines
- **dialer_gui.py:** ~4280 lines
- **bulk_processor_gui.py:** 348 lines
- **lead_processor_v2.py:** 877 lines
- **cache_manager.py:** 283 lines
- **ai_assistant.py:** ~200 lines
- **config.py:** 28 lines
- **build_v4.1.py:** ~90 lines

**Total:** ~6,251 lines of Python code

---

## Key Function Categories

### API Integration
- `CloudTalkAPI.make_call()` - CloudTalk calling
- `LeadProcessor.phone_lookup()` - TrestleIQ phone API
- `LeadProcessor.address_lookup()` - TrestleIQ address API
- `AIAssistant.correct_address()` - OpenAI address correction
- `AIAssistant.filter_and_rank_contacts()` - OpenAI person filtering

### Data Processing
- `LeadProcessor.parse_address()` - Address parsing
- `LeadProcessor.clean_phone()` - Phone formatting
- `LeadProcessor.process_row()` - Row processing
- `DialerGUI.extract_people_from_data()` - Data extraction
- `DialerGUI.process_lookup_data()` - Response processing

### Caching
- `CacheManager.get_cached_lookup()` - Cache retrieval
- `CacheManager.store_lookup()` - Cache storage
- `CacheManager.normalize_phone()` - Phone normalization
- `ExcelCache.load_cache()` - Excel cache loading
- `ExcelCache.get()` - Excel cache retrieval

### UI Management
- `DialerGUI.show_setup_screen()` - Setup UI
- `DialerGUI.show_dialer_screen()` - Main UI
- `DialerGUI.display_current_result()` - Result display
- `DialerGUI.display_ai_results()` - AI results display
- `DialerGUI.update_status()` - Status updates

### Navigation
- `DialerGUI.next_person()` - Next person
- `DialerGUI.prev_person()` - Previous person
- `DialerGUI.next_result()` - Next result
- `DialerGUI.prev_result()` - Previous result
- `DialerGUI.next_phone()` - Next phone
- `DialerGUI.prev_phone()` - Previous phone

### Data Persistence
- `DialerGUI.save_results_to_excel()` - Save to Excel
- `DialerGUI.update_data_in_excel()` - Update Excel
- `DialerGUI.save_call_history()` - Save call history
- `LeadProcessor.create_excel_output()` - Create Excel output
- `CacheManager.save_cache()` - Save cache

---

**Version:** 4.1  
**Last Updated:** 2025-10-07  
**Total Functions:** 100+  
**Total Lines:** ~6,251  
