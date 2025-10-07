# Setup Instructions

## Configuration Setup

1. **Copy the configuration template:**
   ```bash
   cp config_template.py config.py
   ```

2. **Edit config.py with your API keys:**
   - Add your TrestleIQ API key to `API_KEY`
   - Add your CloudTalk credentials to `CLOUDTALK_ACCESS_KEY_ID`, `CLOUDTALK_ACCESS_KEY_SECRET`, and `CLOUDTALK_AGENT_ID`
   - Add your OpenAI API key to `OPENAI_API_KEY`

3. **Example config.py:**
   ```python
   # TrestleIQ API Configuration
   API_KEY = "your_trestleiq_api_key_here"
   
   # CloudTalk API Configuration
   CLOUDTALK_ACCESS_KEY_ID = "your_cloudtalk_access_key_id"
   CLOUDTALK_ACCESS_KEY_SECRET = "your_cloudtalk_access_key_secret"
   CLOUDTALK_AGENT_ID = "your_agent_id"
   
   # OpenAI API Configuration
   OPENAI_API_KEY = "your_openai_api_key_here"
   ```

## Important Security Notes

- **Never commit config.py to version control** - it contains sensitive API keys
- The `config.py` file is already in `.gitignore` to prevent accidental commits
- Only commit `config_template.py` which contains empty placeholder values
- Keep your API keys secure and never share them publicly

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python launcher.py
   ```

## Using Default Settings

The application includes "Use Default Config" buttons that will load values from your `config.py` file:
- TrestleIQ API key loads automatically on startup
- CloudTalk and OpenAI credentials can be loaded using their respective "Use Default Config" buttons