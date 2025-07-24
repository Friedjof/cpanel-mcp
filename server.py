#!/usr/bin/env python3
"""
cPanel MCP Server - Entry point for the Model Context Protocol server.

This server provides MCP tools for managing cPanel email accounts and forwarders.
It loads configuration from environment variables and a .env file.

Usage:
    python server.py
    
Or install as package and use:
    cpanel-mcp
"""

from src.server import run_server

if __name__ == "__main__":
    run_server()
