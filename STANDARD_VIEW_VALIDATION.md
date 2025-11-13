# Standard View Results Validation

## What Was Added

Added validation to ensure **Standard View results** (phone numbers, addresses, names) always match the person currently being displayed.

## The Problem

Previously, `display_current_result()` would display whatever was in `self.current_results` without checking if those results belonged to the current person. This could cause:

- Person A's phone numbers showing when viewing Person B
- Wrong addresses displayed
- Mismatched data after rapid navigation

## The Solution

### Validation in `display_current_result()`

Added validation that checks if `current_results` match the current person **before displaying**:

```python
def display_current_result(self):
    """Display current result - validates we're showing data for current person"""
    # Validate we have a valid person index
    if self.current_person_idx < 0 or self.current_person_idx >= len(self.original_data):
        logger.warning(f"Invalid person index: {self.current_person_idx}")
        return
    
    # CRITICAL: Validate current_results match current person
    if self.current_results:
        current_person = self.original_data[self.current_person_idx]
        current_phone = self.lead_processor.clean_phone(current_person.get('phone', ''))
        current_name = current_person.get('name', '')
        
        # Check if results match current person (using first result as reference)
        result_phone = self.current_results[0].get('original_phone', '')
        result_name = self.current_results[0].get('original_name', '')
        
        if result_phone != current_phone:
            logger.warning(f"Standard View results phone mismatch")
            logger.warning(f"Clearing mismatched results")
            # Clear mismatched results
            self.current_results = []
            self.current_result_idx = 0
            self.current_phone_idx = 0
        else:
            logger.debug(f"Standard View results validated")
    
    if not self.current_results:
        # Show "No results found" UI
        ...
```

## How It Works

### 1. Check Original Phone Number

Every result in `current_results` has:
- `original_phone` - the phone number this result was created for
- `original_name` - the name this result was created for

When displaying, we compare:
```python
result_phone = self.current_results[0].get('original_phone', '')
current_phone = self.lead_processor.clean_phone(current_person.get('phone', ''))

if result_phone != current_phone:
    # MISMATCH - clear results
    self.current_results = []
```

### 2. Clear Mismatched Results

If results don't match, they're cleared immediately:
- `self.current_results = []`
- `self.current_result_idx = 0`
- `self.current_phone_idx = 0`

This causes the UI to show "No results found" instead of wrong data.

### 3. Log for Debugging

All validation is logged:
- **Warning** when mismatch detected
- **Debug** when validation passes

## Multi-Layer Protection

### Layer 1: Creation
Results are created with correct `original_phone` and `original_name`:
```python
results = self.process_lookup_data(person, phone_data, address_data)
# Each result has original_phone and original_name set
```

### Layer 2: Accumulation
Accumulate functions validate before modifying results:
```python
def accumulate_phone_results(self, phone_data, original_person, trigger_ai=True):
    # Validate we're still on the same person
    current_person = self.original_data[self.current_person_idx]
    current_phone = self.lead_processor.clean_phone(current_person.get('phone', ''))
    original_phone = self.lead_processor.clean_phone(original_person.get('phone', ''))
    
    if current_phone != original_phone:
        logger.warning(f"Phone mismatch - aborting accumulate")
        return
```

### Layer 3: Display
Final validation before showing to user:
```python
def display_current_result(self):
    # Validate results match current person
    if result_phone != current_phone:
        # Clear and show "No results"
```

## What This Prevents

### Scenario 1: Rapid Navigation
```
User on Person 1 → API call starts
User clicks Next → Now on Person 2
API returns results for Person 1
Without validation: Shows Person 1 data on Person 2 screen ❌
With validation: Clears mismatched data, shows "No results" ✅
```

### Scenario 2: Background Operations
```
User on Person A → Background thread processing
User navigates to Person B
Background thread completes for Person A
Without validation: Updates current_results with Person A data ❌
With validation: Detects mismatch, clears results ✅
```

### Scenario 3: Cache Issues
```
User on Person 1 → Results cached
User on Person 2 → Accidentally loads Person 1's cached results
Without validation: Shows Person 1 data ❌
With validation: Detects mismatch, clears results ✅
```

## Testing

### Test 1: Rapid Navigation
1. Load Person 1
2. Immediately click Next 5 times
3. **Expected:** Each person shows their own data or "No results"
4. **Not Expected:** Person 1's data showing on Person 5

### Test 2: Background Completion
1. Load Person A (API starts)
2. Click Next to Person B before API completes
3. Wait for API to complete
4. **Expected:** Person B shows "No results" or Person B's data
5. **Not Expected:** Person A's data showing on Person B

### Test 3: Manual Lookups
1. Load Person 1
2. Click "Phone" button (manual lookup)
3. Immediately click Next to Person 2
4. **Expected:** Person 2 shows their data
5. **Not Expected:** Person 1's lookup results showing on Person 2

## Logging

All validation events are logged:

```
DEBUG: Standard View results validated for person 5 (John Doe, +1234567890)
WARNING: Standard View results phone mismatch: result=+1111111111, current=+1234567890
WARNING: Clearing mismatched results for person 5 (John Doe)
```

## Summary

**Before:**
- ❌ Standard View could show wrong person's data
- ❌ No validation of results vs current person
- ❌ Race conditions during navigation

**After:**
- ✅ Standard View always shows correct person's data
- ✅ Validation on every display
- ✅ Mismatched results cleared immediately
- ✅ Comprehensive logging for debugging

The Standard View now has the same level of protection as the AI tab - both validate that displayed data matches the current person using phone number as the identifier.
