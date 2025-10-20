# TLS AI/AR Production System - System Overview

**Version:** 0.1.0 - Pilot Phase  
**Date:** October 2025  
**Organization:** Toyota Logistics Services - Portland VDC

---

## Executive Summary

The TLS AI/AR Production System is a comprehensive platform that integrates artificial intelligence, augmented reality, and IoT devices to enhance vehicle processing operations. The system manages the complete workflow from vehicle arrival through installation, quality assurance, and yard logistics.

### Key Capabilities

✅ **140,000+ VIN Management** - Track vehicles across 4 docks (2,500 units each)  
✅ **AI-Guided Workflows** - Step-by-step AR guidance for installers  
✅ **Computer Vision QA** - Automated quality verification using CV  
✅ **Policy-Based Access Control** - Declarative rules for vehicle access  
✅ **Real-Time Analytics** - KPI dashboards for supervisors  
✅ **Intelligent Logistics** - Optimize yard operations and throughput  

---

## System Architecture

### High-Level Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     User Interface Layer                      │
│  ┌───────────┐  ┌────────────┐  ┌──────────────────────┐    │
│  │ AR Client │  │ Dashboards │  │ Mobile/Web Interface │    │
│  └─────┬─────┘  └──────┬─────┘  └──────────┬───────────┘    │
└────────┼────────────────┼────────────────────┼───────────────┘
         │                │                    │
┌────────┼────────────────┼────────────────────┼───────────────┐
│        │    Application Services Layer       │               │
│        └──────────┬──────────────────────────┘               │
│                   ▼                                           │
│        ┌──────────────────────┐                              │
│        │  API Orchestrator    │  (FastAPI - Port 8000)       │
│        │  - Vehicle Mgmt      │                              │
│        │  - SOP Steps         │                              │
│        │  - QA Operations     │                              │
│        │  - Access Control    │                              │
│        └──────────┬───────────┘                              │
│                   │                                           │
│        ┌──────────┴──────────┬──────────────┬───────────┐   │
│        ▼                     ▼              ▼           ▼   │
│  ┌──────────┐      ┌──────────────┐  ┌───────────┐  ┌──────┐
│  │ CV       │      │ Rules Engine │  │ Device    │  │Event │
│  │ Service  │      │ (Policies)   │  │ I/O       │  │ Bus  │
│  │ :8001    │      │              │  │ :8002     │  │      │
│  └──────────┘      └──────────────┘  └───────────┘  └──────┘
└─────────────────────────────────────────────────────────────┘
         │                     │              │           │
┌────────┼─────────────────────┼──────────────┼───────────┼───┐
│        │       Data Layer                   │           │   │
│        ▼                                    ▼           ▼   │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │  Vehicle DB  │  │  Events DB   │  │  Analytics DB   │  │
│  │  Parts DB    │  │  Audit Log   │  │  KPI Tables     │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. API Orchestrator
- **Technology:** FastAPI, Python 3.11+
- **Port:** 8000
- **Purpose:** Central coordination of all operations
- **Features:**
  - Vehicle registration and tracking
  - SOP step management
  - QA walkaround coordination
  - Access grant/deny decisions
  - Work package management
  - Defect tracking

#### 2. Rules Engine
- **Technology:** Python, YAML policies
- **Purpose:** Policy-based decision making
- **Features:**
  - Declarative rule definitions
  - Context-based evaluation
  - Priority-based rule ordering
  - Multiple condition types (all/any)
  - Grant/deny/alert actions

#### 3. Computer Vision Service
- **Technology:** OpenCV, FastAPI
- **Port:** 8001
- **Purpose:** Visual verification and detection
- **Features:**
  - VIN OCR (barcode reading)
  - Part presence detection
  - Decal alignment verification
  - Damage detection (V2)
  - Template matching

#### 4. Device I/O Service
- **Technology:** FastAPI, BLE, Serial
- **Port:** 8002
- **Purpose:** Hardware device interface
- **Features:**
  - Torque wrench integration
  - Label printer (ZPL)
  - Barcode/RFID scanners
  - Gate/door control
  - Device heartbeat monitoring

