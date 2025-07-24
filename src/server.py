"""Main server module for cPanel MCP."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP
from config import load_config
from cpanel import CpanelAPI
from routes import CpanelRoutes

# Global variables for the server and API client
mcp = FastMCP("cPanel Email Management")
api_client: CpanelAPI | None = None


def initialize_server() -> None:
    """Initialize the server with configuration and routes."""
    global api_client
    
    try:
        # Load configuration from environment and .env file
        config = load_config()
        
        # Create cPanel API client (non-async for FastMCP compatibility)
        api_client = CpanelAPI(config)
        
        # Register routes
        CpanelRoutes(mcp, api_client)
        
    except Exception as e:
        print(f"Error initializing cPanel MCP server: {e}")
        raise


def run_server() -> None:
    """Run the server."""
    initialize_server()
    mcp.run('sse', 'localhost:8000')

if __name__ == "__main__":
    run_server()