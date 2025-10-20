# Deployment Guide

This guide covers different deployment options for TLS Concept - Toyota Production 2.0.

## Table of Contents
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Environment Variables](#environment-variables)
- [Monitoring](#monitoring)

## Local Development

### Prerequisites
- Python 3.12 or higher
- pip package manager
- Virtual environment (recommended)

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/AreteDriver/TLS-Concept-production-2.0.git
cd TLS-Concept-production-2.0
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run the application**
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Docker Deployment

### Using Docker (Planned)

**Dockerfile** (to be created):
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Build and run**:
```bash
docker build -t tls-concept:latest .
docker run -p 8501:8501 tls-concept:latest
```

### Using Docker Compose (Planned)

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

**Run**:
```bash
docker-compose up -d
```

## Cloud Deployment

### Streamlit Cloud

1. **Connect repository**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select the repository

2. **Configure secrets**
   - Add environment variables in Streamlit Cloud dashboard
   - Add `OPENAI_API_KEY` and other secrets

3. **Deploy**
   - Click "Deploy"
   - Application will be available at `your-app.streamlit.app`

### AWS Deployment

#### EC2 Deployment

1. **Launch EC2 instance**
```bash
# Use Ubuntu 22.04 LTS
# t2.medium or larger recommended
```

2. **Setup application**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip

# Install dependencies
sudo apt update
sudo apt install python3.12 python3-pip -y

# Clone and setup
git clone https://github.com/AreteDriver/TLS-Concept-production-2.0.git
cd TLS-Concept-production-2.0
pip install -r requirements.txt

# Run with systemd service
sudo cp deployment/tls-concept.service /etc/systemd/system/
sudo systemctl start tls-concept
sudo systemctl enable tls-concept
```

#### AWS ECS (Planned)
- Container deployment using ECS Fargate
- Auto-scaling configuration
- Load balancer setup

### Azure Deployment

#### Azure App Service
```bash
az webapp up --name tls-concept-app \
  --resource-group tls-rg \
  --runtime "PYTHON:3.12" \
  --sku B1
```

### Google Cloud Platform

#### Cloud Run (Planned)
```bash
gcloud run deploy tls-concept \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for AI features | `sk-...` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LOG_LEVEL` | Logging level | `INFO` |
| `APP_ENV` | Environment name | `development` |
| `ENABLE_AI_GUIDANCE` | Enable AI features | `false` |
| `ENABLE_METRICS_DASHBOARD` | Enable metrics | `true` |

### Setting Environment Variables

**Linux/macOS**:
```bash
export OPENAI_API_KEY="your-key-here"
```

**Windows**:
```cmd
set OPENAI_API_KEY=your-key-here
```

**.env file**:
```
OPENAI_API_KEY=your-key-here
LOG_LEVEL=INFO
```

## Monitoring

### Application Logs

View logs:
```bash
# Development
streamlit run app.py

# Production (systemd)
sudo journalctl -u tls-concept -f
```

### Health Checks

Create a health check endpoint (planned):
```python
@st.cache_data
def health_check():
    return {"status": "healthy", "version": "2.0.0"}
```

### Metrics Collection

Planned integrations:
- Application performance monitoring (APM)
- Error tracking (Sentry)
- User analytics

## Performance Optimization

### Streamlit Configuration

Create `.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 200
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[runner]
fastReruns = true
```

### Caching Strategies

Use Streamlit caching:
```python
@st.cache_data
def load_data():
    # Expensive operation
    pass

@st.cache_resource
def initialize_model():
    # Load ML model once
    pass
```

## Security Best Practices

1. **Never commit secrets**
   - Use environment variables
   - Add `.env` to `.gitignore`

2. **Use HTTPS in production**
   - Configure SSL certificates
   - Use reverse proxy (nginx/caddy)

3. **Implement authentication** (planned)
   - User login system
   - Role-based access control

4. **Regular updates**
   - Keep dependencies updated
   - Monitor security advisories

## Backup and Recovery

### Data Backup
```bash
# Backup data directory
tar -czf backup-$(date +%Y%m%d).tar.gz data/
```

### Disaster Recovery
- Regular automated backups
- Multi-region deployment
- Database replication

## Troubleshooting

### Common Issues

**Port already in use**:
```bash
# Find process using port 8501
lsof -i :8501
# Kill the process
kill -9 <PID>
```

**Module not found**:
```bash
# Ensure virtual environment is activated
source .venv/bin/activate
# Reinstall dependencies
pip install -r requirements.txt
```

**Permission denied**:
```bash
# Fix file permissions
chmod +x app.py
```

## Support

For deployment issues:
- Check [GitHub Issues](https://github.com/AreteDriver/TLS-Concept-production-2.0/issues)
- Review application logs
- Contact maintainers

## Next Steps

After deployment:
1. Configure monitoring
2. Set up automated backups
3. Implement CI/CD pipeline
4. Configure auto-scaling (if cloud deployment)
5. Set up alerting
