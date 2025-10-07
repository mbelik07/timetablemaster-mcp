# app.py - Flask application wrapper for MCP
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from timetable_api import TimetableMasterAPI

load_dotenv()

app = Flask(__name__)

# Configuration
TIMETABLE_MASTER_BASE_URL = "https://www.timetablemaster.com/api/v1"
TIMETABLE_MASTER_API_KEY = os.getenv("TIMETABLE_API_KEY")

if not TIMETABLE_MASTER_API_KEY:
    print("WARNING: TIMETABLE_API_KEY not set!")
    TIMETABLE_MASTER_API_KEY = "PLACEHOLDER"

# Instantiate the API client
timetable_client = TimetableMasterAPI(TIMETABLE_MASTER_API_KEY, TIMETABLE_MASTER_BASE_URL)

# MCP Metadata
MCP_METADATA = {
    "name": "TimetableMaster_MCP",
    "version": "1.0.0",
    "description": "MCP for interacting with the TimetableMaster API to manage and retrieve timetable data.",
    "tools": [
        {
            "name": "list_timetables",
            "description": "Retrieves a list of all timetables for your organization, returning basic information like ID, name, and status.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        },
        {
            "name": "get_timetable_data",
            "description": "Retrieves complete and detailed timetable data for a specific timetable using its unique ID, including subjects, teachers, classes, rooms, and schedule.",
            "parameters": {
                "type": "object",
                "properties": {
                    "timetable_id": {
                        "type": "string",
                        "description": "The unique identifier of the timetable (e.g., 'tt_67890')."
                    }
                },
                "required": ["timetable_id"]
            }
        }
    ]
}

@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "service": "TimetableMaster MCP Server",
        "version": "1.0.0",
        "endpoints": {
            "metadata": "/metadata",
            "invoke": "/invoke",
            "health": "/health"
        }
    })

@app.route("/metadata", methods=["GET"])
def get_metadata():
    """Returns the MCP metadata describing available tools."""
    return jsonify(MCP_METADATA)

@app.route("/invoke", methods=["POST"])
def invoke_tool():
    """Handles tool invocation requests."""
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "error": "No JSON data provided"}), 400
    
    tool_name = data.get("tool_name")
    parameters = data.get("parameters", {})
    
    if not tool_name:
        return jsonify({"success": False, "error": "tool_name is required"}), 400
    
    try:
        if tool_name == "list_timetables":
            result = timetable_client.list_timetables()
            return jsonify({"success": True, "result": {"timetables": result}})
        
        elif tool_name == "get_timetable_data":
            timetable_id = parameters.get("timetable_id")
            if not timetable_id:
                return jsonify({
                    "success": False, 
                    "error": "Missing 'timetable_id' parameter for get_timetable_data"
                }), 400
            
            result = timetable_client.get_timetable_data(timetable_id)
            return jsonify({"success": True, "result": {"timetable_data": result}})
        
        else:
            return jsonify({"success": False, "error": f"Unknown tool: {tool_name}"}), 404
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for Render."""
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)