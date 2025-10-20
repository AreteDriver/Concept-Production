"""Event schemas for the TLS AI/AR system event bus."""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class BaseEvent(BaseModel):
    """Base event with common fields."""
    event_id: str = Field(..., description="Unique event identifier")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    event_type: str = Field(..., description="Type of event")


class VehicleScannedEvent(BaseEvent):
    """Event: vehicle.scanned - VIN scanned at a location."""
    event_type: str = Field(default="vehicle.scanned")
    vin: str = Field(..., description="Vehicle VIN")
    user_id: str = Field(..., description="User who scanned")
    location: str = Field(..., description="Scan location")
    device_id: str = Field(..., description="Device used for scanning")


class SOPStepStartedEvent(BaseEvent):
    """Event: sop.step.started - SOP step initiated."""
    event_type: str = Field(default="sop.step.started")
    vin: str = Field(..., description="Vehicle VIN")
    step_id: str = Field(..., description="SOP step ID")
    user_id: str = Field(..., description="User performing step")
    device_id: str = Field(..., description="Device being used")


class SOPStepCompletedEvent(BaseEvent):
    """Event: sop.step.completed - SOP step completed with results."""
    event_type: str = Field(default="sop.step.completed")
    vin: str = Field(..., description="Vehicle VIN")
    step_id: str = Field(..., description="SOP step ID")
    user_id: str = Field(..., description="User who completed step")
    result: str = Field(..., description="Result: pass/fail/override")
    artifacts: dict = Field(default_factory=dict, description="Photos, readings, etc.")
    duration_seconds: float = Field(..., description="Time taken to complete")


class QAWalkaroundCompletedEvent(BaseEvent):
    """Event: qa.walkaround.completed - QA walkaround inspection done."""
    event_type: str = Field(default="qa.walkaround.completed")
    vin: str = Field(..., description="Vehicle VIN")
    user_id: str = Field(..., description="QA inspector")
    defects: list[str] = Field(default_factory=list, description="List of defect IDs found")
    photos: list[str] = Field(default_factory=list, description="Photo URIs")
    overall_status: str = Field(..., description="green/yellow/red")


class AccessGrantedEvent(BaseEvent):
    """Event: access.granted - Vehicle access granted."""
    event_type: str = Field(default="access.granted")
    vin: str = Field(..., description="Vehicle VIN")
    scope: str = Field(..., description="start/unlock/drive")
    issued_by: str = Field(..., description="User or system")
    ttl_seconds: int = Field(..., description="Time to live")
    reason: str = Field(..., description="Grant reason")
    token: str = Field(..., description="Access token")


class DefectEvent(BaseEvent):
    """Event: defect.opened|updated|closed - Defect lifecycle event."""
    event_type: str = Field(default="defect.opened")
    defect_id: str = Field(..., description="Defect ID")
    vin: str = Field(..., description="Vehicle VIN")
    code: str = Field(..., description="Defect code")
    severity: str = Field(..., description="critical/major/minor")
    status: str = Field(..., description="open/in_progress/resolved/closed")
    user_id: str = Field(..., description="User involved in the event")


class TelemetryTorqueEvent(BaseEvent):
    """Event: telemetry.torque.captured - Torque wrench reading captured."""
    event_type: str = Field(default="telemetry.torque.captured")
    vin: str = Field(..., description="Vehicle VIN")
    step_id: str = Field(..., description="SOP step ID")
    user_id: str = Field(..., description="User performing torque")
    device_id: str = Field(..., description="Torque wrench device ID")
    value_nm: float = Field(..., description="Measured torque in Newton-meters")
    spec_nm: float = Field(..., description="Required torque specification")
    within_tolerance: bool = Field(..., description="Whether reading is within acceptable range")


class PartScannedEvent(BaseEvent):
    """Event: part.scanned - Part scanned for check-in or verification."""
    event_type: str = Field(default="part.scanned")
    part_number: str = Field(..., description="Part number")
    location: str = Field(..., description="Storage location")
    user_id: str = Field(..., description="User who scanned")
    quantity: int = Field(default=1, description="Quantity scanned")
    associated_vin: Optional[str] = Field(None, description="VIN if part is being assigned")


class YardMovementEvent(BaseEvent):
    """Event: yard.movement - Vehicle moved in yard."""
    event_type: str = Field(default="yard.movement")
    vin: str = Field(..., description="Vehicle VIN")
    from_location: str = Field(..., description="Previous location")
    to_location: str = Field(..., description="New location")
    driver_id: str = Field(..., description="Yard driver")
    reason: str = Field(..., description="Movement reason")
