# AI Features Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                  Passion Of Rugs Advanced Dialer v4.1           │
│                     with AI Features                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │         User Interface (dialer_gui.py)  │
        │  ┌───────────────────────────────────┐  │
        │  │  Setup Screen                     │  │
        │  │  - OpenAI API Key Input           │  │
        │  │  - Test Connection Button         │  │
        │  └───────────────────────────────────┘  │
        │  ┌───────────────────────────────────┐  │
        │  │  Dialer Screen                    │  │
        │  │  ┌─────────────────────────────┐  │  │
        │  │  │ Results Notebook (Tabs)     │  │  │
        │  │  │ ┌─────────┬───────────────┐ │  │  │
        │  │  │ │Standard │ AI Overview & │ │  │  │
        │  │  │ │  View   │   Filtering   │ │  │  │
        │  │  │ └─────────┴───────────────┘ │  │  │
        │  │  └─────────────────────────────┘  │  │
        │  │  ┌─────────────────────────────┐  │  │
        │  │  │ Settings Window             │  │  │
        │  │  │ - AI Address Correction ☑   │  │  │
        │  │  │ - AI Person Filtering ☑     │  │  │
        │  │  └─────────────────────────────┘  │  │
        │  └───────────────────────────────────┘  │
        └─────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │   Core Processing (lead_processor_v2.py)│
        │  ┌───────────────────────────────────┐  │
        │  │  phone_lookup()                   │  │
        │  │  - TrestleIQ Reverse Phone API    │  │
        │  └───────────────────────────────────┘  │
        │  ┌───────────────────────────────────┐  │
        │  │  address_lookup()                 │  │
        │  │  - TrestleIQ Reverse Address API  │  │
        │  │  - AI Correction Integration      │  │
        │  └───────────────────────────────────┘  │
        └─────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │      AI Assistant (ai_assistant.py)     │
        │  ┌───────────────────────────────────┐  │
        │  │  correct_address()                │  │
        │  │  - Analyzes failed address        │  │
        │  │  - Returns corrected components   │  │
        │  │  - Provides reasoning             │  │
        │  └───────────────────────────────────┘  │
        │  ┌───────────────────────────────────┐  │
        │  │  filter_and_rank_contacts()       │  │
        │  │  - Analyzes API responses         │  │
        │  │  - Identifies original customer   │  │
        │  │  - Ranks by confidence            │  │
        │  │  - Generates insights             │  │
        │  └───────────────────────────────────┘  │
        └─────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │         OpenAI GPT-4o-mini API          │
        │  - Address correction prompts           │
        │  - Person filtering prompts             │
        │  - JSON structured responses            │
        └─────────────────────────────────────────┘
```

## Data Flow: Address Correction

```
┌──────────────────────────────────────────────────────────────────┐
│ 1. User loads person with address                               │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│ 2. lead_processor.address_lookup() called                       │
│    - Parse address components                                   │
│    - Call TrestleIQ API                                         │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ API Response    │
                    └─────────────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
        ┌───────────────┐         ┌────────────────┐
        │ Success       │         │ Failure        │
        │ (has results) │         │ (no results)   │
        └───────────────┘         └────────────────┘
                │                           │
                │                           ▼
                │               ┌────────────────────────────┐
                │               │ 3. AI Correction Triggered │
                │               │    (if enabled)            │
                │               └────────────────────────────┘
                │                           │
                │                           ▼
                │               ┌────────────────────────────┐
                │               │ 4. ai_assistant.           │
                │               │    correct_address()       │
                │               │    - Analyze address       │
                │               │    - Fix common issues     │
                │               │    - Return corrected      │
                │               └────────────────────────────┘
                │                           │
                │                           ▼
                │               ┌────────────────────────────┐
                │               │ 5. Retry API Call          │
                │               │    with corrected address  │
                │               └────────────────────────────┘
                │                           │
                │                           ▼
                │                   ┌───────────────┐
                │                   │ Success?      │
                │                   └───────────────┘
                │                           │
                │                   ┌───────┴────────┐
                │                   │                │
                │                   ▼                ▼
                │           ┌──────────┐     ┌──────────────┐
                │           │ Yes      │     │ No           │
                │           │ Log      │     │ Try again    │
                │           │ success  │     │ (max 2)      │
                │           └──────────┘     └──────────────┘
                │                   │                │
                └───────────────────┴────────────────┘
                                    │
                                    ▼
                        ┌───────────────────────┐
                        │ 6. Display Results    │
                        │    - Standard View    │
                        │    - AI Tab (if used) │
                        └───────────────────────┘
