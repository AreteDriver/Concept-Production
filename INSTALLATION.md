# Installation Guide - EVE Online Mobile App (Neocom 2.0)

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/AreteDriver/TLS-Concept-production-2.0.git
cd TLS-Concept-production-2.0
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run eve_neocom_app.py
```

The application will open in your browser at `http://localhost:8501`

## Configuration (Optional)

### EVE Online ESI API Setup

To enable full character authentication and private data access:

1. **Register Your Application**
   - Go to https://developers.eveonline.com/
   - Create a new application
   - Set the callback URL to `http://localhost:8501/callback`
   - Note your Client ID and Client Secret

2. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your credentials
   ```

3. **Set Required Scopes**
   The app requires these ESI scopes:
   - `esi-characters.read_corporation_roles.v1`
   - `esi-assets.read_assets.v1`
   - `esi-markets.read_character_orders.v1`
   - `esi-location.read_location.v1`
   - `esi-skills.read_skills.v1`

### OpenAI Integration (Optional)

For enhanced AI features:

1. Obtain an API key from https://platform.openai.com/
2. Add to `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## System Requirements

- Python 3.8 or higher
- 2GB RAM minimum
- Internet connection for API access

## Troubleshooting

### Dependencies Installation Issues

If you encounter issues installing requirements:

```bash
# Use a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Port Already in Use

If port 8501 is in use:

```bash
streamlit run eve_neocom_app.py --server.port 8502
```

### API Connection Issues

- Ensure you have internet connectivity
- Check ESI API status at https://esi.evetech.net/ui/
- Verify zKillboard is accessible at https://zkillboard.com/

## Running Tests

To verify the installation:

```bash
python test_app.py
```

Expected output: 3-5 tests should pass (ESI tests may fail without internet access)

## Docker Support (Future)

Docker support coming soon for easier deployment.

## Support

- Issues: https://github.com/AreteDriver/TLS-Concept-production-2.0/issues
- EVE ESI Docs: https://esi.evetech.net/ui/
- Streamlit Docs: https://docs.streamlit.io/
