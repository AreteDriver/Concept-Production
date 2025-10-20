"""Unit tests for data models."""

import sys
from pathlib import Path

# Add packages to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "packages"))

import pytest
from datetime import datetime
from event_contracts.models import (
    Vehicle, WorkPackage, SOPStep, Check, Defect, AccessGrant, User, Device, Part, YardPosition
)
from pydantic import ValidationError


def test_vehicle_creation():
    """Test creating a valid vehicle."""
    vehicle = Vehicle(
        vin="1HGCM82633A123456",
        model="Camry",
        color="Silver",
        work_package_id="wp_001"
    )
    
    assert vehicle.vin == "1HGCM82633A123456"
    assert vehicle.status == "incoming"  # Default
    assert vehicle.customer_priority is False  # Default


def test_vehicle_invalid_vin():
    """Test that VIN validation works."""
    with pytest.raises(ValidationError):
        Vehicle(
            vin="SHORT",  # Too short
            model="Camry",
            color="Silver",
            work_package_id="wp_001"
        )


def test_sop_step_creation():
    """Test creating an SOP step."""
    step = SOPStep(
        id="step_001",
        type="install",
        description="Install window decal",
        sequence_order=1,
        cv_required=True,
        photo_required=True,
        required_tools=["squeegee", "spray_bottle"],
        required_parts=["decal_123"]
    )
    
    assert step.id == "step_001"
    assert step.type == "install"
    assert len(step.required_tools) == 2
    assert step.torque_spec is None


def test_sop_step_with_torque():
    """Test SOP step with torque specification."""
    step = SOPStep(
        id="step_002",
        type="verify",
        description="Torque lug nuts",
        sequence_order=2,
        torque_spec=140.0
    )
    
    assert step.torque_spec == 140.0


def test_work_package_creation():
    """Test creating a work package with steps."""
    steps = [
        SOPStep(
            id="step_001",
            type="install",
            description="Step 1",
            sequence_order=1
        ),
        SOPStep(
            id="step_002",
            type="verify",
            description="Step 2",
            sequence_order=2
        )
    ]
    
    package = WorkPackage(
        id="wp_001",
        vehicle_model="Camry",
        steps=steps,
        estimated_duration_minutes=90,
        required_certifications=["basic_install"]
    )
    
    assert len(package.steps) == 2
    assert package.estimated_duration_minutes == 90


def test_check_creation():
    """Test creating a check record."""
    check = Check(
        id="check_001",
        step_id="step_001",
        user_id="user_123",
        vin="1HGCM82633A123456",
        result="pass",
        artifacts={"photo_uri": "s3://bucket/photo.jpg", "torque": 142.0}
    )
    
    assert check.result == "pass"
    assert "photo_uri" in check.artifacts


def test_defect_creation():
    """Test creating a defect."""
    defect = Defect(
        id="defect_001",
        vin="1HGCM82633A123456",
        code="PAINT_SCRATCH",
        description="Scratch on rear door",
        severity="minor",
        reported_by="qa_user_001"
    )
    
    assert defect.severity == "minor"
    assert defect.status == "open"  # Default
    assert defect.resolved_at is None


def test_defect_severity_validation():
    """Test defect severity must be valid."""
    with pytest.raises(ValidationError):
        Defect(
            id="defect_001",
            vin="1HGCM82633A123456",
            code="TEST",
            description="Test",
            severity="invalid",  # Invalid severity
            reported_by="user"
        )


def test_access_grant_creation():
    """Test creating an access grant."""
    grant = AccessGrant(
        vin="1HGCM82633A123456",
        scope="start",
        issued_by="qa_user_001",
        ttl_seconds=1800,
        reason="QA passed",
        token="abc123xyz"
    )
    
    assert grant.scope == "start"
    assert grant.ttl_seconds == 1800


def test_user_creation():
    """Test creating a user."""
    user = User(
        id="user_001",
        name="John Doe",
        role="installer",
        certifications=["basic_install", "torque_certified"]
    )
    
    assert user.role == "installer"
    assert len(user.certifications) == 2
    assert user.active is True  # Default


def test_user_role_validation():
    """Test user role must be valid."""
    with pytest.raises(ValidationError):
        User(
            id="user_001",
            name="John Doe",
            role="invalid_role",  # Invalid role
            certifications=[]
        )


def test_device_creation():
    """Test creating a device."""
    device = Device(
        id="device_001",
        type="torque_wrench",
        firmware_version="1.2.3"
    )
    
    assert device.type == "torque_wrench"
    assert device.status == "active"  # Default


def test_part_creation():
    """Test creating a part."""
    part = Part(
        id="part_001",
        part_number="DECAL-WIN-123",
        description="Window decal",
        storage_location="A-12-3",
        quantity=500,
        compatible_models=["Camry", "RAV4"]
    )
    
    assert part.quantity == 500
    assert part.reserved_quantity == 0  # Default
    assert len(part.compatible_models) == 2


def test_yard_position_creation():
    """Test creating a yard position."""
    position = YardPosition(
        dock_number="1",
        position_id="P001",
        current_vin="1HGCM82633A123456"
    )
    
    assert position.dock_number == "1"
    assert position.status == "available"  # Default even with VIN
    assert position.capacity == 1  # Default


def test_yard_position_dock_validation():
    """Test yard position dock number must be 1-4."""
    with pytest.raises(ValidationError):
        YardPosition(
            dock_number="5",  # Invalid dock number
            position_id="P001"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
