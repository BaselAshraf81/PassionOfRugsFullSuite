# Configuration template for TrestleIQ API processing
# Copy this file to config.py and fill in your actual API keys

# TrestleIQ API Configuration
API_KEY = ""  # Enter your TrestleIQ API key here
BASE_URL = "https://api.trestleiq.com"

# CloudTalk API Configuration (for Dialer GUI Mode)
CLOUDTALK_ACCESS_KEY_ID = ""  # Enter your CloudTalk Access Key ID
CLOUDTALK_ACCESS_KEY_SECRET = ""  # Enter your CloudTalk Access Key Secret
CLOUDTALK_AGENT_ID = ""  # Enter your CloudTalk Agent ID

# OpenAI API Configuration (for AI features)
OPENAI_API_KEY = ""  # Enter your OpenAI API key here

# File paths
INPUT_FILE = "PV_filtered_ActivityBelow40_AllLineTypes.xlsx"
OUTPUT_FILE = "processed_results.csv"

# Processing settings
ACTIVITY_SCORE_THRESHOLD = 30  # Only process entries with activity score <= this value
RATE_LIMIT_DELAY = 0.1  # Seconds to wait between API calls

# Column mappings (adjust if your Excel columns have different names)
COLUMN_MAPPING = {
    'name': 'name',
    'phone': 'phone', 
    'address': 'address',
    'city': 'city',
    'state': 'state',
    'zip': 'zip',
    'activity_score': 'activity_score'  # Note: underscore not space
}