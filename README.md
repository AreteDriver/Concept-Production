# EVE Online Mobile App - Neocom 2.0

A modern, AI-powered mobile application for EVE Online with advanced features for character management, route planning, asset tracking, and AI-assisted logistics decisions.

## Quick Start

```bash
pip install -r requirements.txt
streamlit run eve_neocom_app.py
```

## Features

- 🚀 **Multi-Character Management**: Support for up to 100 characters
- 🗺️ **Intelligent Route Planning**: AI-powered route optimization with 2D map visualization
- 🛡️ **Threat Assessment**: Real-time zKillboard integration for danger analysis
- 🚢 **Jump-Capable Ship Support**: Routes for carriers, jump freighters, and more
- 📊 **Asset Tracking**: Monitor all character assets across New Eden
- 💰 **Market Orders**: Track and analyze market orders
- 🤖 **AI Assistant**: Fitting suggestions, logistics decisions, and route optimization
- ⚡ **ESI Integration**: Full EVE Online ESI API integration

## Documentation

See [EVE_NEOCOM_README.md](EVE_NEOCOM_README.md) for comprehensive documentation.

## Project Structure

```
eve_app/
├── api/              # ESI and zKillboard API clients
├── modules/          # Core functionality (characters, routes)
├── ai/               # AI assistant features
├── ui/               # Streamlit user interface
└── data/             # Character and app data storage
```

## Original TLS Concept

This repository was originally a scaffold for an AI-driven QA/Lean system under development. The EVE Online app represents a practical implementation of AI-assisted decision support systems.
