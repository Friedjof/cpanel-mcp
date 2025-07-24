"""Configuration management for cPanel MCP server."""

from __future__ import annotations

import os
from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv


class CpanelConfig(BaseModel):
    """Configuration for cPanel connection."""
    
    hostname: str = Field(..., description="cPanel hostname")
    username: str = Field(..., description="cPanel username")
    api_token: str = Field(..., description="cPanel API token")
    port: int = Field(default=2083, description="cPanel port")
    ssl: bool = Field(default=True, description="Use SSL connection")
    
    @field_validator('port')
    @classmethod
    def validate_port(cls, v):
        if not 1 <= v <= 65535:
            raise ValueError('Port must be between 1 and 65535')
        return v
    
    @field_validator('hostname')
    @classmethod
    def validate_hostname(cls, v):
        if not v or v.isspace():
            raise ValueError('Hostname cannot be empty')
        return v.strip()
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if not v or v.isspace():
            raise ValueError('Username cannot be empty')
        return v.strip()
    
    @field_validator('api_token')
    @classmethod
    def validate_api_token(cls, v):
        if not v or v.isspace():
            raise ValueError('API token cannot be empty')
        return v.strip()


def load_config() -> CpanelConfig:
    """Load configuration from environment variables and .env file."""
    load_dotenv()
    
    # Get required environment variables
    hostname = os.environ.get("CPANEL_HOSTNAME")
    username = os.environ.get("CPANEL_USERNAME") 
    api_token = os.environ.get("CPANEL_API_TOKEN")
    
    # Check for required variables
    missing_vars = []
    if not hostname:
        missing_vars.append("CPANEL_HOSTNAME")
    if not username:
        missing_vars.append("CPANEL_USERNAME")
    if not api_token:
        missing_vars.append("CPANEL_API_TOKEN")
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    # Get optional variables with defaults
    port_str = os.environ.get("CPANEL_PORT")
    ssl_str = os.environ.get("CPANEL_SSL")
    
    config_data: dict = {
        "hostname": hostname,
        "username": username,
        "api_token": api_token,
    }
    
    # Parse optional port
    if port_str:
        try:
            config_data["port"] = int(port_str)
        except ValueError:
            raise ValueError(f"Invalid port value: {port_str}")
    
    # Parse optional SSL setting
    if ssl_str:
        config_data["ssl"] = ssl_str.lower() in ("true", "1", "yes", "on")
    
    return CpanelConfig(**config_data)