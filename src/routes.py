"""MCP tool routes for cPanel email and DNS management."""

from __future__ import annotations

from typing import Dict, Any
from mcp.server.fastmcp import FastMCP
from cpanel import CpanelAPI, CpanelAPIError


class CpanelRoutes:
    """MCP tool routes for cPanel operations."""

    def __init__(self, mcp_server: FastMCP, cpanel_api: CpanelAPI):
        """Initialize the routes with MCP server and cPanel API client.
        
        Args:
            mcp_server: FastMCP server instance
            cpanel_api: CpanelAPI client instance
        """
        self.mcp = mcp_server
        self.api = cpanel_api
        self._register_tools()

    def _register_tools(self) -> None:
        """Register all MCP tools."""
        self._register_email_account_tools()
        self._register_email_forwarder_tools()
        self._register_dns_management_tools()

    def _register_email_account_tools(self) -> None:
        """Register email account management tools."""
        
        @self.mcp.tool()
        def add_email_account(email: str, password: str, quota: int = 0) -> Dict[str, Any]:
            """Add a new email account to cPanel.

            Args:
                email: The full email address (e.g., "user@example.com")
                password: The password for the new email account
                quota: The mailbox size limit in megabytes (MB). Default is 0 for unlimited.

            Returns:
                dict: The JSON response from the API
            """
            try:
                return self.api.add_email_account(email, password, quota)
            except CpanelAPIError as e:
                return {"error": str(e)}
            except Exception as e:
                return {"error": f"Unexpected error: {str(e)}"}

        @self.mcp.tool()
        def delete_email_account(email: str) -> Dict[str, Any]:
            """Delete an email account from cPanel.

            Args:
                email: The full email address to delete (e.g., "user@example.com")

            Returns:
                dict: The JSON response from the API
            """
            try:
                return self.api.delete_email_account(email)
            except CpanelAPIError as e:
                return {"error": str(e)}
            except Exception as e:
                return {"error": f"Unexpected error: {str(e)}"}

        @self.mcp.tool()
        def list_email_accounts(domain: str) -> Dict[str, Any]:
            """List all email accounts for a specific domain.

            Args:
                domain: The domain to list email accounts for (e.g., "example.com")

            Returns:
                dict: The JSON response from the API
            """
            try:
                return self.api.list_email_accounts(domain)
            except CpanelAPIError as e:
                return {"error": str(e)}
            except Exception as e:
                return {"error": f"Unexpected error: {str(e)}"}

        @self.mcp.tool()
        def get_email_settings() -> Dict[str, Any]:
            """Retrieve the client settings for email accounts.

            Returns:
                dict: The JSON response from the API
            """
            try:
                return self.api.get_email_settings()
            except CpanelAPIError as e:
                return {"error": str(e)}
            except Exception as e:
                return {"error": f"Unexpected error: {str(e)}"}

        @self.mcp.tool()
        def update_quota(email: str, quota: int) -> Dict[str, Any]:
            """Change the quota for a given email account.

            Args:
                email: The full email address for which to update the quota
                quota: The new account limit in megabytes (MB)

            Returns:
                dict: The JSON response from the API
            """
            try:
                return self.api.update_quota(email, quota)
            except CpanelAPIError as e:
                return {"error": str(e)}
            except Exception as e:
                return {"error": f"Unexpected error: {str(e)}"}

        @self.mcp.tool()
        def change_password(email: str, new_password: str) -> Dict[str, Any]:
            """Change the password for a given email account.

            Args:
                email: The full email address for which to change the password
                new_password: The new password to set

            Returns:
                dict: The JSON response from the API
            """
            try:
                return self.api.change_password(email, new_password)
            except CpanelAPIError as e:
                return {"error": str(e)}
            except Exception as e:
                return {"error": f"Unexpected error: {str(e)}"}

    def _register_email_forwarder_tools(self) -> None:
        """Register email forwarder management tools."""
        
        @self.mcp.tool()
        def create_email_forwarder(email: str, destination: str) -> Dict[str, Any]:
            """Create an email forwarder.

            Args:
                email: The full source email address
                destination: The full destination email address to forward email to

            Returns:
                dict: The JSON response from the API
            """
            try:
                return self.api.create_email_forwarder(email, destination)
            except CpanelAPIError as e:
                return {"error": str(e)}
            except Exception as e:
                return {"error": f"Unexpected error: {str(e)}"}

        @self.mcp.tool()
        def delete_email_forwarder(email: str, destination: str) -> Dict[str, Any]:
            """Delete an email forwarder.

            Args:
                email: The full source email address
                destination: The full destination email address

            Returns:
                dict: The JSON response from the API
            """
            try:
                return self.api.delete_email_forwarder(email, destination)
            except CpanelAPIError as e:
                return {"error": str(e)}
            except Exception as e:
                return {"error": f"Unexpected error: {str(e)}"}

        @self.mcp.tool()
        def list_email_forwarders(domain: str) -> Dict[str, Any]:
            """List email forwarders for a domain.

            Args:
                domain: The domain to list email forwarders for (e.g., "example.com")

            Returns:
                dict: The JSON response from the API
            """
            try:
                return self.api.list_email_forwarders(domain)
            except CpanelAPIError as e:
                return {"error": str(e)}
            except Exception as e:
                return {"error": f"Unexpected error: {str(e)}"}

    def _register_dns_management_tools(self) -> None:
        """Register DNS management tools."""
        
        @self.mcp.tool()
        def get_dns_records(domain: str) -> Dict[str, Any]:
            """Get all DNS records for a domain.

            Args:
                domain: The domain to get DNS records for (e.g., "example.com")

            Returns:
                dict: The JSON response from the WHM API containing all DNS records with line numbers
            """
            try:
                return self.api.get_dns_records(domain)
            except CpanelAPIError as e:
                return {"error": str(e)}
            except Exception as e:
                return {"error": f"Unexpected error: {str(e)}"}

        @self.mcp.tool()
        def add_dns_record(
            domain: str, 
            name: str, 
            record_type: str, 
            address: str, 
            ttl: int = 3600, 
            record_class: str = "IN"
        ) -> Dict[str, Any]:
            """Add a new DNS record to a domain.

            Args:
                domain: The domain to add the record to (e.g., "example.com")
                name: The record name (e.g., "app.example.com" or "www")
                record_type: The DNS record type (A, AAAA, CNAME, MX, TXT, etc.)
                address: The record value/address (e.g., IP address for A record)
                ttl: Time to live in seconds (default: 3600)
                record_class: DNS class (default: "IN")

            Returns:
                dict: The JSON response from the WHM API
            """
            try:
                return self.api.add_dns_record(domain, name, record_type, address, ttl, record_class)
            except CpanelAPIError as e:
                return {"error": str(e)}
            except Exception as e:
                return {"error": f"Unexpected error: {str(e)}"}

        @self.mcp.tool()
        def edit_dns_record(
            domain: str, 
            line: int, 
            name: str, 
            record_type: str, 
            address: str, 
            ttl: int = 3600, 
            record_class: str = "IN"
        ) -> Dict[str, Any]:
            """Edit an existing DNS record.

            Args:
                domain: The domain containing the record (e.g., "example.com")
                line: The line number of the record to edit (from get_dns_records)
                name: The new record name
                record_type: The new DNS record type (A, AAAA, CNAME, MX, TXT, etc.)
                address: The new record value/address
                ttl: Time to live in seconds (default: 3600)
                record_class: DNS class (default: "IN")

            Returns:
                dict: The JSON response from the WHM API
            """
            try:
                return self.api.edit_dns_record(domain, line, name, record_type, address, ttl, record_class)
            except CpanelAPIError as e:
                return {"error": str(e)}
            except Exception as e:
                return {"error": f"Unexpected error: {str(e)}"}

        @self.mcp.tool()
        def delete_dns_record(domain: str, line: int) -> Dict[str, Any]:
            """Delete a DNS record from a domain.

            Args:
                domain: The domain containing the record (e.g., "example.com")
                line: The line number of the record to delete (from get_dns_records)

            Returns:
                dict: The JSON response from the WHM API
            """
            try:
                return self.api.delete_dns_record(domain, line)
            except CpanelAPIError as e:
                return {"error": str(e)}
            except Exception as e:
                return {"error": f"Unexpected error: {str(e)}"}