"""Rules engine implementation for evaluating policies."""

from typing import Any, Literal
from pydantic import BaseModel, Field
from .policy import Policy, Rule, Condition, Action


class PolicyDecision(BaseModel):
    """Result of policy evaluation."""
    decision: Literal['grant', 'deny'] = Field(..., description="Final decision")
    matched_rules: list[str] = Field(default_factory=list, description="IDs of matched rules")
    actions: list[Action] = Field(default_factory=list, description="Actions to execute")
    reason: str = Field(..., description="Reason for decision")


class RulesEngine:
    """Rules engine for evaluating policies against context."""
    
    def __init__(self, policy: Policy):
        """Initialize with a policy."""
        self.policy = policy
        # Sort rules by priority (higher first)
        self.policy.rules.sort(key=lambda r: r.priority, reverse=True)
    
    def evaluate(self, context: dict[str, Any]) -> PolicyDecision:
        """
        Evaluate policy against context.
        
        Args:
            context: Dictionary containing vehicle, qa, defects, user, etc.
            
        Returns:
            PolicyDecision with grant/deny and actions
        """
        matched_rules = []
        all_actions = []
        
        for rule in self.policy.rules:
            if self._evaluate_rule(rule, context):
                matched_rules.append(rule.id)
                all_actions.extend(rule.actions)
        
        # Determine final decision - deny takes precedence
        deny_actions = [a for a in all_actions if a.type == 'deny']
        grant_actions = [a for a in all_actions if a.type == 'grant']
        
        if deny_actions:
            return PolicyDecision(
                decision='deny',
                matched_rules=matched_rules,
                actions=deny_actions,
                reason=deny_actions[0].message or "Access denied by policy"
            )
        elif grant_actions:
            return PolicyDecision(
                decision='grant',
                matched_rules=matched_rules,
                actions=grant_actions,
                reason=grant_actions[0].reason or "Access granted by policy"
            )
        else:
            return PolicyDecision(
                decision='deny',
                matched_rules=matched_rules,
                actions=[],
                reason="No matching grant rules"
            )
    
    def _evaluate_rule(self, rule: Rule, context: dict[str, Any]) -> bool:
        """Evaluate if a rule matches the context."""
        conditions = rule.conditions
        
        if 'all' in conditions:
            # All conditions must match
            return all(
                self._evaluate_condition(cond, context)
                for cond in conditions['all']
            )
        elif 'any' in conditions:
            # Any condition must match
            return any(
                self._evaluate_condition(cond, context)
                for cond in conditions['any']
            )
        else:
            return False
    
    def _evaluate_condition(self, condition: dict, context: dict[str, Any]) -> bool:
        """Evaluate a single condition."""
        field_path = condition.get('field', '')
        operator = condition.get('operator', '==')
        expected_value = condition.get('value')
        
        # Navigate nested context using field path
        actual_value = self._get_nested_value(context, field_path)
        
        # Evaluate based on operator
        if operator == '==':
            return actual_value == expected_value
        elif operator == '!=':
            return actual_value != expected_value
        elif operator == '>':
            return actual_value > expected_value
        elif operator == '<':
            return actual_value < expected_value
        elif operator == '>=':
            return actual_value >= expected_value
        elif operator == '<=':
            return actual_value <= expected_value
        elif operator == 'in':
            return actual_value in expected_value
        elif operator == 'not_in':
            # Check if expected_value is not in actual_value (e.g., cert not in list of certs)
            if isinstance(actual_value, list):
                return expected_value not in actual_value
            else:
                return actual_value not in expected_value
        elif operator == 'contains':
            return expected_value in actual_value
        else:
            return False
    
    def _get_nested_value(self, data: dict, path: str) -> Any:
        """Get value from nested dictionary using dot notation."""
        keys = path.split('.')
        value = data
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return None
                
        return value
