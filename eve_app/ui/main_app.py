"""Main Streamlit UI for EVE Online Mobile App."""

import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from eve_app.api.esi_client import ESIClient
from eve_app.api.zkillboard_client import ZKillboardClient
from eve_app.modules.character_manager import CharacterManager, Character
from eve_app.modules.route_planner import RoutePlanner
from eve_app.ai.assistant import AIAssistant


def init_session_state():
    """Initialize Streamlit session state."""
    if 'character_manager' not in st.session_state:
        st.session_state.character_manager = CharacterManager()
    if 'esi_client' not in st.session_state:
        st.session_state.esi_client = ESIClient()
    if 'zkill_client' not in st.session_state:
        st.session_state.zkill_client = ZKillboardClient()
    if 'route_planner' not in st.session_state:
        st.session_state.route_planner = RoutePlanner(
            st.session_state.esi_client,
            st.session_state.zkill_client
        )
    if 'ai_assistant' not in st.session_state:
        st.session_state.ai_assistant = AIAssistant()


def show_character_management():
    """Display character management interface."""
    st.header("Character Management")
    
    char_mgr = st.session_state.character_manager
    
    # Show character count
    count = char_mgr.get_character_count()
    st.info(f"Characters: {count}/{char_mgr.MAX_CHARACTERS}")
    
    # Add character section
    with st.expander("Add New Character", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            char_id = st.number_input("Character ID", min_value=1, step=1)
            char_name = st.text_input("Character Name")
        with col2:
            access_token = st.text_input("Access Token (optional)", type="password")
            refresh_token = st.text_input("Refresh Token (optional)", type="password")
        
        if st.button("Add Character"):
            if char_name and char_id:
                char = Character(
                    character_id=char_id,
                    name=char_name,
                    access_token=access_token if access_token else None,
                    refresh_token=refresh_token if refresh_token else None
                )
                if char_mgr.add_character(char):
                    st.success(f"Added character: {char_name}")
                    st.rerun()
                else:
                    st.error("Failed to add character (may be at maximum)")
            else:
                st.warning("Please provide character ID and name")
    
    # List characters
    st.subheader("Your Characters")
    characters = char_mgr.get_all_characters()
    
    if not characters:
        st.info("No characters added yet. Add your first character above!")
    else:
        for char in characters:
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"**{char.name}**")
                    st.caption(f"ID: {char.character_id}")
                with col2:
                    token_status = "✓ Authenticated" if char.is_token_valid() else "✗ No Token"
                    st.write(token_status)
                with col3:
                    if st.button("Remove", key=f"remove_{char.character_id}"):
                        char_mgr.remove_character(char.character_id)
                        st.rerun()
                st.divider()


