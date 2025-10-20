# Getting Started with TLS AI/AR Production System

This guide will help you get the TLS AI/AR Production System up and running on your local machine.

## Prerequisites

- **Python 3.11 or 3.12**
- **pip** (Python package manager)
- **Git** (for cloning the repository)

Optional:
- **Docker** (for containerized deployment)
- **Streamlit** (for dashboards - installed with requirements)

## Quick Start (5 Minutes)

### 1. Clone the Repository

```bash
git clone https://github.com/AreteDriver/TLS-Concept-production-2.0.git
cd TLS-Concept-production-2.0
```

### 2. Install Dependencies

```bash
# Install core dependencies
pip install pydantic pytest pyyaml requests
```

### 3. Run Tests

```bash
# Run all tests to verify installation
pytest tests/ -v
```

Expected output: All tests should pass ✅

### 4. Start the Orchestrator API

```bash
cd apps/orchestrator-api
pip install -r requirements.txt
python main.py
```

The API will start at `http://localhost:8000`

Open your browser and visit:
- **Interactive API Docs:** http://localhost:8000/docs
- **API Health Check:** http://localhost:8000/

### 5. Load Sample Data

Open a new terminal and run:

```bash
cd /path/to/TLS-Concept-production-2.0
python scripts/load_sample_data.py
```

This will:
- Load 3 work packages (Camry, RAV4, Tacoma)
- Create 3 sample vehicles
- Populate the system with test data

### 6. Launch the Supervisor Dashboard

Open another terminal:

```bash
cd apps/dashboards
pip install -r requirements.txt
streamlit run supervisor_dashboard.py
```

The dashboard will open automatically in your browser showing:
- Real-time KPIs
- Cycle time trends
- Defects tracking
- Labor & capacity metrics

### 7. Launch the Logistics Planner

In another terminal:

```bash
cd apps/dashboards
streamlit run logistics_planner.py
```

This shows:
- Dock allocation & status
- Incoming vehicle management
- Resource optimization recommendations
- Daily production planning

---

## Understanding the System

### Core Components

1. **Orchestrator API** (Port 8000)
   - Central API for all operations
   - Manages vehicles, steps, QA, and access control
   - Built with FastAPI

2. **CV Service** (Port 8001)
   - Computer vision operations
   - VIN OCR, part detection, decal verification
   - Image processing endpoints

3. **Device I/O Service** (Port 8002)
   - Hardware device interface
   - Torque wrench, printer, scanner, gate control
   - WebSocket support for real-time data

4. **Rules Engine** (Package)
   - Policy-based access control
   - Declarative rules in YAML
   - Context evaluation for grant/deny decisions

5. **Dashboards** (Streamlit Apps)
   - Supervisor dashboard for production monitoring
   - Logistics planner for yard management

---

## Basic Workflows

### Register a Vehicle

```bash
curl -X POST http://localhost:8000/vehicles/1HGCM82633A999999 \
  -H "Content-Type: application/json" \
  -d '{
    "vin": "1HGCM82633A999999",
    "model": "Camry",
    "color": "Red",
    "status": "incoming",
    "work_package_id": "wp_camry_standard",
    "dock_location": "Dock 1",
    "parking_position": "P150"
  }'
```

### Get Vehicle Status

```bash
curl http://localhost:8000/vehicles/1HGCM82633A999999
```

### Get SOP Steps for Vehicle

```bash
curl http://localhost:8000/vehicles/1HGCM82633A999999/steps
```

### Complete an SOP Step

```bash
curl -X POST http://localhost:8000/steps/apply-window-decal/complete \
  -H "Content-Type: application/json" \
  -d '{
    "vin": "1HGCM82633A999999",
    "result": "pass",
    "artifacts": {
      "photo_uri": "s3://bucket/photo.jpg",
      "cv_verification": {
        "iou_score": 0.91,
        "skew_degrees": 0.8
      }
    }
  }'
```

### Submit QA Walkaround

```bash
curl -X POST http://localhost:8000/qa/1HGCM82633A999999/walkaround \
  -H "Content-Type: application/json" \
  -d '{
    "defects": [],
    "photos": ["photo1.jpg", "photo2.jpg"],
    "overall_status": "green"
  }'
```

