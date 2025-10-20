# EVE Online Mobile App - Neocom 2.0

A modern, AI-powered mobile application for EVE Online, inspired by Neocom II with updated technology and enhanced features.

## Features

### Character Management
- **Multi-Character Support**: Manage up to 100 characters
- **ESI SSO Integration**: Authenticate characters via EVE Online SSO
- **Character Data**: Track skills, assets, and market orders for each character

### Route Planning
- **Intelligent Route Calculation**: Calculate optimal routes between solar systems
- **2D Map Visualization**: Visual representation of routes with system information
- **Jump-Capable Ship Support**: Special routing for carriers, dreadnoughts, jump freighters, and more
- **Skill Consideration**: Routes adjusted based on jump drive skill levels
- **Threat Assessment**: Integration with zKillboard for real-time danger analysis

### Asset Tracking
- **Real-Time Asset Data**: View all character assets across New Eden
- **Location Tracking**: See where your items are located
- **Asset Organization**: Easy-to-navigate asset list

### Market Orders
- **Order Monitoring**: Track all active buy and sell orders
- **Market Analysis**: AI-powered market opportunity analysis
- **Order Management**: View order status and history

### AI Assistant Features
- **Route Optimization**: AI suggests optimal routes based on cargo value and threat level
- **Alternative Routes**: Automatically identifies and suggests safer alternatives
- **Ship Fitting Suggestions**: Get AI-powered fitting recommendations
- **Threat Analysis**: Real-time analysis of hostile forces and gankers per system
- **Logistics Decision Support**: AI-assisted decision making for logistics operations

### Security & Threat Intelligence
- **zKillboard Integration**: Real-time kill data from zKillboard API
- **System Danger Levels**: Automatic classification of system danger
- **Active Ganker Tracking**: Identifies and tracks active hostile pilots
- **Pod Kill Monitoring**: Tracks capsule kills as danger indicators
- **Historical Kill Data**: Analyzes recent activity to assess current threats

## Technical Architecture

### Project Structure
```
eve_app/
├── api/
│   ├── esi_client.py          # EVE ESI API integration
│   └── zkillboard_client.py   # zKillboard API integration
├── modules/
│   ├── character_manager.py   # Character management
│   └── route_planner.py       # Route planning & 2D map
├── ai/
│   └── assistant.py           # AI decision support
├── ui/
│   └── main_app.py           # Streamlit UI
└── data/
    └── characters.json        # Character storage
```

### API Integrations

#### ESI (EVE Swagger Interface)
- Character information
- Skills and training
- Assets and locations
- Market orders
- Route calculation
- System information

#### zKillboard
- System kill statistics
- Character kill history
- Threat level analysis
- Active ganker identification

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup
```bash
# Clone the repository
git clone https://github.com/AreteDriver/TLS-Concept-production-2.0.git
cd TLS-Concept-production-2.0

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run eve_neocom_app.py
```

## Usage

### Running the Application
```bash
streamlit run eve_neocom_app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Adding Characters
1. Navigate to "Character Management"
2. Click "Add New Character"
3. Enter Character ID and Name
4. (Optional) Add OAuth tokens for authenticated features
5. Click "Add Character"

### Planning Routes
1. Navigate to "Route Planner"
2. Enter Origin and Destination system IDs
3. Select ship type (regular or jump-capable)
4. Set jump drive skill level if applicable
5. Enter estimated cargo value
6. Click "Calculate Route"
7. Review AI recommendations and threat analysis

### Viewing Assets
1. Navigate to "Asset Tracker"
2. Select a character
3. Click "Refresh Assets" (requires authentication)
4. View all assets and locations

### Tracking Market Orders
1. Navigate to "Market Orders"
2. Select a character
3. Click "Refresh Orders" (requires authentication)
4. View AI-powered market analysis

### Getting Fitting Suggestions
1. Navigate to "Ship Fitting"
2. Enter ship type and purpose
3. Set budget
4. Click "Get Fitting Suggestions"
5. Review recommended modules and notes

## Configuration

### EVE SSO Setup (Optional)
To enable full character authentication:

1. Create an application at https://developers.eveonline.com/
2. Configure OAuth callback URL
3. Add Client ID and Secret to the ESI client initialization

### OpenAI Integration (Optional)
For enhanced AI features:

1. Obtain OpenAI API key
2. Initialize AIAssistant with API key
3. Advanced AI features will be available

## Features in Detail

### Jump-Capable Ship Support
The route planner supports the following jump-capable ships:
- **Titans**: 6.0 LY base range
- **Supercarriers**: 6.0 LY base range
- **Carriers**: 7.0 LY base range
- **Dreadnoughts**: 7.0 LY base range
- **Force Auxiliaries**: 7.0 LY base range
- **Jump Freighters**: 10.0 LY base range
- **Black Ops**: 8.0 LY base range

Range increases by 20% per level of Jump Drive Calibration skill.

### Threat Assessment System
The threat assessment analyzes:
- Number of kills in last 24 hours
- Pod kills (high danger indicator)
- Total ISK value lost
- Active ganker identification
- Kill frequency patterns

Danger levels:
- **Safe**: Few or no recent kills
- **Moderate**: Some activity, exercise caution
- **Dangerous**: High activity, significant risk
- **Very Dangerous**: Extreme activity, avoid if possible

### AI Decision Support
The AI assistant provides:
- Risk assessment based on cargo value and route danger
- Timing suggestions (off-peak hours)
- Escort recommendations for valuable cargo
- Alternative route suggestions
- System-specific warnings with actionable advice

## Development

### Adding New Features
The modular architecture makes it easy to add new features:

1. **New API Integration**: Add client in `eve_app/api/`
2. **New Module**: Add functionality in `eve_app/modules/`
3. **New AI Feature**: Extend `eve_app/ai/assistant.py`
4. **New UI Page**: Add to `eve_app/ui/main_app.py`

### Testing
```bash
# Run tests (when test suite is added)
python -m pytest tests/
```

## Known Limitations

1. Character data requires valid OAuth tokens for full functionality
2. 2D map visualization is simplified (can be enhanced with actual coordinate data)
3. Jump route calculation is approximated (requires actual system coordinate database)
4. Market analysis is basic (can be enhanced with AI/ML models)

## Future Enhancements

- [ ] Mobile-native application (React Native or Flutter)
- [ ] Push notifications for market orders and asset alerts
- [ ] Advanced fitting simulation with EFT/Pyfa integration
- [ ] Corporation/Alliance fleet management
- [ ] Wormhole mapping integration
- [ ] Advanced market analytics with ML predictions
- [ ] Real-time price tracking
- [ ] Contract management
- [ ] Industry and manufacturing planning
- [ ] PI (Planetary Interaction) management

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes. EVE Online and all associated logos and designs are the intellectual property of CCP Games.

## Acknowledgments

- CCP Games for EVE Online and the ESI API
- zKillboard for kill data API
- Original Neocom II developers for inspiration

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/AreteDriver/TLS-Concept-production-2.0/issues
- EVE Online ESI Documentation: https://esi.evetech.net/ui/
- zKillboard API: https://github.com/zKillboard/zKillboard

## Disclaimer

This is an unofficial tool and is not affiliated with or endorsed by CCP Games. Use at your own risk. Always follow the EVE Online EULA and Terms of Service.