def show_route_planner():
    """Display route planning interface."""
    st.header("Route Planner & 2D Map")
    
    col1, col2 = st.columns(2)
    with col1:
        origin = st.number_input("Origin System ID", min_value=30000000, max_value=33000000, value=30000142)
        ship_type = st.selectbox("Ship Type", 
            ["regular", "carrier", "dreadnought", "jump_freighter", "black_ops", "titan"])
    with col2:
        destination = st.number_input("Destination System ID", min_value=30000000, max_value=33000000, value=30002187)
        skill_level = st.slider("Jump Drive Skill Level", 0, 5, 5)
    
    avoid_dangerous = st.checkbox("Avoid Dangerous Systems", value=True)
    cargo_value = st.number_input("Estimated Cargo Value (ISK)", min_value=0, value=0, step=100000000)
    
    if st.button("Calculate Route"):
        with st.spinner("Calculating route..."):
            route_planner = st.session_state.route_planner
            route_data = route_planner.calculate_route(
                origin=origin,
                destination=destination,
                ship_type=ship_type,
                avoid_dangerous=avoid_dangerous,
                skill_level=skill_level
            )
            
            if route_data['success']:
                st.success("Route calculated successfully!")
                
                # Show route analysis
                analysis = route_data['analysis']
                st.subheader("Route Analysis")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Jumps", analysis['total_jumps'])
                with col2:
                    st.metric("Danger Level", analysis['overall_danger'])
                with col3:
                    dangerous_count = len(analysis['dangerous_systems'])
                    st.metric("Dangerous Systems", dangerous_count)
                
                # Security breakdown
                st.subheader("Security Breakdown")
                sec_stats = analysis['security_stats']
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("High Sec", sec_stats['highsec'])
                with col2:
                    st.metric("Low Sec", sec_stats['lowsec'])
                with col3:
                    st.metric("Null Sec", sec_stats['nullsec'])
                
                # Dangerous systems
                if analysis['dangerous_systems']:
                    st.subheader("⚠️ Dangerous Systems")
                    for sys in analysis['dangerous_systems']:
                        with st.expander(f"{sys['name']} - {sys['threat']['danger_level']}"):
                            st.write(f"Recent Kills: {sys['threat']['recent_kills']}")
                            st.write(f"Pod Kills: {sys['threat']['pod_kills']}")
                            st.write(f"Active Gankers: {len(sys['threat']['active_gankers'])}")
                
                # AI Suggestions
                st.subheader("🤖 AI Recommendations")
                ai_assistant = st.session_state.ai_assistant
                suggestions = ai_assistant.suggest_route(route_data, cargo_value=cargo_value)
                
                st.write(f"**Assessment:** {suggestions['overall_assessment']}")
                
                for rec in suggestions['recommendations']:
                    priority_emoji = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
                    st.write(f"{priority_emoji} **{rec['type'].replace('_', ' ').title()}:** {rec['message']}")
                    if 'action' in rec:
                        st.caption(f"→ {rec['action']}")
                
                # 2D Map visualization
                st.subheader("Route Map")
                map_data = route_planner.get_2d_map_data(route_data['gate_route'])
                
                # Simple text representation (would be replaced with actual 2D map)
                st.info(f"Route through {map_data['total_systems']} systems")
                for i, system in enumerate(map_data['systems'][:10]):  # Show first 10
                    danger_emoji = "🟢" if system['danger_level'] == 'safe' else "🟡" if system['danger_level'] == 'moderate' else "🔴"
                    st.write(f"{i+1}. {danger_emoji} {system['name']} (Sec: {system['security']:.2f})")
                
                if len(map_data['systems']) > 10:
                    st.caption(f"... and {len(map_data['systems']) - 10} more systems")
                
                # Alternative routes
                if route_data['alternatives']:
                    st.subheader("Alternative Routes")
                    for i, alt in enumerate(route_data['alternatives'][:3]):
                        with st.expander(f"Alternative {i+1}: {alt['type']} route"):
                            st.write(f"Jumps: {alt['analysis']['total_jumps']}")
                            st.write(f"Danger: {alt['analysis']['overall_danger']}")
            else:
                st.error(f"Failed to calculate route: {route_data.get('error', 'Unknown error')}")


def show_asset_tracker():
    """Display asset tracking interface."""
    st.header("Asset Tracker")
    
    char_mgr = st.session_state.character_manager
    characters = char_mgr.get_all_characters()
    
    if not characters:
        st.info("Add characters to track their assets")
        return
    
    selected_char = st.selectbox(
        "Select Character",
        options=characters,
        format_func=lambda x: x.name
    )
    
    if selected_char:
        st.subheader(f"Assets for {selected_char.name}")
        
        if selected_char.is_token_valid():
            if st.button("Refresh Assets"):
                with st.spinner("Fetching assets..."):
                    esi_client = st.session_state.esi_client
                    assets = esi_client.get_character_assets(
                        selected_char.character_id,
                        selected_char.access_token
                    )
                    
                    if assets:
                        st.success(f"Found {len(assets)} assets")
                        char_mgr.update_character_data(
                            selected_char.character_id,
                            assets=assets
                        )
                    else:
                        st.warning("No assets found or authentication failed")
        else:
            st.warning("Character not authenticated. Add access token to view assets.")
        
        # Display cached assets
        if selected_char.assets:
            st.write(f"Cached assets: {len(selected_char.assets)} items")
            st.caption("Note: This is sample data. Full implementation would show detailed asset list.")
        else:
            st.info("No cached assets. Refresh to fetch from ESI.")


