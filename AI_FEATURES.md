# AI Features - Passion Of Rugs Advanced Dialer v4.1

## Overview

The AI Overview & Filtering tab provides intelligent address correction and person matching using OpenAI's GPT-5 nano model (the cheapest option available). These features help improve data quality and identify the original customer more accurately.

## Features

### 1. AI Address Correction (Automatic Retry)

**What it does:**
- Automatically corrects malformed addresses when API lookups fail
- Retries the API call with the corrected address
- No user approval needed - happens seamlessly in the background

**When it triggers:**
- Only when reverse address API returns no results or errors
- Reactive fix only - doesn't correct addresses that work

**How it works:**
1. Initial address lookup fails
2. AI analyzes the address and corrects common issues:
   - Abbreviated street types (St→Street, Ave→Avenue, etc.)
   - Missing or misspelled state codes
   - Incomplete ZIP codes
   - Typos and OCR errors
   - Street numbers in wrong position
3. Automatically retries with corrected address
4. If successful, logs the correction for transparency
5. If still fails, tries one more correction (max 2 attempts)

**Status bar messages:**
- "Address lookup failed - AI correcting format..."
- "Retrying with corrected address (attempt 1)..."
- "Address corrected and verified ✓"
- "Address validation failed - manual review needed"

**Cost:** ~$0.0002 per correction (~500 tokens)

---

### 2. Intelligent Person Matching & Filtering

**What it does:**
- Analyzes both reverse phone and reverse address API responses
- Identifies the original customer from all returned contacts
- Filters out unrelated residents and relatives
- Ranks contacts by confidence score
- Provides actionable insights and recommendations

**When it triggers:**
- After BOTH reverse phone AND reverse address API calls succeed
- Only if AI features are enabled in settings

**Data analyzed:**
- Original customer data (name, phone, address from 2015)
- Reverse phone API response (owners, phones, addresses)
- Reverse address API response (current residents, associated people)

**Confidence scoring:**
- **High (80-100%):** Exact name match, mobile phone, current resident
- **Medium (50-79%):** Partial name match, related person, landline
- **Low (0-49%):** Only last name match, unclear relationship, VOIP

**Output sections:**

#### Priority 1: Direct Matches
- Exact or strong matches to original customer
- All phone numbers for that person (deduplicated)
- Prioritized: Mobile > Landline > VOIP
- Includes confidence score and reasoning

#### Priority 2: Related Contacts
- Spouse, same last name, associated persons
- Only shown if clearly connected to customer
- Lower confidence scores
- Useful as backup contacts

#### AI Insights & Recommendations
- **Acceptance Probability:** Likelihood customer will engage (0-100%)
- **Recommended First Contact:** Best phone number to call
- **Best Time to Call:** Optimal calling window
- **Address History:** Number of moves since purchase
- **Time at Current Address:** How long at current location
- **Additional Notes:** Other relevant observations

**Cost:** ~$0.0008 per person (~2000 tokens)

---

## Setup

### 1. Install OpenAI Library

