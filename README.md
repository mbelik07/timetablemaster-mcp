# TimetableMaster MCP Server

This is a Model Context Protocol (MCP) server for the TimetableMaster API, allowing LLMs to interact with timetable data.

## Features

- **list_timetables**: Retrieves all timetables for your organization
- **get_timetable_data**: Gets detailed data for a specific timetable

## Setup

### Local Development

1. Clone this repository
2. Create a virtual environment: `python3 -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and add your TimetableMaster API key
6. Run: `smitheory-ai mcp run mcp_server_definition.py:timetable_mcp_server --host 127.0.0.1 --port 5000`

### Deployment on Render

This repository is configured for deployment on Render.com:

1. Connect your GitHub repository to Render
2. Set the environment variable `TIMETABLE_API_KEY` in Render's dashboard
3. Render will automatically deploy using the configuration in this repo

## API Documentation

For more information about the TimetableMaster API, visit: https://www.timetablemaster.com/docs

## License

MIT