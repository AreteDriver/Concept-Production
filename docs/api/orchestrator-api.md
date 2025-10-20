# TLS Orchestrator API Specification

**Version:** 0.1.0  
**Base URL:** `http://localhost:8000`  
**Protocol:** HTTP/REST  
**Authentication:** Bearer Token (JWT)

---

## Table of Contents

1. [Authentication](#authentication)
2. [Vehicle Management](#vehicle-management)
3. [SOP Steps](#sop-steps)
4. [QA Operations](#qa-operations)
5. [Access Control](#access-control)
6. [Work Packages](#work-packages)
7. [Defects](#defects)

---

## Authentication

### POST /auth/login

Login to obtain access token.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "expires_in": 3600
}
```

**Status Codes:**
- `200 OK` - Successful login
- `401 Unauthorized` - Invalid credentials

---

## Vehicle Management

### GET /vehicles/{vin}

Get vehicle information and current status.

**Parameters:**
- `vin` (path, required): Vehicle Identification Number (11-17 characters)

**Response:**
```json
{
  "vin": "1HGCM82633A123456",
  "model": "Camry",
  "color": "Silver",
  "status": "install",
  "work_package_id": "wp_001",
  "dock_location": "Dock 1",
  "parking_position": "P125",
  "customer_priority": false,
  "created_at": "2025-10-20T10:00:00Z",
  "updated_at": "2025-10-20T14:30:00Z"
}
```

**Status Codes:**
- `200 OK` - Vehicle found
- `404 Not Found` - Vehicle not registered
- `401 Unauthorized` - Missing or invalid token

### POST /vehicles/{vin}

Register a new vehicle in the system.

**Request Body:**
```json
{
  "vin": "1HGCM82633A123456",
  "model": "Camry",
  "color": "Silver",
  "status": "incoming",
  "work_package_id": "wp_camry_001",
  "dock_location": "Dock 1",
  "parking_position": "P125",
  "customer_priority": false
}
```

**Response:** Same as GET /vehicles/{vin}

**Status Codes:**
- `201 Created` - Vehicle registered
- `400 Bad Request` - Invalid data
- `409 Conflict` - Vehicle already exists

---

## SOP Steps

### GET /vehicles/{vin}/steps

Get SOP steps for a vehicle based on its work package.

**Response:**
```json
[
  {
    "id": "step_001",
    "type": "install",
    "description": "Install window decal",
    "cv_required": true,
    "photo_required": true,
    "torque_spec": null,
    "required_tools": ["squeegee", "spray_bottle"],
    "required_parts": ["decal_123"],
    "cv_template": "decals/window_template.png",
    "pass_criteria": {
      "cv": {
        "iou_threshold": 0.85,
        "skew_deg_max": 2.0
      }
    },
    "sequence_order": 1
  }
]
```

**Status Codes:**
- `200 OK` - Steps retrieved
- `404 Not Found` - Vehicle or work package not found

### POST /steps/{step_id}/complete

Mark an SOP step as complete with results.

**Request Body:**
```json
{
  "vin": "1HGCM82633A123456",
  "result": "pass",
  "artifacts": {
    "photo_uri": "s3://bucket/photo.jpg",
    "torque_nm": 142.0,
    "cv_verification": {
      "iou_score": 0.89,
      "skew_degrees": 1.2
    }
  }
}
```

**Response:**
```json
{
  "id": "check_step_001_1HGCM82633A123456",
  "step_id": "step_001",
  "user_id": "user_123",
  "vin": "1HGCM82633A123456",
  "timestamp": "2025-10-20T14:35:00Z",
  "result": "pass",
  "artifacts": { ... },
  "notes": null
}
```

**Status Codes:**
- `200 OK` - Step completed
- `400 Bad Request` - Invalid result or missing required artifacts
- `404 Not Found` - Step not found

---

## QA Operations

### POST /qa/{vin}/walkaround

Submit QA walkaround inspection results.

**Request Body:**
```json
{
  "defects": ["defect_001", "defect_002"],
  "photos": ["s3://bucket/qa_photo1.jpg", "s3://bucket/qa_photo2.jpg"],
  "overall_status": "green"
}
```

**Response:**
```json
{
  "vin": "1HGCM82633A123456",
  "status": "green",
  "defects_count": 0,
  "photos_count": 5
}
```

**Overall Status Values:**
- `green` - No issues, ready for yard
- `yellow` - Minor issues, can proceed with notes
- `red` - Critical issues, cannot proceed

**Status Codes:**
- `200 OK` - QA submitted
- `404 Not Found` - Vehicle not found

---

## Access Control

### POST /access/{vin}/grant

Grant vehicle access (start/unlock/drive).

**Request Body:**
```json
{
  "scope": "start",
  "ttl_seconds": 1800,
  "reason": "QA passed, all checks complete"
}
```

**Scope Values:**
- `start` - Allow engine start
- `unlock` - Allow door unlock
- `drive` - Allow driving (full access)

**Response:**
```json
{
  "vin": "1HGCM82633A123456",
  "scope": "start",
  "issued_by": "user_123",
  "issued_at": "2025-10-20T14:40:00Z",
  "ttl_seconds": 1800,
  "reason": "QA passed, all checks complete",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Status Codes:**
- `200 OK` - Access granted
- `403 Forbidden` - Policy denies access
- `404 Not Found` - Vehicle not found

### GET /access/{vin}/check

Check if vehicle has valid access grant.

**Query Parameters:**
- `scope` (required): Access scope to check (start/unlock/drive)

**Response:**
```json
{
  "has_access": true,
  "grants": [
    {
      "scope": "start",
      "issued_at": "2025-10-20T14:40:00Z",
      "expires_at": "2025-10-20T15:10:00Z"
    }
  ]
}
```

---

## Work Packages

### GET /work-packages/{package_id}

Get work package definition.

**Response:**
```json
{
  "id": "wp_camry_001",
  "vehicle_model": "Camry",
  "steps": [ ... ],
  "estimated_duration_minutes": 90,
  "required_certifications": ["basic_install", "torque_certified"]
}
```

### POST /work-packages

Create a new work package definition.

**Request Body:**
```json
{
  "id": "wp_camry_002",
  "vehicle_model": "Camry",
  "steps": [ ... ],
  "estimated_duration_minutes": 85,
  "required_certifications": ["basic_install"]
}
```

---

## Defects

### GET /defects/{vin}

Get all defects for a vehicle.

**Response:**
```json
[
  {
    "id": "defect_001",
    "vin": "1HGCM82633A123456",
    "step_id": "step_003",
    "code": "PAINT_SCRATCH",
    "description": "Scratch on rear door",
    "severity": "minor",
    "status": "open",
    "assignee": "user_456",
    "reported_by": "qa_user_001",
    "created_at": "2025-10-20T13:00:00Z",
    "resolved_at": null
  }
]
```

### POST /defects

Create a new defect.

**Request Body:**
```json
{
  "id": "defect_002",
  "vin": "1HGCM82633A123456",
  "code": "DECAL_MISALIGNED",
  "description": "Window decal skewed 3 degrees",
  "severity": "major",
  "reported_by": "qa_user_001"
}
```

**Severity Values:**
- `critical` - Safety or compliance issue
- `major` - Quality issue requiring rework
- `minor` - Cosmetic or documentation issue

---

## Common Response Codes

- `200 OK` - Request successful
- `201 Created` - Resource created
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Missing or invalid authentication
- `403 Forbidden` - Authenticated but not authorized
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource already exists
- `500 Internal Server Error` - Server error

---

## Rate Limiting

- **Rate Limit:** 1000 requests per hour per user
- **Headers:**
  - `X-RateLimit-Limit`: Maximum requests per hour
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Time when limit resets (Unix timestamp)

---

## Interactive API Documentation

When running the orchestrator API locally, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json