#### 5. Dashboards
- **Technology:** Streamlit, Plotly
- **Purpose:** Real-time monitoring and planning
- **Components:**
  - **Supervisor Dashboard**
    - Cycle time metrics
    - First-time-through rate
    - Defects tracking
    - Active vehicles status
    - Labor & capacity
  - **Logistics Planner**
    - Dock allocation
    - Incoming vehicle management
    - Resource optimization
    - Daily production planning
    - Parts inventory

---

## Data Models

### Core Entities

#### Vehicle
```python
{
  "vin": "1HGCM82633A123456",
  "model": "Camry",
  "color": "Silver",
  "status": "install|qa|yard|shipped",
  "work_package_id": "wp_001",
  "dock_location": "Dock 1",
  "parking_position": "P125",
  "customer_priority": false
}
```

#### WorkPackage
```python
{
  "id": "wp_camry_001",
  "vehicle_model": "Camry",
  "steps": [SOPStep...],
  "estimated_duration_minutes": 90,
  "required_certifications": ["basic_install", "torque_certified"]
}
```

#### SOPStep
```python
{
  "id": "step_001",
  "type": "install|inspect|measure|verify",
  "description": "Install window decal",
  "cv_required": true,
  "photo_required": true,
  "torque_spec": null,
  "required_tools": ["squeegee", "spray_bottle"],
  "required_parts": ["decal_123"],
  "pass_criteria": {...}
}
```

#### Check
```python
{
  "id": "check_001",
  "step_id": "step_001",
  "user_id": "user_123",
  "vin": "1HGCM82633A123456",
  "result": "pass|fail|override",
  "artifacts": {
    "photo_uri": "s3://bucket/photo.jpg",
    "torque_nm": 142.0
  }
}
```

#### Defect
```python
{
  "id": "defect_001",
  "vin": "1HGCM82633A123456",
  "code": "PAINT_SCRATCH",
  "severity": "critical|major|minor",
  "status": "open|in_progress|resolved|closed"
}
```

---

## Key Workflows

### 1. VIN → Install → QA → Access (Primary Workflow)

```
┌─────────────────┐
│ 1. Scan VIN     │
│    Barcode      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. Load Work    │
│    Package      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. Pre-flight   │
│    Checks       │
│  - Parts Ready  │
│  - Tools Avail  │
│  - Certs Valid  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. Guided       │
│    Install      │
│  Step-by-step   │
│  with AR        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 5. Capture      │
│    Evidence     │
│  - Photos       │
│  - Torque       │
│  - CV Check     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 6. QA           │
│    Walkaround   │
│  - Checklist    │
│  - Photos       │
│  - Defects      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 7. Rules        │
│    Engine       │
│  Evaluate       │
│  Context        │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐ ┌───────┐
│ GRANT │ │ DENY  │
│ Access│ │ Access│
└───────┘ └───────┘
```

### 2. Parts Department Workflow

```
Scan Part → AR Shows Location → Place in Storage → Update Inventory → Associate with VIN (if allocated)
```

### 3. Logistics Planning Workflow

```
Bulk VIN Import → Analyze (Priority, Parts, Labor) → Assign Dock/Position → Schedule Shuttle → Track Progress
```

---

## Security & Access Control

### Authentication
- SSO/OIDC integration (stub in V1)
- JWT tokens for API access
- Role-based access control

### Roles
- **Installer** - Perform installations
- **QA** - Quality inspections
- **Yard Driver** - Move vehicles
- **Supervisor** - Monitor operations
- **Admin** - System configuration
- **Parts Clerk** - Manage inventory

### Policy-Based Access
Vehicle access (start/unlock/drive) is controlled by policies:
- All install steps complete
- QA status green
- No open defects
- Required certifications present
- Hot unit priority handling

---

## Key Performance Indicators

### Production Metrics
- **Cycle Time** - Average time per vehicle (Target: 70 min)
- **Throughput** - Units per day (Target: 200/day)
- **First-Time-Through Rate** - % passing without rework (Target: >90%)
- **Rework Rate** - % requiring corrections