def show_market_orders():
    """Display market orders interface."""
    st.header("Market Orders")
    
    char_mgr = st.session_state.character_manager
    characters = char_mgr.get_all_characters()
    
    if not characters:
        st.info("Add characters to track their market orders")
        return
    
    selected_char = st.selectbox(
        "Select Character",
        options=characters,
        format_func=lambda x: x.name,
        key="market_char_select"
    )
    
    if selected_char:
        st.subheader(f"Market Orders for {selected_char.name}")
        
        if selected_char.is_token_valid():
            if st.button("Refresh Orders"):
                with st.spinner("Fetching orders..."):
                    esi_client = st.session_state.esi_client
                    orders = esi_client.get_character_orders(
                        selected_char.character_id,
                        selected_char.access_token
                    )
                    
                    if orders:
                        st.success(f"Found {len(orders)} active orders")
                        char_mgr.update_character_data(
                            selected_char.character_id,
                            orders=orders
                        )
                        
                        # AI analysis
                        ai_assistant = st.session_state.ai_assistant
                        analysis = ai_assistant.analyze_market_opportunity(orders)
                        
                        st.subheader("Market Analysis")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Orders", analysis['total_orders'])
                        with col2:
                            st.metric("Buy Orders", analysis['buy_orders'])
                        with col3:
                            st.metric("Sell Orders", analysis['sell_orders'])
                        
                        st.write(f"**Total Value:** {analysis['total_value']:,.2f} ISK")
                    else:
                        st.info("No active orders found")
        else:
            st.warning("Character not authenticated. Add access token to view orders.")


def show_ship_fitting():
    """Display ship fitting suggestions interface."""
    st.header("Ship Fitting Assistant")
    
    col1, col2 = st.columns(2)
    with col1:
        ship_type = st.text_input("Ship Type", "Iteron Mark V")
        purpose = st.selectbox("Purpose", ["hauling", "combat", "exploration", "mining"])
    with col2:
        budget = st.number_input("Budget (ISK)", min_value=0, value=100000000, step=10000000)
    
    if st.button("Get Fitting Suggestions"):
        ai_assistant = st.session_state.ai_assistant
        fitting = ai_assistant.suggest_fitting(ship_type, purpose, budget)
        
        st.subheader(f"Suggested Fit: {fitting['ship']}")
        st.write(f"**Purpose:** {fitting['purpose']}")
        
        st.subheader("Modules")
        for module in fitting['modules']:
            st.write(f"- **{module['category'].title()}:** {module['module']}")
        
        if fitting['notes']:
            st.subheader("Notes")
            for note in fitting['notes']:
                st.info(note)


def main():
    """Main application entry point."""
    st.set_page_config(
        page_title="EVE Online - Neocom 2.0",
        page_icon="🚀",
        layout="wide"
    )
    
    st.title("🚀 EVE Online Mobile App - Neocom 2.0")
    st.caption("Modern mobile app for EVE Online with AI assistance")
    
    init_session_state()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select Page",
        ["Character Management", "Route Planner", "Asset Tracker", 
         "Market Orders", "Ship Fitting"]
    )
    
    st.sidebar.divider()
    st.sidebar.info(
        "**Features:**\n"
        "- Manage up to 100 characters\n"
        "- ESI API integration\n"
        "- zKillboard threat analysis\n"
        "- AI-powered route planning\n"
        "- 2D route map visualization\n"
        "- Ship fitting suggestions\n"
        "- Asset & market tracking"
    )
    
    # Show selected page
    if page == "Character Management":
        show_character_management()
    elif page == "Route Planner":
        show_route_planner()
    elif page == "Asset Tracker":
        show_asset_tracker()
    elif page == "Market Orders":
        show_market_orders()
    elif page == "Ship Fitting":
        show_ship_fitting()


if __name__ == "__main__":
    main()
