"""cPanel API client implementation."""

from __future__ import annotations

import httpx
from typing import Dict, Any, Optional, Tuple
from config import CpanelConfig


class CpanelAPIError(Exception):
    """Exception raised for cPanel API errors."""
    pass


class CpanelAPI:
    """Client for interacting with cPanel UAPI."""

    def __init__(self, config: CpanelConfig):
        """Initialize the cPanel API client.
        
        Args:
            config: cPanel configuration object
        """
        self.config = config
        protocol = "https" if config.ssl else "http"
        self.base_url = f"{protocol}://{config.hostname}:{config.port}"
        self.headers = {
            "Authorization": f"cpanel {self.config.username}:{self.config.api_token}",
            "Content-Type": "application/json",
        }

    def make_call(
        self, 
        module: str, 
        function: str, 
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make a call to the cPanel UAPI.

        Args:
            module: The cPanel UAPI module (e.g., "Email")
            function: The function to call (e.g., "add_pop")
            params: The parameters to pass for the API call

        Returns:
            The JSON response from the API

        Raises:
            CpanelAPIError: If the API call fails
        """
        if params is None:
            params = {}

        url = f"{self.base_url}/execute/{module}/{function}"
        
        try:
            response = httpx.get(url, headers=self.headers, params=params, timeout=30.0)
            response.raise_for_status()
            
            result = response.json()
            
            # Check if the API returned an error
            if isinstance(result, dict) and result.get("status") == 0:
                error_msg = result.get("errors", ["Unknown API error"])[0]
                raise CpanelAPIError(f"cPanel API error: {error_msg}")
            
            return result
            
        except httpx.RequestError as e:
            raise CpanelAPIError(f"Request failed: {e}")
        except ValueError as e:
            raise CpanelAPIError(f"Invalid JSON response from cPanel API: {e}")

    @staticmethod
    def split_email(email: str) -> Tuple[str, str]:
        """Split an email address into username and domain.
        
        Args:
            email: Full email address (e.g., "user@example.com")
            
        Returns:
            Tuple of (username, domain)
            
        Raises:
            ValueError: If email format is invalid
        """
        if "@" not in email:
            raise ValueError(f"Invalid email format: {email}")
        
        parts = email.split("@")
        if len(parts) != 2:
            raise ValueError(f"Invalid email format: {email}")
        
        username, domain = parts
        if not username or not domain:
            raise ValueError(f"Invalid email format: {email}")
        
        return username, domain

    # Email Account Management Methods
    def add_email_account(
        self, 
        email: str, 
        password: str, 
        quota: int = 0
    ) -> Dict[str, Any]:
        """Add a new email account.
        
        Args:
            email: Full email address
            password: Password for the new account
            quota: Mailbox size limit in MB (0 for unlimited)
            
        Returns:
            API response
        """
        username, domain = self.split_email(email)
        params = {
            "domain": domain,
            "email": username,
            "password": password,
            "quota": quota,
        }
        return self.make_call("Email", "add_pop", params)

    def delete_email_account(self, email: str) -> Dict[str, Any]:
        """Delete an email account.
        
        Args:
            email: Full email address to delete
            
        Returns:
            API response
        """
        username, domain = self.split_email(email)
        params = {
            "domain": domain,
            "email": username,
        }
        return self.make_call("Email", "del_pop", params)

    def list_email_accounts(self, domain: str) -> Dict[str, Any]:
        """List all email accounts for a domain.
        
        Args:
            domain: Domain to list accounts for
            
        Returns:
            API response
        """
        params = {"domain": domain}
        return self.make_call("Email", "list_pops", params)

    def get_email_settings(self) -> Dict[str, Any]:
        """Get email client settings.
        
        Returns:
            API response
        """
        return self.make_call("Email", "get_client_settings")

    def update_quota(self, email: str, quota: int) -> Dict[str, Any]:
        """Update email account quota.
        
        Args:
            email: Full email address
            quota: New quota in MB
            
        Returns:
            API response
        """
        username, domain = self.split_email(email)
        params = {
            "username": username,
            "domain": domain,
            "quota": quota
        }
        return self.make_call("Email", "edit_pop_quota", params)

    def change_password(self, email: str, new_password: str) -> Dict[str, Any]:
        """Change email account password.
        
        Args:
            email: Full email address
            new_password: New password
            
        Returns:
            API response
        """
        username, domain = self.split_email(email)
        params = {
            "username": username,
            "domain": domain,
            "password": new_password
        }
        return self.make_call("Email", "passwd_pop", params)

    # Email Forwarder Management Methods
    def create_email_forwarder(
        self, 
        email: str, 
        destination: str
    ) -> Dict[str, Any]:
        """Create an email forwarder.
        
        Args:
            email: Source email address
            destination: Destination email address
            
        Returns:
            API response
        """
        username, domain = self.split_email(email)
        params = {
            "username": username,
            "domain": domain,
            "fwdopt": "fwd",
            "fwdemail": destination
        }
        return self.make_call("Email", "add_forwarder", params)

    def delete_email_forwarder(
        self, 
        email: str, 
        destination: str
    ) -> Dict[str, Any]:
        """Delete an email forwarder.
        
        Args:
            email: Source email address
            destination: Destination email address
            
        Returns:
            API response
        """
        params = {
            "address": email,
            "forwarder": destination
        }
        return self.make_call("Email", "delete_forwarder", params)

    def list_email_forwarders(self, domain: str) -> Dict[str, Any]:
        """List email forwarders for a domain.
        
        Args:
            domain: Domain to list forwarders for
            
        Returns:
            API response
        """
        params = {"domain": domain}
        return self.make_call("Email", "list_forwarders", params)
    
    def get_forwarder_settings(self) -> Dict[str, Any]:
        """Get email forwarder settings.
        
        Returns:
            API response
        """
        return self.make_call("Email", "get_forwarder_settings")