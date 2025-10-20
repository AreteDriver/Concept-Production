# TLS AI/AR Production System 2.0

> AI + AR augmented production for Toyota Logistics Services Portland VDC
> 
> **Version:** 0.1.0 (Pilot Phase)

## 🎯 Executive Summary

This system integrates AI-powered computer vision and AR guidance to enhance PPO install, QA inspection, and yard operations. AR glasses guide workers through SOPs, enforce quality checks, and control vehicle access based on completion status. The system tracks 140,000+ VINs across 4 docks with intelligent logistics planning.

**Key Benefits:**
- ✅ Reduce cycle time and rework
- ✅ Increase first-time-through quality
- ✅ Eliminate training gaps with guided workflows
- ✅ Real-time KPI tracking and alerts
- ✅ Intelligent yard logistics planning

---

## 📁 Repository Structure

```
TLS-Concept-production-2.0/
├── apps/                          # Microservices and applications
│   ├── orchestrator-api/          # FastAPI orchestrator (port 8000)
│   ├── cv-service/                # Computer vision service (port 8001)
│   ├── device-io/                 # Device I/O service (port 8002)
│   ├── edge-gateway/              # MQTT/HTTPS bridge (future)
│   ├── ar-client/                 # AR client for XR devices (future)
│   └── dashboards/                # Streamlit analytics dashboards
│       ├── supervisor_dashboard.py    # Production KPIs
│       └── logistics_planner.py       # Yard & logistics planning
│
├── packages/                      # Shared libraries
│   ├── event-contracts/           # Pydantic models and events
│   ├── rules-engine/              # Policy evaluation engine
│   ├── sdk-js/                    # JavaScript SDK (future)
│   └── sdk-py/                    # Python SDK (future)
│
├── docs/                          # Documentation
│   ├── sop/                       # SOP definitions (YAML)
│   ├── policies/                  # Access control policies
│   ├── api/                       # OpenAPI specs (future)
│   ├── adr/                       # Architecture decisions (future)
│   └── training/                  # Training materials (future)
│
├── tests/                         # Test suites
│   ├── unit/                      # Unit tests
│   ├── integration/               # Integration tests
│   └── e2e/                       # End-to-end tests (future)
│
├── infra/                         # Infrastructure as code
│   ├── k8s/                       # Kubernetes manifests (future)
│   ├── terraform/                 # Terraform configs (future)
│   └── ci/                        # CI/CD configs
│
└── .github/
    └── workflows/                 # GitHub Actions CI/CD
        └── ci.yml                 # Main CI pipeline
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or 3.12
- pip (Python package manager)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/AreteDriver/TLS-Concept-production-2.0.git
cd TLS-Concept-production-2.0
```

2. **Install dependencies for services:**

**Orchestrator API:**
```bash
cd apps/orchestrator-api
pip install -r requirements.txt
python main.py
# Access at http://localhost:8000
# API docs at http://localhost:8000/docs
```

**CV Service:**
```bash
cd apps/cv-service
pip install -r requirements.txt
python main.py
# Access at http://localhost:8001
```

**Device I/O Service:**
```bash
cd apps/device-io
pip install -r requirements.txt
python main.py
# Access at http://localhost:8002
```

**Supervisor Dashboard:**
```bash
cd apps/dashboards
pip install -r requirements.txt
streamlit run supervisor_dashboard.py
# Opens in browser automatically
```

**Logistics Planner:**
```bash
cd apps/dashboards
streamlit run logistics_planner.py
```

### Running Tests

```bash
# Unit tests
cd tests/unit
pytest -v

# Integration tests
cd tests/integration
pytest -v

# Run all tests with coverage
pytest tests/ -v --cov=packages --cov=apps
```

---

## 🏗️ System Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌────────────────────┐
│   AR Client     │────▶│  Edge Gateway    │────▶│  API Orchestrator  │
│  (HoloLens/XR)  │     │  (MQTT/HTTPS)    │     │    (FastAPI)       │
└─────────────────┘     └──────────────────┘     └────────┬───────────┘
                                                            │
                        ┌───────────────────────────────────┼────────────┐
                        │                                   │            │
                        ▼                                   ▼            ▼
              ┌──────────────────┐              ┌──────────────┐  ┌─────────────┐
              │  Rules Engine    │              │  CV Service  │  │  Device I/O │
              │  (Policy Eval)   │              │  (Vision)    │  │  (Hardware) │
              └──────────────────┘              └──────────────┘  └─────────────┘
                        │
                        ▼
              ┌──────────────────┐
              │   Event Bus      │
              │   (Kafka/NATS)   │
              └─────────┬────────┘
                        │
                        ▼
              ┌──────────────────┐
              │  Data Lakehouse  │
              │  Analytics/KPIs  │
              └──────────────────┘
```

### Key Components:

1. **API Orchestrator** - Central API for vehicle, step, and access management
2. **Rules Engine** - Declarative policy evaluation for SOP gating and access control
3. **CV Service** - Computer vision for VIN OCR, part detection, and quality verification
4. **Device I/O** - Interface for torque wrenches, printers, scanners, and gates
5. **Dashboards** - Real-time KPI monitoring and logistics planning
6. **Event Contracts** - Shared data models and event schemas

---

## 🔄 Core Workflows

### 1. VIN → Install → QA → Access Flow

```
1. Scan VIN barcode
   └─▶ System pulls work package and SOP steps
   
2. Pre-flight checks
   └─▶ Verify parts, tools, and certifications
   
