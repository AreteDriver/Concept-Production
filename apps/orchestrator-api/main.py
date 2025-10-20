"""FastAPI Orchestrator API for TLS AI/AR system."""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import sys
from pathlib import Path

# Add packages to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "packages"))

from event_contracts.models import (
    Vehicle, WorkPackage, SOPStep, Check, Defect, AccessGrant, User
)
from event_contracts.events import (
    VehicleScannedEvent, SOPStepStartedEvent, SOPStepCompletedEvent,
    QAWalkaroundCompletedEvent, AccessGrantedEvent, DefectEvent
)

app = FastAPI(
    title="TLS Orchestrator API",
    description="API for TLS AI/AR Production System",
    version="0.1.0"
)

security = HTTPBearer()

# In-memory storage (replace with database in production)
vehicles_db: dict[str, Vehicle] = {}
work_packages_db: dict[str, WorkPackage] = {}
checks_db: dict[str, Check] = {}
defects_db: dict[str, Defect] = {}
access_grants_db: dict[str, list[AccessGrant]] = {}
users_db: dict[str, User] = {}


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current authenticated user (stub implementation)."""
    # In production, validate JWT token and return user
    # For now, return a mock user
    return User(
        id="user123",
        name="John Doe",
        role="installer",
        certifications=["basic_install", "torque_certified"]
    )


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "TLS Orchestrator API",
        "version": "0.1.0"
    }


@app.post("/auth/login")
def login(username: str, password: str):
    """Login endpoint (stub implementation)."""
    # In production, validate credentials against SSO/OIDC
    return {
        "access_token": "mock_token_123",
        "token_type": "bearer",
        "expires_in": 3600
    }


@app.get("/vehicles/{vin}", response_model=Vehicle)
def get_vehicle(vin: str, current_user: User = Depends(get_current_user)):
    """Get vehicle status by VIN."""
    if vin not in vehicles_db:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicles_db[vin]


@app.post("/vehicles/{vin}", response_model=Vehicle, status_code=status.HTTP_201_CREATED)
def create_vehicle(vin: str, vehicle: Vehicle, current_user: User = Depends(get_current_user)):
    """Create or register a new vehicle."""
    vehicles_db[vin] = vehicle
    return vehicle


@app.get("/vehicles/{vin}/steps", response_model=list[SOPStep])
def get_vehicle_steps(vin: str, current_user: User = Depends(get_current_user)):
    """Get SOP steps for a vehicle."""
    if vin not in vehicles_db:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    vehicle = vehicles_db[vin]
    if vehicle.work_package_id not in work_packages_db:
        raise HTTPException(status_code=404, detail="Work package not found")
    
    work_package = work_packages_db[vehicle.work_package_id]
    return work_package.steps


@app.post("/steps/{step_id}/complete", response_model=Check)
def complete_step(
    step_id: str,
    vin: str,
    result: str,
    artifacts: dict = {},
    current_user: User = Depends(get_current_user)
):
    """Complete an SOP step."""
    check = Check(
        id=f"check_{step_id}_{vin}",
        step_id=step_id,
        user_id=current_user.id,
        vin=vin,
        result=result,
        artifacts=artifacts
    )
    checks_db[check.id] = check
    return check


@app.post("/qa/{vin}/walkaround", response_model=dict)
def submit_qa_walkaround(
    vin: str,
    defects: list[str] = [],
    photos: list[str] = [],
    overall_status: str = "green",
    current_user: User = Depends(get_current_user)
):
    """Submit QA walkaround results."""
    if vin not in vehicles_db:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    # Update vehicle status
    vehicle = vehicles_db[vin]
    if overall_status == "green":
        vehicle.status = "yard"
    
    return {
        "vin": vin,
        "status": overall_status,
        "defects_count": len(defects),
        "photos_count": len(photos)
    }


@app.post("/access/{vin}/grant", response_model=AccessGrant)
def grant_access(
    vin: str,
    scope: str,
    ttl_seconds: int = 1800,
    reason: str = "Manual grant",
    current_user: User = Depends(get_current_user)
):
    """Grant vehicle access (start/unlock/drive)."""
    if vin not in vehicles_db:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    import secrets
    access_grant = AccessGrant(
        vin=vin,
        scope=scope,
        issued_by=current_user.id,
        ttl_seconds=ttl_seconds,
        reason=reason,
        token=secrets.token_urlsafe(32)
    )
    
    if vin not in access_grants_db:
        access_grants_db[vin] = []
    access_grants_db[vin].append(access_grant)
    
    return access_grant


@app.get("/access/{vin}/check")
def check_access(vin: str, scope: str):
    """Check if vehicle has valid access grant."""
    if vin not in access_grants_db:
        return {"has_access": False, "reason": "No grants found"}
    
    grants = access_grants_db[vin]
    valid_grants = [
        g for g in grants
        if g.scope == scope
    ]
    
    return {
        "has_access": len(valid_grants) > 0,
        "grants": valid_grants
    }


@app.get("/defects/{vin}", response_model=list[Defect])
def get_vehicle_defects(vin: str, current_user: User = Depends(get_current_user)):
    """Get all defects for a vehicle."""
    return [d for d in defects_db.values() if d.vin == vin]


@app.post("/defects", response_model=Defect, status_code=status.HTTP_201_CREATED)
def create_defect(defect: Defect, current_user: User = Depends(get_current_user)):
    """Create a new defect."""
    defects_db[defect.id] = defect
    return defect


@app.get("/work-packages/{package_id}", response_model=WorkPackage)
def get_work_package(package_id: str, current_user: User = Depends(get_current_user)):
    """Get work package definition."""
    if package_id not in work_packages_db:
        raise HTTPException(status_code=404, detail="Work package not found")
    return work_packages_db[package_id]


@app.post("/work-packages", response_model=WorkPackage, status_code=status.HTTP_201_CREATED)
def create_work_package(package: WorkPackage, current_user: User = Depends(get_current_user)):
    """Create a new work package."""
    work_packages_db[package.id] = package
    return package


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
