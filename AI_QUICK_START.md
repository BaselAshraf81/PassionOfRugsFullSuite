# AI Features Quick Start Guide

## 5-Minute Setup

### Step 1: Install OpenAI Library (1 minute)

Open your command prompt or terminal and run:

```bash
pip install openai
```

Or install all dependencies at once:

```bash
pip install -r requirements.txt
```

### Step 2: Get Your OpenAI API Key (2 minutes)

1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Give it a name (e.g., "Passion Of Rugs Dialer")
5. Copy the key (starts with `sk-`)
6. **Important:** Save it somewhere safe - you won't see it again!

### Step 3: Configure in Application (1 minute)

1. Launch the Passion Of Rugs Advanced Dialer
2. In the setup screen, scroll to "AI Configuration (Optional)"
3. Paste your OpenAI API key
4. Click the "Test" button
5. Wait for "Connection Successful" message
6. Continue with normal setup

### Step 4: Use AI Features (1 minute)

1. Load a person (the app will automatically use AI if enabled)
2. Wait for API lookups to complete
3. Click the "AI Overview & Filtering" tab
4. View your AI-powered results!

## What You Get

### Automatic Address Correction
- Fixes typos and abbreviations in addresses
- Automatically retries failed lookups
- No extra clicks needed - happens in background
- See corrections in the AI tab

### Intelligent Person Filtering
- Identifies the original customer from all results
- Ranks contacts by confidence (High/Medium/Low)
- Shows related contacts (spouse, family)
- Provides insights:
  - Acceptance probability
  - Best time to call
  - Recommended phone number
  - Address history

### Cost
- ~$0.001 per person (0.1 cents)
- ~$1 for 1000 people
- Only charges when AI is used

## Quick Tips

### Enable/Disable AI Features

Click the ⚙️ Settings button in the dialer screen:
- ☑ AI Address Correction (auto-retry on failure)
- ☑ AI Person Filtering & Insights

### When to Use AI

**Use AI when:**
- Working with old or messy address data
- Need to identify original customer from multiple residents
- Want confidence scores for calling decisions
- Need insights on best time to call

**Skip AI when:**
- Data is already clean
- Simple, single-person results
- Want to minimize costs

### Troubleshooting

**"AI Features Disabled" message:**
- Make sure OpenAI library is installed: `pip install openai`
- Check API key is entered in setup
- Click "Test" to verify connection

**"No AI Analysis Available" message:**
- Wait for API calls to complete
- Check that accumulated data has meaningful results
- Make sure AI Person Filtering is enabled in settings

**Address correction not working:**
- Enable "AI Address Correction" in settings
- Check that address lookup actually failed
- Some addresses may be genuinely invalid

## Example Results

### Before AI (Standard View)
```
Multiple residents at address:
- John Smith (age 45)
- Mary Smith (age 42)
- John Smith Jr (age 20)
- Sarah Johnson (age 38)

Multiple phone numbers:
- +1-206-555-0100
- +1-206-555-0101
- +1-206-555-0102
- +1-206-555-0103
```

### After AI (AI Overview Tab)
```
PRIORITY 1: DIRECT MATCHES
✓ John Smith - Confidence: 95% (High)
  📱 +1-206-555-0100 (Mobile - T-Mobile)
  📍 456 Oak Ave, Seattle WA 98101
  Reasoning: Exact name match, current mobile number
  [Copy] [Call via CloudTalk]

PRIORITY 2: RELATED CONTACTS
Mary Smith (Spouse) - Confidence: 72% (Medium)
  📱 +1-206-555-0101 (Mobile)
  Reasoning: Listed as spouse, same address
  [Copy] [Call via CloudTalk]

AI INSIGHTS
Acceptance Probability: 85% (High)
Recommended First Contact: +1-206-555-0100
Best Time to Call: Weekday evenings (6-8 PM)
Address History: 1 move since purchase (2020)
```

## Need Help?

- **Full Documentation:** See AI_FEATURES.md
- **Technical Details:** See AI_IMPLEMENTATION_SUMMARY.md
- **OpenAI Status:** https://status.openai.com
- **API Key Issues:** Check OpenAI dashboard for credits

## That's It!

You're now using AI-powered features to improve your calling efficiency. The AI will automatically:
- Fix address problems
- Identify the right person to call
- Provide insights for better conversations

Happy calling! 📞

---

**Version:** 4.1  
**AI Model:** GPT-5 nano (cheapest option)  
**Cost:** ~$0.0005 per person (0.05 cents) - 50% cheaper!  
