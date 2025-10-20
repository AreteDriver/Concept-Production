"""Policy definitions for the rules engine."""

from typing import Any, Literal, Optional
from pydantic import BaseModel, Field


class Condition(BaseModel):
    """A condition to evaluate in a rule."""
    field: str = Field(..., description="Field path to evaluate (e.g., 'vehicle.status')")
    operator: Literal['==', '!=', '>', '<', '>=', '<=', 'in', 'not_in', 'contains'] = Field(
        ...,
        description="Comparison operator"
    )
    value: Any = Field(..., description="Value to compare against")


class Action(BaseModel):
    """Action to take when rule matches."""
    type: Literal['grant', 'deny', 'alert', 'log'] = Field(..., description="Action type")
    scope: Optional[str] = Field(None, description="Scope for grant/deny (e.g., 'start', 'unlock', 'drive')")
    ttl_seconds: Optional[int] = Field(None, description="TTL for grants")
    reason: Optional[str] = Field(None, description="Reason for action")
    message: Optional[str] = Field(None, description="Message to display")


class Rule(BaseModel):
    """A single rule in a policy."""
    id: str = Field(..., description="Unique rule identifier")
    description: Optional[str] = Field(None, description="Human-readable description")
    conditions: dict = Field(..., description="Conditions (all/any with list of Condition)")
    actions: list[Action] = Field(..., description="Actions to take when conditions match")
    priority: int = Field(default=0, description="Rule priority (higher = evaluated first)")


class Policy(BaseModel):
    """A policy containing multiple rules."""
    version: str = Field(default="v1", description="Policy version")
    name: str = Field(..., description="Policy name")
    description: Optional[str] = Field(None, description="Policy description")
    rules: list[Rule] = Field(default_factory=list, description="List of rules")
