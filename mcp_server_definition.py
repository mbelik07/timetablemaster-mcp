# mcp_server_definition.py
import os
from dotenv import load_dotenv

# Try different import patterns for smitheory.ai
try:
    from smitheory.ai.mcp import MCPServer, ToolDefinition, ToolParameter
except ImportError:
    try:
        from smitheory_ai.mcp import MCPServer, ToolDefinition, ToolParameter
    except ImportError:
        # Fallback to basic MCP SDK if smitheory.ai has different structure
        from mcp.server import Server as MCPServer
        from mcp.types import Tool as ToolDefinition
        from mcp.types import ToolParameter

from timetable_api import TimetableMasterAPI

# Load environment variables from the .env file
load_dotenv()

# --- Configuration ---
TIMETABLE_MASTER_BASE_URL = "https://www.timetablemaster.com/api/v1"
TIMETABLE_MASTER_API_KEY = os.getenv("TIMETABLE_API_KEY")

if not TIMETABLE_MASTER_API_KEY:
    raise ValueError("Error: TIMETABLE_API_KEY not found. Please set it in your .env file.")

# Instantiate the TimetableMaster API client once to reuse it
timetable_client = TimetableMasterAPI(TIMETABLE_MASTER_API_KEY, TIMETABLE_MASTER_BASE_URL)

# --- Tool Functions ---
def list_timetables_tool() -> dict:
    """
    The implementation logic for the 'list_timetables' tool.
    """
    try:
        result = timetable_client.list_timetables()
        return {"success": True, "timetables": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_timetable_data_tool(timetable_id: str) -> dict:
    """
    The implementation logic for the 'get_timetable_data' tool.
    """
    try:
        result = timetable_client.get_timetable_data(timetable_id)
        return {"success": True, "timetable_data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

# --- MCP Server Definition ---
tools = [
    ToolDefinition(
        name="list_timetables",
        description="Retrieves a list of all timetables for your organization, returning basic information like ID, name, and status.",
        parameters=[]
    ),
    ToolDefinition(
        name="get_timetable_data",
        description="Retrieves complete and detailed timetable data for a specific timetable using its unique ID, including subjects, teachers, classes, rooms, and schedule.",
        parameters=[
            ToolParameter(
                name="timetable_id",
                type="string",
                description="The unique identifier of the timetable (e.g., 'tt_67890').",
                required=True
            )
        ]
    )
]

timetable_mcp_server = MCPServer(
    name="TimetableMaster_MCP",
    version="1.0.0",
    description="MCP for interacting with the TimetableMaster API to manage and retrieve timetable data.",
    tools=tools
)

timetable_mcp_server.register_tool_function("list_timetables", list_timetables_tool)
timetable_mcp_server.register_tool_function("get_timetable_data", get_timetable_data_tool)