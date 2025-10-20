"""Integration tests for complete workflows."""

import sys
from pathlib import Path

# Add packages to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "packages"))

import pytest
from event_contracts.models import Vehicle, WorkPackage, SOPStep, Check, Defect, AccessGrant
from rules_engine import RulesEngine, Policy, Rule, Action


def test_vin_to_install_to_qa_to_access_workflow():
    """Test the complete VIN → Install → QA → Access workflow."""
    
    # Step 1: Vehicle arrives and is scanned
    vehicle = Vehicle(
        vin="1HGCM82633A123456",
        model="Camry",
        color="Silver",
        status="incoming",
        work_package_id="wp_camry_001"
    )
    
    assert vehicle.status == "incoming"
    
    # Step 2: Work package assigned with SOP steps
    work_package = WorkPackage(
        id="wp_camry_001",
        vehicle_model="Camry",
        steps=[
            SOPStep(
                id="step_001",
                type="install",
                description="Install decal",
                sequence_order=1,
                cv_required=True
            ),
            SOPStep(
                id="step_002",
                type="verify",
                description="Torque lug nuts",
                sequence_order=2,
                torque_spec=140.0
            )
        ],
        estimated_duration_minutes=90
    )
    
    assert len(work_package.steps) == 2
    
    # Step 3: Installer completes steps
    checks = []
    for step in work_package.steps:
        check = Check(
            id=f"check_{step.id}_{vehicle.vin}",
            step_id=step.id,
            user_id="installer_001",
            vin=vehicle.vin,
            result="pass",
            artifacts={"completed": True}
        )
        checks.append(check)
    
    assert all(check.result == "pass" for check in checks)
    
    # Step 4: Update vehicle status to install_done
    vehicle.status = "install"  # Would be updated by orchestrator
    
    # Step 5: QA walkaround - no defects found
    defects = []  # Empty list means green
    qa_status = "green"
    
    # Step 6: Check access grant policy
    policy = Policy(
        name="access_control",
        rules=[
            Rule(
                id="grant_start_after_qa",
                conditions={
                    "all": [
                        {"field": "vehicle.status", "operator": "==", "value": "install"},
                        {"field": "qa.status", "operator": "==", "value": "green"},
                        {"field": "defects.count", "operator": "==", "value": 0}
                    ]
                },
                actions=[
                    Action(type="grant", scope="start", ttl_seconds=1800, reason="Install+QA green")
                ]
            )
        ]
    )
    
    engine = RulesEngine(policy)
    context = {
        "vehicle": {"status": "install"},
        "qa": {"status": qa_status},
        "defects": {"count": len(defects)}
    }
    
    decision = engine.evaluate(context)
    
    # Step 7: Verify access is granted
    assert decision.decision == "grant"
    assert decision.actions[0].scope == "start"
    
    # Step 8: Create access grant
    access_grant = AccessGrant(
        vin=vehicle.vin,
        scope="start",
        issued_by="system",
        ttl_seconds=1800,
        reason=decision.reason,
        token="secure_token_123"
    )
    
    assert access_grant.scope == "start"
    assert access_grant.ttl_seconds == 1800


def test_workflow_with_defects_blocks_access():
    """Test that defects block access grants."""
    
    vehicle = Vehicle(
        vin="1HGCM82633A789012",
        model="RAV4",
        color="Blue",
        status="install",
        work_package_id="wp_rav4_001"
    )
    
    # QA finds a defect
    defect = Defect(
        id="defect_001",
        vin=vehicle.vin,
        code="PAINT_SCRATCH",
        description="Scratch on door",
        severity="minor",
        reported_by="qa_user_001"
    )
    
    # Policy blocks access when defects exist
    policy = Policy(
        name="access_control",
        rules=[
            Rule(
                id="grant_start_after_qa",
                priority=10,
                conditions={
                    "all": [
                        {"field": "qa.status", "operator": "==", "value": "green"}
                    ]
                },
                actions=[
                    Action(type="grant", scope="start", ttl_seconds=1800)
                ]
            ),
            Rule(
                id="block_on_defects",
                priority=100,  # Higher priority
                conditions={
                    "all": [
                        {"field": "defects.count", "operator": ">", "value": 0}
                    ]
                },
                actions=[
                    Action(type="deny", scope="start", message="Open defects present")
                ]
            )
        ]
    )
    
    engine = RulesEngine(policy)
    context = {
        "qa": {"status": "green"},
        "defects": {"count": 1}
    }
    
    decision = engine.evaluate(context)
    
    # Access should be denied due to defects
    assert decision.decision == "deny"
    assert "defects" in decision.reason.lower()


