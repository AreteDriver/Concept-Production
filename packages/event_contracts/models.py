"""Core data models for TLS AI/AR system."""

from typing import Literal, Optional
from datetime import datetime
from pydantic import BaseModel, Field, constr


class Vehicle(BaseModel):
    """Vehicle entity representing a unit in the system."""
    vin: constr(min_length=11, max_length=17) = Field(..., description="Vehicle Identification Number")
    model: str = Field(..., description="Vehicle model")
    color: str = Field(..., description="Vehicle color")
    status: Literal['incoming', 'install', 'qa', 'yard', 'shipped'] = Field(
        default='incoming',
        description="Current status of the vehicle"
    )
    work_package_id: str = Field(..., description="Associated work package ID")
    dock_location: Optional[str] = Field(None, description="Dock location (1-4)")
    parking_position: Optional[str] = Field(None, description="Specific parking position")
    customer_priority: bool = Field(default=False, description="Hot unit flag")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class SOPStep(BaseModel):
    """Standard Operating Procedure step definition."""
    id: str = Field(..., description="Unique step identifier")
    type: Literal['install', 'inspect', 'measure', 'verify'] = Field(..., description="Step type")
    description: str = Field(..., description="Step description")
    cv_required: bool = Field(default=False, description="Computer vision verification required")
    photo_required: bool = Field(default=False, description="Photo capture required")
    torque_spec: Optional[float] = Field(None, description="Required torque specification in Nm")
    required_tools: list[str] = Field(default_factory=list, description="Required tools")
    required_parts: list[str] = Field(default_factory=list, description="Required parts")
    cv_template: Optional[str] = Field(None, description="CV template path for verification")
    pass_criteria: dict = Field(default_factory=dict, description="Pass criteria configuration")
    sequence_order: int = Field(..., description="Order in the workflow")


class WorkPackage(BaseModel):
    """Work package defining the complete set of operations for a vehicle."""
    id: str = Field(..., description="Work package identifier")
    vehicle_model: str = Field(..., description="Vehicle model this package applies to")
    steps: list[SOPStep] = Field(default_factory=list, description="List of SOP steps")
    estimated_duration_minutes: int = Field(..., description="Estimated completion time")
    required_certifications: list[str] = Field(default_factory=list, description="Required worker certifications")


class Check(BaseModel):
    """Individual check/verification record."""
    id: str = Field(..., description="Check identifier")
    step_id: str = Field(..., description="Associated SOP step ID")
    user_id: str = Field(..., description="User who performed the check")
    vin: str = Field(..., description="Vehicle VIN")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    result: Literal['pass', 'fail', 'override'] = Field(..., description="Check result")
    artifacts: dict = Field(default_factory=dict, description="Artifacts (photos, torque readings, etc.)")
    notes: Optional[str] = Field(None, description="Additional notes")


class Defect(BaseModel):
    """Defect record for quality tracking."""
    id: str = Field(..., description="Defect identifier")
    vin: str = Field(..., description="Vehicle VIN")
    step_id: Optional[str] = Field(None, description="Related SOP step if applicable")
    code: str = Field(..., description="Defect code")
    description: str = Field(..., description="Defect description")
    severity: Literal['critical', 'major', 'minor'] = Field(..., description="Defect severity")
    status: Literal['open', 'in_progress', 'resolved', 'closed'] = Field(default='open')
    assignee: Optional[str] = Field(None, description="Assigned user ID")
    reported_by: str = Field(..., description="User who reported the defect")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = Field(None)


class AccessGrant(BaseModel):
    """Access grant for vehicle control."""
    vin: str = Field(..., description="Vehicle VIN")
    scope: Literal['start', 'unlock', 'drive'] = Field(..., description="Access scope")
    issued_by: str = Field(..., description="User or system that issued the grant")
    issued_at: datetime = Field(default_factory=datetime.utcnow)
    ttl_seconds: int = Field(..., description="Time to live in seconds")
    reason: str = Field(..., description="Reason for access grant")
    token: str = Field(..., description="Access token")


class User(BaseModel):
    """User/worker in the system."""
    id: str = Field(..., description="User identifier")
    name: str = Field(..., description="User name")
    role: Literal['installer', 'qa', 'yard_driver', 'supervisor', 'admin', 'parts_clerk'] = Field(
        ...,
        description="User role"
    )
    certifications: list[str] = Field(default_factory=list, description="List of certifications")
    active: bool = Field(default=True)


class Device(BaseModel):
    """Device/hardware in the system."""
    id: str = Field(..., description="Device identifier")
    type: Literal['ar_glasses', 'torque_wrench', 'scanner', 'tablet', 'printer'] = Field(
        ...,
        description="Device type"
    )
    firmware_version: str = Field(..., description="Firmware version")
    last_seen: datetime = Field(default_factory=datetime.utcnow)
    status: Literal['active', 'inactive', 'maintenance'] = Field(default='active')
    assigned_to: Optional[str] = Field(None, description="User ID if assigned")


class Part(BaseModel):
    """Parts inventory item."""
    id: str = Field(..., description="Part identifier")
    part_number: str = Field(..., description="Part number")
    description: str = Field(..., description="Part description")
    storage_location: str = Field(..., description="Storage location")
    quantity: int = Field(..., description="Available quantity")
    reserved_quantity: int = Field(default=0, description="Reserved for specific VINs")
    compatible_models: list[str] = Field(default_factory=list, description="Compatible vehicle models")


class YardPosition(BaseModel):
    """Yard/dock parking position."""
    dock_number: Literal['1', '2', '3', '4'] = Field(..., description="Dock number (1-4)")
    position_id: str = Field(..., description="Position identifier within dock")
    capacity: int = Field(default=1, description="Number of vehicles that can fit")
    current_vin: Optional[str] = Field(None, description="Currently parked VIN")
    status: Literal['available', 'occupied', 'reserved', 'maintenance'] = Field(default='available')