```bash
pip install openai
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

### 2. Get OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy the key (starts with `sk-`)

### 3. Configure in Application

**During Setup:**
1. Launch the application
2. In the setup screen, find "AI Configuration (Optional)"
3. Paste your OpenAI API key
4. Click "Test" to verify connection
5. Continue with normal setup

**The AI features will be automatically enabled if:**
- OpenAI library is installed
- Valid API key is provided
- Test connection succeeds

---

## Using AI Features

### Viewing AI Analysis

1. Load a person (with auto lookups enabled)
2. Wait for API calls to complete
3. Click the "AI Overview & Filtering" tab
4. View filtered results and insights

### AI Tab Layout

```
┌─────────────────────────────────────────────┐
│ ORIGINAL CUSTOMER DATA                      │
│ Name, Phone, Address from dataset           │
│ ✓ Shows AI correction if applied            │
├─────────────────────────────────────────────┤
│ AI FILTERED RESULTS                         │
│                                             │
│ PRIORITY 1: DIRECT MATCHES                  │
│ ✓ Customer Name - Confidence: 95% (High)   │
│   📱 Phone (Mobile - Carrier)               │
│   📍 Current Address                        │
│   [Copy] [Call via CloudTalk]               │
│                                             │
│ PRIORITY 2: RELATED CONTACTS                │
│ Spouse Name - Confidence: 72% (Medium)     │
│   📱 Phone (Mobile)                         │
│   [Copy] [Call via CloudTalk]               │
├─────────────────────────────────────────────┤
│ AI INSIGHTS & RECOMMENDATIONS               │
│ Acceptance Probability: 85% (High)          │
│ Recommended First Contact: +1-XXX-XXX-XXXX │
│ Best Time to Call: Weekday evenings         │
│ Address History: 1 move since purchase      │
│ Additional Notes: ...                       │
└─────────────────────────────────────────────┘
```

### Calling from AI Tab

- Click "Call via CloudTalk" button next to any phone number
- Works the same as calling from Standard View
- Call history is tracked normally

### Copying Phone Numbers

- Click "Copy" button to copy phone to clipboard
- Status bar confirms the copy

---

## Settings

Access settings via the ⚙️ Settings button in the dialer screen.

**AI Settings (when AI is enabled):**

- ☑ **AI Address Correction (auto-retry on failure)**
  - Enable/disable automatic address correction
  - When disabled, failed addresses won't be corrected
  
- ☑ **AI Person Filtering & Insights**
  - Enable/disable intelligent person matching
  - When disabled, AI tab shows raw data only

**Note:** These settings can be toggled without restarting the application.

---

## Cost Estimation

Using GPT-5 nano (cheapest OpenAI model available):
- Input: $0.050 per 1M tokens
- Output: $0.400 per 1M tokens

**Per person with both features (GPT-5 nano):**
- Address correction (if needed): ~$0.00010 (500 input + 200 output tokens)
- Person filtering: ~$0.00042 (2000 input + 800 output tokens)
- **Total: ~$0.0005 per person (0.05 cents) - 50% cheaper!**

**For 1000 people:**
- Estimated cost: ~$0.50 (half the previous cost!)
- Assuming 30% need address correction

**Cost optimization:**
- Only corrects addresses that fail (not all addresses)
- Corrections are logged and can be cached
- Person filtering only runs when both APIs succeed
- No redundant API calls

---

## Troubleshooting

### AI Features Not Available

**Problem:** AI tab shows "AI Features Disabled"

**Solutions:**
1. Check OpenAI library is installed: `pip install openai`
2. Verify API key is entered in setup
3. Click "Test" button to verify connection
4. Restart application after installing OpenAI

### AI Analysis Not Showing

**Problem:** AI tab shows "No AI Analysis Available"

**Possible causes:**
1. API lookups haven't completed yet
2. Both phone and address lookups failed
3. AI Person Filtering is disabled in settings

**Solutions:**
1. Wait for API calls to complete
2. Check Standard View tab for results
3. Enable AI Person Filtering in settings
4. Try manual API buttons if auto lookups are off

### Address Correction Not Working

**Problem:** Addresses still failing after AI correction

**Possible causes:**
1. Address is genuinely invalid (doesn't exist)
2. Max correction attempts reached (2 attempts)
3. AI Address Correction disabled in settings

**Solutions:**
1. Check original address data quality
2. Try manual address lookup with corrected data
3. Enable AI Address Correction in settings
4. Review AI correction log in AI tab

### API Key Errors

**Problem:** "Connection failed" when testing API key

**Solutions:**
1. Verify API key is correct (starts with `sk-`)
2. Check internet connection
3. Verify OpenAI account has credits
4. Check API key hasn't been revoked
5. Try generating a new API key

---

## Privacy & Data

**What data is sent to OpenAI:**
- Original customer name, phone, address
- API responses from TrestleIQ (phone and address lookups)
- No sensitive business data or call history

**Data retention:**
- OpenAI retains data for 30 days for abuse monitoring
- After 30 days, data is deleted
- See OpenAI's data usage policy for details

**Local storage:**
- AI corrections are logged locally in memory
- No AI results are saved to Excel
- Only verified contact data goes to Excel

---

## Best Practices

### When to Use AI Features

**Use AI Address Correction when:**
- Working with old or OCR-scanned address data
- Addresses have abbreviations or typos
- High failure rate on address lookups

**Use AI Person Filtering when:**
- Need to identify original customer from multiple residents
- Want confidence scores for calling decisions
- Need insights on best time to call

### When to Disable AI Features

**Disable AI Address Correction when:**
- Address data is already clean and validated
- Want to minimize API costs
- Prefer manual address correction

**Disable AI Person Filtering when:**
- Don't need detailed analysis
- Working with simple, single-person results
- Want to minimize API costs

### Optimizing Costs

1. **Enable caching:** Reuse API responses without re-analyzing
2. **Batch processing:** Process multiple people in one session
3. **Selective use:** Enable AI only for difficult cases
4. **Monitor usage:** Check OpenAI dashboard for token usage

---

## Technical Details

### AI Model

- **Model:** GPT-5 nano (cheapest option available)
- **Provider:** OpenAI
- **Cost:** $0.050/1M input, $0.400/1M output tokens
- **Response format:** JSON mode (structured output)
- **Temperature:** 0.1 (deterministic, consistent results)
- **Max tokens:** 300 (address correction), 1500 (person filtering)
- **Alternative:** GPT-4.1 nano ($0.20/$0.80 per 1M tokens)

### Address Correction Prompt

The AI receives:
- Original address components (street, city, state, ZIP)
- API requirements and validation rules
- Common address issues to fix
- Expected JSON output format

Returns:
- Corrected address components
- Reasoning for corrections made

### Person Filtering Prompt

The AI receives:
- Original customer data
- Full reverse phone API response
- Full reverse address API response
- Instructions for matching and scoring

Returns:
- Primary matches (direct customer matches)
- Related contacts (family members, etc.)
- Insights (acceptance probability, recommendations)

---

## Future Enhancements

Potential improvements for future versions:

1. **AI Learning:** Learn from user corrections to improve accuracy
2. **Batch Analysis:** Analyze multiple people at once for efficiency
3. **Custom Prompts:** Allow users to customize AI instructions
4. **Cost Tracking:** Display real-time token usage and costs
5. **Export AI Insights:** Option to export AI analysis to Excel
6. **Alternative Models:** Support for other AI providers (Anthropic, etc.)

---

## Support

For issues or questions about AI features:

1. Check this documentation first
2. Review error messages in status bar
3. Check OpenAI API status: https://status.openai.com
4. Verify API key and credits in OpenAI dashboard

---

**Version:** 4.1  
**Last Updated:** 2025-10-06  
**AI Model:** GPT-5 nano (cheapest: $0.050/$0.400 per 1M tokens)  
