# TimetableMaster MCP Server

This is a Model Context Protocol (MCP) server for the TimetableMaster API, allowing LLMs to interact with timetable data.

## Features

- **list_timetables**: Retrieves all timetables for your organization
- **get_timetable_data**: Gets detailed data for a specific timetable

## API Endpoints

### GET /
Returns service status and available endpoints.

### GET /metadata
Returns MCP metadata describing all available tools.

### POST /invoke
Invokes a specific tool with parameters.

Example request:
```json
{
  "tool_name": "list_timetables",
  "parameters": {}
}
```

Example request with parameters:
```json
{
  "tool_name": "get_timetable_data",
  "parameters": {
    "timetable_id": "tt_67890"
  }
}
```

### GET /health
Health check endpoint.

## Setup

### Local Development

1. Clone this repository
2. Create a virtual environment: `python3 -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and add your TimetableMaster API key
6. Run: `python app.py`

### Deployment on Render

This repository is configured for deployment on Render.com:

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set the environment variable `TIMETABLE_API_KEY` in Render's dashboard
4. Render will automatically deploy using:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `bash start.sh`

## Environment Variables

- `TIMETABLE_API_KEY`: Your TimetableMaster API key (required)
- `PORT`: Port to run the server on (automatically set by Render)

## Testing

Test the metadata endpoint:
```bash
curl https://timetablemaster-mcp.onrender.com/metadata
```

Test listing timetables:
```bash
curl -X POST https://timetablemaster-mcp.onrender.com/invoke \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "list_timetables", "parameters": {}}'
```

## API Documentation

For more information about the TimetableMaster API, visit: https://www.timetablemaster.com/docs

## License

MIT