### Grant Vehicle Access

```bash
curl -X POST http://localhost:8000/access/1HGCM82633A999999/grant \
  -H "Content-Type: application/json" \
  -d '{
    "scope": "start",
    "ttl_seconds": 1800,
    "reason": "QA passed, all steps complete"
  }'
```

---

## Testing the Rules Engine

The rules engine evaluates policies to grant or deny vehicle access.

### Example: Test Policy Evaluation

```python
from packages.rules_engine import RulesEngine, Policy, Rule, Action

# Load policy from YAML
import yaml
with open('docs/policies/access-control.yaml') as f:
    policy_data = yaml.safe_load(f)

policy = Policy(**policy_data)
engine = RulesEngine(policy)

# Evaluate context
context = {
    "vehicle": {"status": "install_done"},
    "qa": {"status": "green"},
    "defects": {"open": {"count": 0}}
}

decision = engine.evaluate(context)
print(f"Decision: {decision.decision}")
print(f"Reason: {decision.reason}")
```

---

## Running All Services Together

### Option 1: Multiple Terminals

**Terminal 1 - Orchestrator API:**
```bash
cd apps/orchestrator-api && python main.py
```

**Terminal 2 - CV Service:**
```bash
cd apps/cv-service && python main.py
```

**Terminal 3 - Device I/O:**
```bash
cd apps/device-io && python main.py
```

**Terminal 4 - Supervisor Dashboard:**
```bash
cd apps/dashboards && streamlit run supervisor_dashboard.py
```

**Terminal 5 - Logistics Planner:**
```bash
cd apps/dashboards && streamlit run logistics_planner.py
```

### Option 2: Docker Compose (Future)

```bash
docker-compose up
```

This will start all services in containers.

---

## Development Tips

### Running Tests During Development

```bash
# Run specific test file
pytest tests/unit/test_rules_engine.py -v

# Run with coverage
pytest tests/ --cov=packages --cov=apps --cov-report=html

# Run only integration tests
pytest tests/integration/ -v
```

### Code Formatting

```bash
# Format code with black
black packages/ apps/ tests/

# Sort imports
isort packages/ apps/ tests/

# Lint with flake8
flake8 packages/ apps/ tests/ --max-line-length=120
```

### Validating YAML Files

```bash
python -c "
import yaml
from pathlib import Path

for yaml_file in Path('docs').rglob('*.yaml'):
    with open(yaml_file) as f:
        yaml.safe_load(f)
    print(f'✓ {yaml_file}')
"
```

---

## Troubleshooting

### Issue: API won't start

**Problem:** Port already in use
```
ERROR: Address already in use
```

**Solution:** Change the port or kill the existing process
```bash
# Check what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or run on different port
uvicorn main:app --port 8001
```

### Issue: Import errors

**Problem:** Cannot import modules
```
ModuleNotFoundError: No module named 'event_contracts'
```

**Solution:** Ensure packages directory is in Python path
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "packages"))
```

### Issue: Tests failing

**Problem:** Pydantic validation errors

**Solution:** Install correct Pydantic version
```bash
pip install pydantic==2.9.2
```

---

## Next Steps

Once you have the system running:

1. **Explore the API** - Visit http://localhost:8000/docs
2. **Review the Dashboards** - Monitor KPIs and logistics
3. **Read the Documentation** - See `docs/` for detailed specs
4. **Modify SOPs** - Edit YAML files in `docs/sop/`
5. **Customize Policies** - Edit `docs/policies/access-control.yaml`
6. **Add New Vehicles** - Use the API or load_sample_data.py script
7. **Run Workflows** - Test the complete VIN→Install→QA→Access flow

---

## Additional Resources

- **API Documentation:** `docs/api/orchestrator-api.md`
- **Architecture Decisions:** `docs/adr/`
- **SOP Examples:** `docs/sop/`
- **Policy Examples:** `docs/policies/`
- **Main README:** `README.md`

---

## Getting Help

If you encounter issues:
1. Check the logs in each service terminal
2. Review the API docs at `/docs`
3. Run tests to identify problems
4. Open an issue on GitHub

---

**Happy Building! 🚀**
