# API Documentation

## Overview

This document describes the internal API structure and future external API endpoints for the TLS Concept - Toyota Production 2.0 system.

## Internal Functions

### Main Application (`app.py`)

#### `generate_sample_metrics()`

**Description**: Generate sample metrics data for demonstration purposes.

**Returns**: 
- `pd.DataFrame`: DataFrame containing sample metrics with columns:
  - `Date`: Date range for the metrics
  - `Cycle Time (hrs)`: Manufacturing cycle time in hours
  - `QA Issues`: Number of quality assurance issues
  - `Production Units`: Number of units produced
  - `Efficiency (%)`: Production efficiency percentage

**Caching**: Data is cached for 60 seconds using `@st.cache_data`

**Example**:
```python
df = generate_sample_metrics()
print(df.head())
```

#### `render_sidebar()`

**Description**: Render the sidebar navigation and system status.

**Returns**:
- `str`: Selected page name

**Example**:
```python
page = render_sidebar()
if page == "🏠 Dashboard":
    render_dashboard()
```

#### `render_dashboard()`

**Description**: Render the main dashboard view with key metrics and trends.

**Parameters**: None

**Returns**: None (renders Streamlit UI)

#### `render_metrics()`

**Description**: Render the detailed metrics analysis view.

**Parameters**: None

**Returns**: None (renders Streamlit UI)

#### `render_ai_guidance()`

**Description**: Render the AI guidance and recommendations view.

**Parameters**: None

**Returns**: None (renders Streamlit UI)

#### `render_settings()`

**Description**: Render the settings and configuration view.

**Parameters**: None

**Returns**: None (renders Streamlit UI)

#### `main()`

**Description**: Main application entry point that orchestrates page routing.

**Parameters**: None

**Returns**: None

**Example**:
```python
if __name__ == "__main__":
    main()
```

### Configuration (`config.py`)

#### `AppConfig` Class

**Description**: Application configuration dataclass.

**Attributes**:
- `app_name` (str): Application name (default: "Toyota Production 2.0")
- `page_icon` (str): Page icon emoji (default: "🏭")
- `layout` (str): Page layout (default: "wide")
- `openai_api_key` (Optional[str]): OpenAI API key from environment
- `log_level` (str): Logging level (default: "INFO")
- `enable_ai_guidance` (bool): Enable AI features flag (default: False)
- `enable_metrics_dashboard` (bool): Enable metrics flag (default: True)
- `enable_ar_interface` (bool): Enable AR interface flag (default: False)

**Methods**:

##### `from_env()`

**Description**: Create configuration instance from environment variables.

**Returns**: 
- `AppConfig`: Configuration instance

**Example**:
```python
from config import AppConfig

config = AppConfig.from_env()
print(config.app_name)
```

## Future REST API Endpoints (Planned)

### Base URL

```
https://api.tls-concept.example.com/v1
```

### Authentication

```http
Authorization: Bearer <api_key>
```

### Endpoints

#### GET `/health`

**Description**: Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "timestamp": "2025-10-20T12:00:00Z"
}
```

#### GET `/metrics`

**Description**: Retrieve current metrics.

**Query Parameters**:
- `period` (string): Time period (day, week, month)
- `metric_type` (string): Type of metric to retrieve

**Response**:
```json
{
  "metrics": [
    {
      "date": "2025-10-20",
      "cycle_time": 22.5,
      "qa_issues": 5,
      "production_units": 100,
      "efficiency": 87.3
    }
  ]
}
```

#### POST `/ai/analyze`

**Description**: Request AI analysis of production data.

**Request Body**:
```json
{
  "data": {...},
  "analysis_type": "prediction|optimization|root_cause"
}
```

**Response**:
```json
{
  "analysis_id": "abc123",
  "results": {...},
  "recommendations": [...]
}
```

#### GET `/ai/recommendations`

**Description**: Get AI-powered recommendations.

**Response**:
```json
{
  "recommendations": [
    {
      "id": "rec_001",
      "type": "optimization",
      "description": "Reduce cycle time by optimizing assembly line 3",
      "impact": "high",
      "confidence": 0.92
    }
  ]
}
```

#### POST `/alerts`

**Description**: Create a new alert.

**Request Body**:
```json
{
  "type": "warning|error|info",
  "message": "Alert message",
  "source": "system|user|ai"
}
```

#### GET `/alerts`

**Description**: Retrieve alerts.

**Query Parameters**:
- `status` (string): open|closed|all
- `type` (string): Filter by alert type

**Response**:
```json
{
  "alerts": [
    {
      "id": "alert_001",
      "type": "warning",
      "message": "Cycle time spike detected",
      "timestamp": "2025-10-20T12:00:00Z",
      "status": "open"
    }
  ]
}
```

## Error Handling

All API endpoints follow standard HTTP status codes:

- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Internal Server Error

**Error Response Format**:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {...}
  }
}
```

## Rate Limiting

- Rate limit: 1000 requests per hour per API key
- Rate limit headers included in responses:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

## Webhooks (Planned)

Configure webhooks to receive real-time updates:

```json
{
  "url": "https://your-app.com/webhook",
  "events": ["alert.created", "metric.threshold", "analysis.complete"],
  "secret": "webhook_secret_key"
}
```

## SDKs (Planned)

Official SDKs will be available for:
- Python
- JavaScript/TypeScript
- Go
- Java

## Support

For API questions or issues:
- GitHub Issues: [Report here](https://github.com/AreteDriver/TLS-Concept-production-2.0/issues)
- Documentation: [docs/](../docs/)