```

## Data Flow: Person Filtering

```
┌──────────────────────────────────────────────────────────────────┐
│ 1. Both phone and address API calls complete successfully       │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│ 2. Check if AI filtering enabled                                │
└──────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
            ┌──────────────┐    ┌──────────────┐
            │ Enabled      │    │ Disabled     │
            └──────────────┘    └──────────────┘
                    │                   │
                    │                   ▼
                    │           ┌──────────────────┐
                    │           │ Show raw data    │
                    │           │ in Standard View │
                    │           └──────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────────────────────┐
│ 3. Prepare data for AI analysis                                 │
│    - Original customer data (name, phone, address)              │
│    - Reverse phone API response (full JSON)                     │
│    - Reverse address API response (full JSON)                   │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│ 4. ai_assistant.filter_and_rank_contacts()                      │
│    - Send data to GPT-4o-mini                                   │
│    - AI analyzes all contacts                                   │
│    - Identifies original customer                               │
│    - Ranks by confidence                                        │
│    - Generates insights                                         │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│ 5. AI returns structured JSON                                   │
│    {                                                            │
│      "primary_matches": [...],      // Priority 1              │
│      "related_contacts": [...],     // Priority 2              │
│      "insights": {                                              │
│        "acceptance_probability": 85,                            │
│        "recommended_first_contact": "+1-XXX-XXX-XXXX",         │
│        "best_time_to_call": "Weekday evenings",                │
│        ...                                                      │
│      }                                                          │
│    }                                                            │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│ 6. Display in AI Overview tab                                   │
│    ┌────────────────────────────────────────────────────────┐  │
│    │ ORIGINAL CUSTOMER DATA                                 │  │
│    │ - Name, Phone, Address                                 │  │
│    │ - AI correction indicator (if applied)                 │  │
│    ├────────────────────────────────────────────────────────┤  │
│    │ AI FILTERED RESULTS                                    │  │
│    │                                                        │  │
│    │ PRIORITY 1: DIRECT MATCHES                             │  │
│    │ ✓ Customer Name - Confidence: 95% (High)              │  │
│    │   📱 Phone (Mobile) [Copy] [Call]                      │  │
│    │   📍 Address                                           │  │
│    │   Reasoning: Exact match, current mobile               │  │
│    │                                                        │  │
│    │ PRIORITY 2: RELATED CONTACTS                           │  │
│    │ Spouse Name - Confidence: 72% (Medium)                │  │
│    │   📱 Phone (Mobile) [Copy] [Call]                      │  │
│    │   Reasoning: Same address, listed as spouse            │  │
│    ├────────────────────────────────────────────────────────┤  │
│    │ AI INSIGHTS & RECOMMENDATIONS                          │  │
│    │ - Acceptance Probability: 85% (High)                   │  │
│    │ - Recommended First Contact: +1-XXX-XXX-XXXX          │  │
│    │ - Best Time to Call: Weekday evenings                  │  │
│    │ - Address History: 1 move since purchase               │  │
│    │ - Additional Notes: ...                                │  │
│    └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

## Component Interaction

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Actions                            │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Setup        │    │ Load Person  │    │ Settings     │
│ - Enter key  │    │ - Auto API   │    │ - Toggle AI  │
│ - Test conn  │    │ - Manual API │    │ - Configure  │
└──────────────┘    └──────────────┘    └──────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │         dialer_gui.py                   │
        │  - Manages UI state                     │
        │  - Coordinates components               │
        │  - Displays results                     │
        └─────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ lead_        │    │ ai_          │    │ cache_       │