### Quality Metrics
- **Defects per 100 Vehicles** - Overall quality indicator
- **Defects by Category** - Paint, Decal, Torque, etc.
- **CV Verification Rate** - % of steps with CV checks

### Resource Metrics
- **Labor Utilization** - Active workers vs. capacity
- **Certification Coverage** - Certified vs. required
- **Dock Utilization** - Occupied vs. total capacity (10,000 units)
- **Parts Availability** - In stock vs. reserved

---

## Technology Stack

### Backend
- **Python 3.11+** - Primary language
- **FastAPI** - REST API framework
- **Pydantic** - Data validation
- **OpenCV** - Computer vision
- **PyYAML** - Configuration

### Frontend
- **Streamlit** - Dashboards and analytics
- **Plotly** - Interactive visualizations
- **AR Client** - HoloLens/Android XR (future)

### Data
- **In-Memory** - V1 pilot (dict-based)
- **PostgreSQL** - V2 production (future)
- **Redis** - Caching (future)
- **Kafka** - Event streaming (future)

### DevOps
- **GitHub Actions** - CI/CD
- **Docker** - Containerization (in progress)
- **Kubernetes** - Orchestration (future)
- **Terraform** - Infrastructure as code (future)

---

## Deployment

### Development (Current)
- Local Python services on different ports
- In-memory data storage
- Mock device implementations
- Streamlit dashboards

### Production (Future)
- Kubernetes cluster
- PostgreSQL + Redis
- MQTT broker for devices
- S3 for artifacts
- Kafka for events
- Load balancers
- Auto-scaling

---

## Testing Strategy

### Unit Tests
- Data model validation
- Rules engine logic
- Policy evaluation
- API endpoint handlers

### Integration Tests
- Complete workflow scenarios
- Cross-service communication
- Event handling
- Database operations

### End-to-End Tests (Future)
- Full system workflows
- AR client integration
- Hardware device interactions
- Performance testing

---

## Future Enhancements

### Phase 2 - Production Expansion
- [ ] Database persistence
- [ ] Real device integration
- [ ] Event bus (Kafka/NATS)
- [ ] AR client application
- [ ] Multiple production lines

### Phase 3 - Advanced Features
- [ ] ML-based damage detection
- [ ] Predictive maintenance
- [ ] Automated scheduling
- [ ] Advanced telematics
- [ ] Warranty integration

### Phase 4 - Optimization
- [ ] AI-driven logistics optimization
- [ ] Dynamic resource allocation
- [ ] Real-time bottleneck detection
- [ ] Continuous learning from data

---

## Success Metrics

### Pilot Success Criteria
- [x] System stable ≥95% uptime
- [x] All tests passing
- [x] Core workflows functional
- [ ] 1 production line deployed
- [ ] Daily throughput goal met

### Production Success Criteria
- [ ] 3+ production lines operational
- [ ] 200+ units/day throughput
- [ ] <5% rework rate
- [ ] 90%+ FTT rate
- [ ] <0.5 defects per 100 vehicles

---

## Support & Maintenance

### Monitoring
- Service health checks
- API latency tracking
- Error rate monitoring
- Resource utilization

### Logging
- Structured JSON logs
- Centralized log aggregation
- Audit trail for all operations
- Event sourcing for replay

### Backup & Recovery
- Database backups (hourly)
- Configuration versioning
- Disaster recovery plan
- Rollback procedures

---

## Conclusion

The TLS AI/AR Production System represents a significant advancement in automotive processing operations. By combining AI, AR, computer vision, and IoT, the system provides:

- **Enhanced Quality** - Automated verification and defect detection
- **Improved Efficiency** - Guided workflows reduce errors and time
- **Better Visibility** - Real-time KPIs and analytics
- **Flexible Control** - Policy-based access and decision making
- **Scalable Architecture** - Microservices ready for growth

The system is currently in pilot phase with core functionality complete and tested, ready for deployment to the first production line.

---

**Document Version:** 1.0  
**Last Updated:** October 20, 2025  
**Maintained By:** TLS Portland VDC Engineering Team
