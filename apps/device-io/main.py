"""Device I/O Service for TLS AI/AR system."""

from fastapi import FastAPI, HTTPException, WebSocket
from pydantic import BaseModel
from typing import Optional, Literal
import asyncio
from datetime import datetime

app = FastAPI(
    title="TLS Device I/O Service",
    description="Interface for physical devices: torque wrenches, printers, scanners, gates",
    version="0.1.0"
)


class TorqueReading(BaseModel):
    """Torque wrench reading."""
    device_id: str
    value_nm: float
    timestamp: datetime = None
    unit: str = "Nm"
    
    def __init__(self, **data):
        if data.get('timestamp') is None:
            data['timestamp'] = datetime.utcnow()
        super().__init__(**data)


class PrintJob(BaseModel):
    """Label print job."""
    printer_id: str
    label_template: str
    data: dict
    copies: int = 1


class GateCommand(BaseModel):
    """Gate/door control command."""
    gate_id: str
    action: Literal['open', 'close', 'lock', 'unlock']
    duration_seconds: Optional[int] = None


class ScanResult(BaseModel):
    """Barcode/RFID scan result."""
    scanner_id: str
    scan_type: Literal['barcode', 'qr', 'rfid', 'vin']
    value: str
    timestamp: datetime = None
    
    def __init__(self, **data):
        if data.get('timestamp') is None:
            data['timestamp'] = datetime.utcnow()
        super().__init__(**data)


# In-memory device registry
devices = {}
active_connections = {}


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "TLS Device I/O Service",
        "version": "0.1.0",
        "devices_connected": len(devices),
        "capabilities": ["torque_wrench", "label_printer", "gate_control", "scanner"]
    }


@app.get("/devices")
def list_devices():
    """List all connected devices."""
    return {
        "devices": list(devices.values()),
        "count": len(devices)
    }


@app.get("/devices/{device_id}")
def get_device(device_id: str):
    """Get device information."""
    if device_id not in devices:
        raise HTTPException(status_code=404, detail="Device not found")
    return devices[device_id]


@app.post("/devices/{device_id}/register")
def register_device(
    device_id: str,
    device_type: str,
    firmware_version: str = "unknown"
):
    """Register a new device."""
    devices[device_id] = {
        "id": device_id,
        "type": device_type,
        "firmware_version": firmware_version,
        "status": "active",
        "last_seen": datetime.utcnow().isoformat()
    }
    return {"message": "Device registered", "device": devices[device_id]}


@app.websocket("/devices/{device_id}/stream")
async def device_stream(websocket: WebSocket, device_id: str):
    """WebSocket stream for real-time device data."""
    await websocket.accept()
    active_connections[device_id] = websocket
    
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back for now - in production, route to event bus
            await websocket.send_text(f"Received from {device_id}: {data}")
    except Exception as e:
        print(f"WebSocket error for {device_id}: {e}")
    finally:
        if device_id in active_connections:
            del active_connections[device_id]


@app.post("/torque/read", response_model=TorqueReading)
async def read_torque(device_id: str, step_id: str):
    """
    Read torque value from a torque wrench.
    
    In production, this would:
    1. Connect to device via BLE
    2. Request current reading
    3. Validate against spec
    4. Emit telemetry event
    """
    # Mock implementation
    import random
    
    mock_torque = random.uniform(130, 150)
    
    reading = TorqueReading(
        device_id=device_id,
        value_nm=mock_torque
    )
    
    return reading


@app.post("/torque/calibrate")
async def calibrate_torque_wrench(device_id: str):
    """Calibrate a torque wrench."""
    if device_id not in devices:
        raise HTTPException(status_code=404, detail="Device not found")
    
    # Mock calibration
    return {
        "device_id": device_id,
        "calibrated": True,
        "calibration_date": datetime.utcnow().isoformat(),
        "next_calibration_due": "2025-01-20"
    }


@app.post("/printer/print", response_model=dict)
async def print_label(job: PrintJob):
    """
    Print a label using ZPL printer.
    
    In production:
    1. Generate ZPL from template + data
    2. Send to printer via serial/network
    3. Confirm print completion
    """
    # Mock implementation
    return {
        "job_id": f"print_{job.printer_id}_{datetime.utcnow().timestamp()}",
        "printer_id": job.printer_id,
        "status": "completed",
        "copies_printed": job.copies
    }


@app.get("/printer/{printer_id}/status")
def get_printer_status(printer_id: str):
    """Get printer status."""
    return {
        "printer_id": printer_id,
        "status": "ready",
        "paper_level": "good",
        "ribbon_level": "good",
        "errors": []
    }


@app.post("/gate/control")
async def control_gate(command: GateCommand):
    """
    Control gate/door access.
    
    In production:
    1. Validate access token
    2. Send relay command
    3. Monitor sensor feedback
    4. Log access event
    """
    # Mock implementation
    return {
        "gate_id": command.gate_id,
        "action": command.action,
        "status": "success",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/scanner/scan", response_model=ScanResult)
async def scan_code(scanner_id: str, scan_type: str = "barcode"):
    """
    Trigger a scan or retrieve last scan.
    
    In production, this would interface with scanner hardware
    via USB/Serial/Bluetooth.
    """
    # Mock implementation
    mock_vin = "1HGCM82633A123456"
    
    result = ScanResult(
        scanner_id=scanner_id,
        scan_type=scan_type,
        value=mock_vin
    )
    
    return result


@app.get("/scanner/{scanner_id}/status")
def get_scanner_status(scanner_id: str):
    """Get scanner status."""
    return {
        "scanner_id": scanner_id,
        "status": "ready",
        "battery_level": 85,
        "last_scan": "2 minutes ago"
    }


@app.post("/devices/{device_id}/heartbeat")
async def device_heartbeat(device_id: str):
    """Update device heartbeat."""
    if device_id in devices:
        devices[device_id]["last_seen"] = datetime.utcnow().isoformat()
        devices[device_id]["status"] = "active"
    else:
        raise HTTPException(status_code=404, detail="Device not registered")
    
    return {"status": "ok", "device_id": device_id}


@app.post("/devices/{device_id}/alert")
async def device_alert(device_id: str, message: str, severity: str = "info"):
    """Send alert from device."""
    alert = {
        "device_id": device_id,
        "message": message,
        "severity": severity,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # In production, publish to event bus
    print(f"ALERT: {alert}")
    
    return alert


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
