"""Unit tests for the rules engine."""

import sys
from pathlib import Path

# Add packages to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "packages"))

import pytest
from rules_engine.engine import RulesEngine, PolicyDecision
from rules_engine.policy import Policy, Rule, Condition, Action


def test_simple_grant_rule():
    """Test a simple grant rule."""
    policy = Policy(
        name="test_policy",
        rules=[
            Rule(
                id="grant_on_green",
                conditions={
                    "all": [
                        {"field": "qa.status", "operator": "==", "value": "green"}
                    ]
                },
                actions=[
                    Action(type="grant", scope="start", ttl_seconds=1800, reason="QA green")
                ]
            )
        ]
    )
    
    engine = RulesEngine(policy)
    
    context = {
        "qa": {"status": "green"},
        "vehicle": {"status": "install_done"}
    }
    
    decision = engine.evaluate(context)
    
    assert decision.decision == "grant"
    assert len(decision.actions) == 1
    assert decision.actions[0].scope == "start"


def test_deny_rule_precedence():
    """Test that deny rules take precedence over grant rules."""
    policy = Policy(
        name="test_policy",
        rules=[
            Rule(
                id="grant_on_green",
                priority=10,
                conditions={
                    "all": [
                        {"field": "qa.status", "operator": "==", "value": "green"}
                    ]
                },
                actions=[
                    Action(type="grant", scope="start", ttl_seconds=1800, reason="QA green")
                ]
            ),
            Rule(
                id="deny_on_defects",
                priority=20,
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
        "defects": {"count": 2}
    }
    
    decision = engine.evaluate(context)
    
    assert decision.decision == "deny"
    assert "defects" in decision.reason.lower()


def test_any_conditions():
    """Test 'any' condition logic."""
    policy = Policy(
        name="test_policy",
        rules=[
            Rule(
                id="grant_on_any_green",
                conditions={
                    "any": [
                        {"field": "qa.status", "operator": "==", "value": "green"},
                        {"field": "supervisor.override", "operator": "==", "value": True}
                    ]
                },
                actions=[
                    Action(type="grant", scope="start", ttl_seconds=1800, reason="Approved")
                ]
            )
        ]
    )
    
    engine = RulesEngine(policy)
    
    # Test with supervisor override
    context = {
        "qa": {"status": "red"},
        "supervisor": {"override": True}
    }
    
    decision = engine.evaluate(context)
    assert decision.decision == "grant"


def test_nested_field_access():
    """Test accessing nested fields in context."""
    policy = Policy(
        name="test_policy",
        rules=[
            Rule(
                id="grant_on_nested",
                conditions={
                    "all": [
                        {"field": "vehicle.install.progress.percent", "operator": ">=", "value": 100}
                    ]
                },
                actions=[
                    Action(type="grant", scope="start")
                ]
            )
        ]
    )
    
    engine = RulesEngine(policy)
    
    context = {
        "vehicle": {
            "install": {
                "progress": {
                    "percent": 100
                }
            }
        }
    }
    
    decision = engine.evaluate(context)
    assert decision.decision == "grant"


def test_in_operator():
    """Test 'in' operator for list membership."""
    policy = Policy(
        name="test_policy",
        rules=[
            Rule(
                id="grant_on_status",
                conditions={
                    "all": [
                        {"field": "vehicle.status", "operator": "in", "value": ["install_done", "yard"]}
                    ]
                },
                actions=[
                    Action(type="grant", scope="unlock")
                ]
            )
        ]
    )
    
    engine = RulesEngine(policy)
    
    context = {"vehicle": {"status": "yard"}}
    decision = engine.evaluate(context)
    assert decision.decision == "grant"


def test_no_matching_rules():
    """Test when no rules match."""
    policy = Policy(
        name="test_policy",
        rules=[
            Rule(
                id="grant_on_green",
                conditions={
                    "all": [
                        {"field": "qa.status", "operator": "==", "value": "green"}
                    ]
                },
                actions=[
                    Action(type="grant", scope="start")
                ]
            )
        ]
    )
    
    engine = RulesEngine(policy)
    
    context = {"qa": {"status": "red"}}
    decision = engine.evaluate(context)
    
    # Should deny when no grant rules match
    assert decision.decision == "deny"
    assert "No matching grant rules" in decision.reason


def test_priority_ordering():
    """Test that rules are evaluated by priority."""
    policy = Policy(
        name="test_policy",
        rules=[
            Rule(
                id="low_priority",
                priority=1,
                conditions={
                    "all": [
                        {"field": "test.value", "operator": "==", "value": 1}
                    ]
                },
                actions=[
                    Action(type="grant", scope="test", reason="Low priority")
                ]
            ),
            Rule(
                id="high_priority",
                priority=100,
                conditions={
                    "all": [
                        {"field": "test.value", "operator": "==", "value": 1}
                    ]
                },
                actions=[
                    Action(type="grant", scope="test", reason="High priority")
                ]
            )
        ]
    )
    
    engine = RulesEngine(policy)
    context = {"test": {"value": 1}}
    decision = engine.evaluate(context)
    
    # High priority rule should be evaluated first
    assert decision.matched_rules[0] == "high_priority"


def test_comparison_operators():
    """Test various comparison operators."""
    policy = Policy(
        name="test_policy",
        rules=[
            Rule(
                id="test_gt",
                conditions={
                    "all": [
                        {"field": "value", "operator": ">", "value": 50}
                    ]
                },
                actions=[Action(type="grant", scope="test")]
            )
        ]
    )
    
    engine = RulesEngine(policy)
    
    # Test >
    assert engine.evaluate({"value": 60}).decision == "grant"
    assert engine.evaluate({"value": 40}).decision == "deny"
    
    # Test !=
    policy.rules[0].conditions = {
        "all": [{"field": "value", "operator": "!=", "value": 50}]
    }
    engine = RulesEngine(policy)
    assert engine.evaluate({"value": 40}).decision == "grant"
    assert engine.evaluate({"value": 50}).decision == "deny"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
