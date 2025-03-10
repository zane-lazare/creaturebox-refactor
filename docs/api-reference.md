# API Reference

## Overview

CreatureBox provides a comprehensive REST API for programmatic interaction with the habitat management system.

## Authentication

### JWT Authentication
- Endpoint: `/auth/login`
- Method: POST
- Required Parameters:
  - `username`
  - `password`

### Example Request
```bash
curl -X POST https://creaturebox.example.com/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username":"admin", "password":"secret"}'
```

## Endpoints

### Sensor Data

#### Get Current Sensor Readings
- Endpoint: `/api/sensors`
- Method: GET
- Authentication: Required
- Response: JSON array of sensor data

#### Get Historical Sensor Data
- Endpoint: `/api/sensors/history`
- Method: GET
- Query Parameters:
  - `start_date`: ISO 8601 timestamp
  - `end_date`: ISO 8601 timestamp
  - `sensor_type`: Optional sensor type filter

### Power Management

#### Get Outlet Status
- Endpoint: `/api/power/outlets`
- Method: GET
- Authentication: Required
- Response: JSON array of outlet statuses

#### Control Outlet
- Endpoint: `/api/power/outlets/{outlet_id}`
- Methods: 
  - GET: Retrieve outlet status
  - POST: Change outlet state
- Request Body:
  ```json
  {
    "state": "on|off",
    "duration": null|seconds
  }
  ```

### Data Analysis

#### Generate Report
- Endpoint: `/api/analysis/report`
- Method: POST
- Request Body:
  ```json
  {
    "report_type": "environmental|power|comprehensive",
    "start_date": "2025-01-01T00:00:00Z",
    "end_date": "2025-03-10T23:59:59Z"
  }
  ```

## Error Handling

### Common Error Codes
- `200`: Success
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Internal Server Error

### Error Response Format
```json
{
  "error": true,
  "code": 400,
  "message": "Invalid request parameters",
  "details": "Additional error information"
}
```

## Rate Limiting

- Max Requests: 100/minute
- Burst Rate: 50 requests in 10 seconds
- Exceeding limits results in temporary IP block

## Webhooks

### Configurable Webhook Endpoints
- `/webhooks/sensors`
- `/webhooks/power`
- `/webhooks/alerts`

### Webhook Configuration
```json
{
  "event_type": "temperature_threshold",
  "url": "https://your-webhook-endpoint.com/receive",
  "method": "POST",
  "authentication": {
    "type": "bearer",
    "token": "your_secret_token"
  }
}
```

## SDK and Client Libraries

### Supported Languages
- Python
- JavaScript
- Go
- Java

### Installation (Python)
```bash
pip install creaturebox-sdk
```

## Versioning

- Current API Version: `v1`
- Endpoint Prefix: `/api/v1/`
- Deprecation Policy: 6-month notice before endpoint retirement

## Security Recommendations

- Use HTTPS
- Implement token rotation
- Store credentials securely
- Monitor and log API access
