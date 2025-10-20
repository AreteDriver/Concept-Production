"""Simple test script to verify EVE app functionality."""

from eve_app.api.esi_client import ESIClient
from eve_app.api.zkillboard_client import ZKillboardClient
from eve_app.modules.character_manager import CharacterManager, Character
from eve_app.modules.route_planner import RoutePlanner
from eve_app.ai.assistant import AIAssistant


def test_esi_client():
    """Test ESI client."""
    print("Testing ESI Client...")
    client = ESIClient()
    
    # Test public endpoint (Jita)
    system_info = client.get_system_info(30000142)
    if system_info:
        print(f"✓ ESI Client working: Retrieved {system_info.get('name', 'Unknown')} system info")
    else:
        print("✗ ESI Client failed")
    return bool(system_info)


def test_character_manager():
    """Test character manager."""
    print("\nTesting Character Manager...")
    
    # Use temp storage for testing
    import tempfile
    import os
    temp_dir = tempfile.mkdtemp()
    storage_path = os.path.join(temp_dir, 'test_chars.json')
    
    manager = CharacterManager(storage_path=storage_path)
    
    # Add test character
    char = Character(character_id=123456, name="Test Pilot")
    success = manager.add_character(char)
    
    if success and manager.get_character_count() == 1:
        print(f"✓ Character Manager working: Added and retrieved character")
        
        # Test removal
        manager.remove_character(123456)
        if manager.get_character_count() == 0:
            print(f"✓ Character removal working")
        
        return True
    else:
        print("✗ Character Manager failed")
        return False


def test_route_planner():
    """Test route planner."""
    print("\nTesting Route Planner...")
    
    esi_client = ESIClient()
    zkill_client = ZKillboardClient()
    planner = RoutePlanner(esi_client, zkill_client)
    
    # Test route calculation (Jita to Amarr)
    route_data = planner.calculate_route(
        origin=30000142,  # Jita
        destination=30002187,  # Amarr
        ship_type='regular'
    )
    
    if route_data['success']:
        print(f"✓ Route Planner working: Calculated route with {route_data['analysis']['total_jumps']} jumps")
        return True
    else:
        print("✗ Route Planner failed")
        return False


def test_ai_assistant():
    """Test AI assistant."""
    print("\nTesting AI Assistant...")
    
    assistant = AIAssistant()
    
    # Test fitting suggestion
    fitting = assistant.suggest_fitting('Iteron Mark V', 'hauling', budget=100_000_000)
    
    if fitting and 'modules' in fitting:
        print(f"✓ AI Assistant working: Generated {len(fitting['modules'])} fitting suggestions")
        return True
    else:
        print("✗ AI Assistant failed")
        return False


def test_zkillboard():
    """Test zKillboard client."""
    print("\nTesting zKillboard Client...")
    
    client = ZKillboardClient()
    
    # Test threat analysis for Jita
    threat = client.analyze_system_threat(30000142)
    
    if threat and 'danger_level' in threat:
        print(f"✓ zKillboard Client working: Jita danger level is '{threat['danger_level']}'")
        return True
    else:
        print("✗ zKillboard Client failed")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("EVE Online Mobile App - Component Tests")
    print("=" * 60)
    
    results = {
        'ESI Client': test_esi_client(),
        'Character Manager': test_character_manager(),
        'AI Assistant': test_ai_assistant(),
        'zKillboard Client': test_zkillboard(),
        'Route Planner': test_route_planner(),
    }
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name}: {status}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\nTotal: {passed}/{total} tests passed")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