def test_hot_unit_expedited_workflow():
    """Test expedited processing for hot units."""
    
    # Hot unit arrives
    vehicle = Vehicle(
        vin="1HGCM82633A111222",
        model="Highlander",
        color="White",
        status="incoming",
        work_package_id="wp_highlander_001",
        customer_priority=True  # Hot unit flag
    )
    
    assert vehicle.customer_priority is True
    
    # Policy grants expedited access for hot units
    policy = Policy(
        name="hot_unit_policy",
        rules=[
            Rule(
                id="hot_unit_priority",
                priority=200,
                conditions={
                    "all": [
                        {"field": "vehicle.customer_priority", "operator": "==", "value": True},
                        {"field": "qa.status", "operator": "==", "value": "green"}
                    ]
                },
                actions=[
                    Action(type="grant", scope="start", ttl_seconds=900, reason="Hot unit - expedited")
                ]
            )
        ]
    )
    
    engine = RulesEngine(policy)
    context = {
        "vehicle": {"customer_priority": True},
        "qa": {"status": "green"}
    }
    
    decision = engine.evaluate(context)
    
    assert decision.decision == "grant"
    assert decision.actions[0].ttl_seconds == 900  # Shorter TTL for hot units
    assert "expedited" in decision.reason.lower()


def test_certification_required_workflow():
    """Test that certifications are checked for operations."""
    
    policy = Policy(
        name="certification_policy",
        rules=[
            Rule(
                id="require_qa_cert",
                conditions={
                    "all": [
                        {"field": "operation.type", "operator": "==", "value": "qa_walkaround"},
                        {"field": "user.certifications", "operator": "not_in", "value": "qa_certified"}
                    ]
                },
                actions=[
                    Action(type="deny", message="QA certification required")
                ]
            )
        ]
    )
    
    engine = RulesEngine(policy)
    
    # User without QA certification
    context = {
        "operation": {"type": "qa_walkaround"},
        "user": {"certifications": ["basic_install"]}
    }
    
    decision = engine.evaluate(context)
    assert decision.decision == "deny"
    
    # User with QA certification - no deny rule triggers
    # In real system, there would be a grant rule too


def test_multi_step_install_tracking():
    """Test tracking progress through multiple install steps."""
    
    vehicle = Vehicle(
        vin="1HGCM82633A555666",
        model="Tacoma",
        color="Gray",
        status="install",
        work_package_id="wp_tacoma_001"
    )
    
    steps = [
        SOPStep(id=f"step_{i}", type="install", description=f"Step {i}", sequence_order=i)
        for i in range(1, 6)
    ]
    
    work_package = WorkPackage(
        id="wp_tacoma_001",
        vehicle_model="Tacoma",
        steps=steps,
        estimated_duration_minutes=120
    )
    
    # Complete steps one by one
    completed_steps = []
    for i, step in enumerate(steps[:3], 1):  # Complete first 3 steps
        check = Check(
            id=f"check_{step.id}",
            step_id=step.id,
            user_id="installer_002",
            vin=vehicle.vin,
            result="pass"
        )
        completed_steps.append(check)
    
    # Calculate progress
    progress_percent = (len(completed_steps) / len(steps)) * 100
    
    assert progress_percent == 60.0  # 3 out of 5 steps
    
    # Policy blocks access until all steps complete
    policy = Policy(
        name="install_progress_policy",
        rules=[
            Rule(
                id="block_during_install",
                conditions={
                    "all": [
                        {"field": "progress.percent", "operator": "<", "value": 100}
                    ]
                },
                actions=[
                    Action(type="deny", message="Installation in progress")
                ]
            )
        ]
    )
    
    engine = RulesEngine(policy)
    context = {"progress": {"percent": progress_percent}}
    
    decision = engine.evaluate(context)
    assert decision.decision == "deny"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
