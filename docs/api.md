# API Reference

This section provides detailed information about the CreatureBox Refactored API endpoints.

The API is built using RESTful principles and returns responses in JSON format.

## Authentication

Most API endpoints require authentication. Include your API key in the header of each request:

```
Authorization: Bearer YOUR_API_KEY
```

## Base URL

All API endpoints are relative to the base URL: `http://your-server:5000/api/`

## Endpoints

### System Status

#### GET /system/status

Returns the current system status and uptime.

**Example Request:**
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" http://your-server:5000/api/system/status
```

**Example Response:**
```json
{
  "status": "running",
  "uptime": "12:34:56",
  "version": "1.0.0"
}
```

### Environmental Data

#### GET /environment/current

Returns current environmental data for all sensors.

**Example Request:**
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" http://your-server:5000/api/environment/current
```

**Example Response:**
```json
{
  "temperature": 25.6,
  "humidity": 65,
  "light_level": 800,
  "updated_at": "2023-04-15T14:30:45"
}
```

### Power Management

#### GET /power/status

Returns the status of all power outlets.

**Example Request:**
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" http://your-server:5000/api/power/status
```

**Example Response:**
```json
{
  "outlets": [
    {
      "id": 1,
      "name": "Main Light",
      "status": "on",
      "power_usage": 45
    },
    {
      "id": 2,
      "name": "Heater",
      "status": "off",
      "power_usage": 0
    }
  ]
}
```

#### PUT /power/outlet/{id}

Controls a specific power outlet.

**Example Request:**
```bash
curl -X PUT -H "Authorization: Bearer YOUR_API_KEY" -H "Content-Type: application/json" -d '{"status": "on"}' http://your-server:5000/api/power/outlet/2
```

**Example Response:**
```json
{
  "id": 2,
  "name": "Heater",
  "status": "on",
  "power_usage": 120
}
```

## Error Responses

The API uses standard HTTP status codes to indicate the success or failure of a request.

**Example Error Response:**
```json
{
  "error": "Unauthorized",
  "message": "Invalid API key",
  "status_code": 401
}
```

Common error codes:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error
