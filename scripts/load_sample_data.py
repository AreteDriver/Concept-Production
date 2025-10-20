#!/usr/bin/env python3
"""Script to load sample work packages and SOPs into the system."""

import sys
from pathlib import Path
import yaml
import requests

# Add packages to path
sys.path.insert(0, str(Path(__file__).parent.parent / "packages"))

from event_contracts.models import WorkPackage, SOPStep, Vehicle


def load_sop_from_yaml(yaml_path: Path) -> SOPStep:
    """Load an SOP step from YAML file."""
    with open(yaml_path) as f:
        data = yaml.safe_load(f)
    
    # Map YAML structure to SOPStep model
    return SOPStep(
        id=data['id'],
        type=data['type'],
        description=data['description'],
        sequence_order=data.get('sequence_order', 1),
        cv_required=data.get('inputs', {}).get('cv_required', False),
        photo_required=data.get('inputs', {}).get('photo_required', False),
        torque_spec=data.get('inputs', {}).get('torque_spec_nm'),
        required_tools=data.get('requires', {}).get('tools', []),
        required_parts=data.get('requires', {}).get('parts', []),
        cv_template=data.get('inputs', {}).get('cv_template'),
        pass_criteria=data.get('pass_criteria', {})
    )


def create_sample_work_packages():
    """Create sample work packages for different vehicle models."""
    
    sop_dir = Path(__file__).parent.parent / "docs" / "sop"
    
    # Load SOPs
    sops = []
    if sop_dir.exists():
        for yaml_file in sop_dir.glob("*.yaml"):
            try:
                sop = load_sop_from_yaml(yaml_file)
                sops.append(sop)
                print(f"✓ Loaded SOP: {sop.id}")
            except Exception as e:
                print(f"✗ Failed to load {yaml_file}: {e}")
    
    # Create work packages for different models
    work_packages = [
        WorkPackage(
            id="wp_camry_standard",
            vehicle_model="Camry",
            steps=sops,
            estimated_duration_minutes=90,
            required_certifications=["basic_install", "torque_certified"]
        ),
        WorkPackage(
            id="wp_rav4_standard",
            vehicle_model="RAV4",
            steps=sops,
            estimated_duration_minutes=95,
            required_certifications=["basic_install", "torque_certified"]
        ),
        WorkPackage(
            id="wp_tacoma_standard",
            vehicle_model="Tacoma",
            steps=sops,
            estimated_duration_minutes=110,
            required_certifications=["basic_install", "torque_certified", "truck_certified"]
        ),
    ]
    
    return work_packages


def create_sample_vehicles():
    """Create sample vehicles for testing."""
    return [
        Vehicle(
            vin="1HGCM82633A123456",
            model="Camry",
            color="Silver",
            status="incoming",
            work_package_id="wp_camry_standard",
            dock_location="Dock 1",
            parking_position="P125",
            customer_priority=False
        ),
        Vehicle(
            vin="2T3RFREV5JW123456",
            model="RAV4",
            color="Blue",
            status="incoming",
            work_package_id="wp_rav4_standard",
            dock_location="Dock 2",
            parking_position="P089",
            customer_priority=True  # Hot unit
        ),
        Vehicle(
            vin="5TFUY5F18NX123456",
            model="Tacoma",
            color="Black",
            status="incoming",
            work_package_id="wp_tacoma_standard",
            dock_location="Dock 3",
            parking_position="P042",
            customer_priority=False
        ),
    ]


def post_to_api(endpoint: str, data: dict, api_base: str = "http://localhost:8000"):
    """Post data to API endpoint."""
    url = f"{api_base}{endpoint}"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        print(f"✓ Posted to {endpoint}: {response.status_code}")
        return response.json()
    except requests.exceptions.ConnectionError:
        print(f"✗ Could not connect to API at {api_base}")
        print("  Make sure the orchestrator API is running:")
        print("  cd apps/orchestrator-api && python main.py")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"✗ HTTP error posting to {endpoint}: {e}")
        return None


def main():
    """Main function to load sample data."""
    print("=" * 60)
    print("Loading Sample Data for TLS AI/AR System")
    print("=" * 60)
    
    # Check if API is available
    api_base = "http://localhost:8000"
    try:
        response = requests.get(api_base)
        if response.status_code == 200:
            print(f"✓ API is running at {api_base}")
        else:
            print(f"✗ API returned status {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print(f"✗ API is not running at {api_base}")
        print("  Start it with: cd apps/orchestrator-api && python main.py")
        print("\nGenerating data files for manual loading...")
        
        # Generate JSON files instead
        work_packages = create_sample_work_packages()
        vehicles = create_sample_vehicles()
        
        output_dir = Path(__file__).parent.parent / "data" / "sample"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        import json
        
        # Save work packages
        for wp in work_packages:
            wp_file = output_dir / f"{wp.id}.json"
            with open(wp_file, 'w') as f:
                json.dump(wp.model_dump(), f, indent=2, default=str)
            print(f"✓ Saved work package: {wp_file}")
        
        # Save vehicles
        for vehicle in vehicles:
            v_file = output_dir / f"vehicle_{vehicle.vin}.json"
            with open(v_file, 'w') as f:
                json.dump(vehicle.model_dump(), f, indent=2, default=str)
            print(f"✓ Saved vehicle: {v_file}")
        
        print(f"\n✓ Sample data saved to {output_dir}")
        return
    
    print("\n" + "=" * 60)
    print("Loading Work Packages")
    print("=" * 60)
    
    work_packages = create_sample_work_packages()
    for wp in work_packages:
        result = post_to_api("/work-packages", wp.model_dump(mode='json'))
        if result:
            print(f"  → Work package {wp.id} created for {wp.vehicle_model}")
    
    print("\n" + "=" * 60)
    print("Loading Sample Vehicles")
    print("=" * 60)
    
    vehicles = create_sample_vehicles()
    for vehicle in vehicles:
        result = post_to_api(f"/vehicles/{vehicle.vin}", vehicle.model_dump(mode='json'))
        if result:
            priority = "🔥 HOT UNIT" if vehicle.customer_priority else ""
            print(f"  → Vehicle {vehicle.vin} ({vehicle.model}) {priority}")
    
    print("\n" + "=" * 60)
    print("✓ Sample data loaded successfully!")
    print("=" * 60)
    print("\nAccess the API at:")
    print(f"  • Interactive docs: {api_base}/docs")
    print(f"  • API endpoint: {api_base}/")
    print("\nAccess the dashboards:")
    print("  • Supervisor: streamlit run apps/dashboards/supervisor_dashboard.py")
    print("  • Logistics: streamlit run apps/dashboards/logistics_planner.py")


if __name__ == "__main__":
    main()