3. Guided install steps
   ├─▶ AR overlay shows instructions
   ├─▶ Capture torque readings
   ├─▶ Take photos for critical items
   └─▶ CV verifies installation
   
4. QA walkaround
   ├─▶ Checklist with photo prompts
   └─▶ CV detects defects
   
5. Access grant evaluation
   └─▶ Rules engine checks completion
       ├─▶ All steps complete? ✓
       ├─▶ QA status green? ✓
       ├─▶ No open defects? ✓
       └─▶ Grant start/unlock/drive access
```

### 2. Parts Department Flow

```
1. Scan part barcode
2. AR shows storage location
3. Visual prompts guide placement
4. System updates inventory
5. Associate with VIN if allocated
```

### 3. Logistics Planning

```
1. Bulk VIN data ingestion from HQ
2. Algorithm assigns parking positions
   ├─▶ Customer priority (hot units)
   ├─▶ Parts availability
   ├─▶ Dock capacity
   └─▶ Labor/certifications
3. Coordinate shuttle movements
4. Track throughput vs. capacity
```

---

## 📊 Key Performance Indicators

The system tracks:

- **Cycle Time** - Time per step and total per vehicle
- **First-Time-Through Rate** - Percentage passing without rework
- **Rework Rate** - By part, step, and installer
- **Defects per 100 Vehicles** - Overall quality metric
- **Training Coverage** - Certifications vs. required
- **Throughput** - Daily units vs. goal
- **Dock Utilization** - Capacity usage across 4 docks
- **Parts Availability** - Inventory vs. demand

---

## 🔐 Security & Access Control

### Policy-Based Access

Access to vehicles is controlled by declarative policies in YAML:

```yaml
rules:
  - id: grant-start-after-qa
    conditions:
      all:
        - field: vehicle.status
          operator: "=="
          value: install_done
        - field: qa.status
          operator: "=="
          value: green
    actions:
      - type: grant
        scope: start
        ttl_seconds: 1800
```

### Authentication

- SSO/OIDC integration (stub in V1)
- Role-based access control (installer, QA, yard driver, supervisor, admin)
- JWT tokens for API access

---

## 📝 SOP Definitions

SOPs are defined in YAML format:

```yaml
id: apply-window-decal
type: install
description: "Apply window decal with proper alignment"
requires:
  tools: [squeegee, spray_bottle]
  parts: [window_decal_123]
inputs:
  photo_required: true
  cv_required: true
  cv_template: decals/window_template.png
pass_criteria:
  cv:
    iou_threshold: 0.85
    skew_deg_max: 2.0
```

See `docs/sop/` for examples.

---

## 🧪 Testing

### Unit Tests
- Rules engine evaluation logic
- Data model validation
- Policy parsing

### Integration Tests
- Complete workflow scenarios
- Access grant flows
- Defect handling
- Hot unit prioritization

### E2E Tests (Future)
- Full system workflows
- AR client integration
- Hardware device interactions

---

## 🚢 Deployment

### Development
- Local services on different ports
- In-memory storage
- Mock device implementations

### Production (Future)
- Kubernetes deployment
- PostgreSQL + Redis
- MQTT broker
- S3 for artifacts
- Kafka for events

---

## 📚 API Documentation

### Orchestrator API

**Base URL:** `http://localhost:8000`

**Key Endpoints:**
- `GET /vehicles/{vin}` - Get vehicle status
- `POST /vehicles/{vin}` - Register vehicle
- `GET /vehicles/{vin}/steps` - Get SOP steps
- `POST /steps/{step_id}/complete` - Complete step
- `POST /qa/{vin}/walkaround` - Submit QA results
- `POST /access/{vin}/grant` - Grant vehicle access

**Interactive Docs:** http://localhost:8000/docs

### CV Service

**Base URL:** `http://localhost:8001`

**Endpoints:**
- `POST /ocr/vin` - VIN barcode OCR
- `POST /detect/part` - Part presence detection
- `POST /verify/decal-alignment` - Decal alignment check
- `POST /detect/damage` - Damage detection

### Device I/O

**Base URL:** `http://localhost:8002`

**Endpoints:**
- `POST /torque/read` - Read torque wrench
- `POST /printer/print` - Print label
- `POST /gate/control` - Control gate/door
- `POST /scanner/scan` - Trigger barcode scan

---

## 🤝 Contributing

1. Create a feature branch
2. Make changes
3. Add tests
4. Run linting: `black . && flake8 .`
5. Submit PR

---

## 📞 Support

For questions or issues:
- Open a GitHub issue
- Contact: TLS Portland VDC Engineering Team

---

## 📄 License

Proprietary - Toyota Logistics Services

---

## 🗺️ Roadmap

### ✅ Phase 0 - Foundation (Current)
- [x] Core data models
- [x] Rules engine
- [x] Orchestrator API
- [x] CV service (mock)
- [x] Device I/O (mock)
- [x] Dashboards
- [x] Unit/integration tests
- [x] CI/CD pipeline

### 🚧 Phase 1 - Pilot Line (Next)
- [ ] Real device integration
- [ ] AR client prototype
- [ ] Single production line deployment
- [ ] Database persistence
- [ ] Event bus integration

### 📅 Phase 2 - Expansion
- [ ] Multiple lines
- [ ] Full yard management
- [ ] Advanced CV models
- [ ] ML-based damage detection
- [ ] Analytics warehouse

### 🔮 Phase 3 - Optimization
- [ ] Predictive maintenance
- [ ] Automated scheduling
- [ ] Advanced telematics
- [ ] Warranty integration