│ processor_   │    │ assistant    │    │ manager      │
│ v2.py        │    │ .py          │    │ .py          │
│              │    │              │    │              │
│ - API calls  │◄───┤ - Correction │    │ - Storage    │
│ - Parsing    │    │ - Filtering  │    │ - Retrieval  │
│ - Processing │    │ - Insights   │    │ - Stats      │
└──────────────┘    └──────────────┘    └──────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │         External Services               │
        │  ┌───────────────┐  ┌─────────────────┐│
        │  │ TrestleIQ API │  │ OpenAI API      ││
        │  │ - Phone       │  │ - GPT-4o-mini   ││
        │  │ - Address     │  │ - JSON mode     ││
        │  └───────────────┘  └─────────────────┘│
        └─────────────────────────────────────────┘
```

## Settings Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Settings Hierarchy                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │         Global Settings                 │
        │  (dialer_settings.json)                 │
        │  ┌───────────────────────────────────┐  │
        │  │ auto_phone_lookup: true           │  │
        │  │ auto_address_lookup: true         │  │
        │  │ ai_enabled: true/false            │  │
        │  │ ai_address_correction: true       │  │
        │  │ ai_person_filtering: true         │  │
        │  │ openai_api_key: "sk-..."          │  │
        │  └───────────────────────────────────┘  │
        └─────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │      Runtime Configuration              │
        │  ┌───────────────────────────────────┐  │
        │  │ AI Assistant Instance             │  │
        │  │ - Initialized if key present      │  │
        │  │ - None if key missing             │  │
        │  └───────────────────────────────────┘  │
        │  ┌───────────────────────────────────┐  │
        │  │ Lead Processor                    │  │
        │  │ - Receives AI assistant           │  │
        │  │ - Uses for corrections            │  │
        │  └───────────────────────────────────┘  │
        └─────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │      Per-Operation Decisions            │
        │  ┌───────────────────────────────────┐  │
        │  │ Address Lookup                    │  │
        │  │ - Check ai_enabled                │  │
        │  │ - Check ai_address_correction     │  │
        │  │ - Apply if both true              │  │
        │  └───────────────────────────────────┘  │
        │  ┌───────────────────────────────────┐  │
        │  │ Person Filtering                  │  │
        │  │ - Check ai_enabled                │  │
        │  │ - Check ai_person_filtering       │  │
        │  │ - Apply if both true              │  │
        │  └───────────────────────────────────┘  │
        └─────────────────────────────────────────┘
```

## Error Handling Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Error Scenarios                              │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ OpenAI Not   │    │ API Key      │    │ AI Call      │
│ Installed    │    │ Invalid      │    │ Fails        │
└──────────────┘    └──────────────┘    └──────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ HAS_OPENAI   │    │ Test         │    │ Try-Except   │
│ = False      │    │ Connection   │    │ Block        │
│              │    │ Fails        │    │              │
│ AI disabled  │    │              │    │ Log error    │
│ gracefully   │    │ Show error   │    │ Fall back    │
└──────────────┘    └──────────────┘    └──────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │      Graceful Degradation               │
        │  - Show raw data in Standard View       │
        │  - Display helpful message in AI tab    │
        │  - Update status bar with info          │
        │  - Application continues working        │
        │  - No crashes or data loss              │
        └─────────────────────────────────────────┘
```

## Cost Tracking

```
┌─────────────────────────────────────────────────────────────────┐
│                    Token Usage                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Address      │    │ Person       │    │ Total        │
│ Correction   │    │ Filtering    │    │ Per Person   │
│              │    │              │    │              │
│ ~500 tokens  │    │ ~2000 tokens │    │ ~2500 tokens │
│ $0.0002      │    │ $0.0008      │    │ $0.001       │
└──────────────┘    └──────────────┘    └──────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │      Cost Optimization                  │
        │  - Only correct failed addresses        │
        │  - Cache API responses                  │
        │  - Efficient prompts                    │
        │  - GPT-4o-mini (cheapest)               │
        │  - JSON mode (structured)               │
        └─────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │      Estimated Costs                    │
        │  - 100 people: ~$0.10                   │
        │  - 1000 people: ~$1.00                  │
        │  - 10000 people: ~$10.00                │
        └─────────────────────────────────────────┘
```

---

**Version:** 4.1  
**Date:** October 6, 2025  
**Status:** Complete ✓  
