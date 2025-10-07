# Data Validation Quick Reference

## Critical Validations Added

### 1. Background AI Analysis
```python
_update_ai_results(ai_results, original_phone, person_idx)
├── Check: person_idx == current_person_idx
├── Check: original_phone == current_person_phone
└── Only update UI if both match
```

### 2. Display Functions
```python
display_current_result()
├── Check: valid person_idx
├── Check: valid result_idx
└── Only display if valid

show_ai_tab()
├── Check: ai_results exists
├── Check: ai_results.original_phone == current_person_phone
└── Only display if match
```

### 3. Accumulate Functions
```python
accumulate_phone_results(phone_data, original_person)
├── Check: valid person_idx
├── Check: original_person.phone == current_person.phone
└── Only accumulate if match

accumulate_address_results(address_data, original_person)
├── Check: valid person_idx
├── Check: original_person.phone == current_person.phone
└── Only accumulate if match
```

## Cache Flow

```
API Call Request
    ↓
Check Permanent Cache
    ↓
Found? → Use cached data → Validate person → Display
    ↓
Not Found? → Call API → Store in cache → Validate person → Display
```

## Preloading Flow

```
Load Person N
    ↓
Start preloading Person N+1 in background
    ↓
Check cache for Person N+1
    ↓
Found? → Store in memory
Not Found? → Call API → Store in cache → Store in memory
    ↓
User navigates to Person N+1
    ↓
Check memory for preloaded data
    ↓
Found? → Validate phone number → Use if match
Not Found? → Load normally
```

## Validation Checklist

✅ Person index validation
✅ Phone number matching
✅ Result index validation
✅ AI results validation
✅ Cache validation
✅ Preload validation

## Key Functions Modified

1. `_run_ai_analysis_background()` - Added person_idx
2. `_update_ai_results()` - Added validation
3. `display_current_result()` - Added validation
4. `show_ai_tab()` - Added validation
5. `accumulate_phone_results()` - Added validation
6. `accumulate_address_results()` - Added validation
7. `process_ai_analysis()` - Added metadata

## Testing Scenarios

| Scenario | Expected | Status |
|----------|----------|--------|
| Quick navigation | Correct data | ✅ |
| Back navigation | Instant load | ✅ |
| Manual lookup during nav | No mix-up | ✅ |
| Preloading | Instant load | ✅ |
| AI analysis | Correct person | ✅ |

## Error Prevention

- Wrong person data: **PREVENTED** ✅
- Race conditions: **PREVENTED** ✅
- Cache mismatches: **PREVENTED** ✅
- Display errors: **PREVENTED** ✅
