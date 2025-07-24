# cPanel MCP Server

An MCP (Model Context Protocol) server that provides AI assistants with comprehensive cPanel management capabilities. This server enables automated email account management and DNS zone management through cPanel's UAPI and WHM API.

## Features

### Email Management
- **Email Account Management**: Create, delete, and list email accounts
- **Password Management**: Change passwords for existing email accounts
- **Quota Management**: Set and update mailbox storage limits
- **Email Forwarding**: Create, delete, and list email forwarders
- **Client Settings**: Retrieve email client configuration settings

### DNS Management
- **DNS Zone Management**: View, add, edit, and delete DNS records
- **Multi-Record Support**: A, AAAA, CNAME, MX, TXT, NS, PTR, SRV, CAA, TLSA records
- **Line-Based Editing**: Precise record management using zone file line numbers
- **TTL Configuration**: Customizable time-to-live settings

### Security & Integration
- **Dual API Support**: Uses both cPanel UAPI and WHM API
- **Secure Authentication**: API token-based authentication
- **Environment Configuration**: Secure configuration via .env files
- **Professional Structure**: Modular codebase with proper error handling

## Available Tools

### Email Account Operations
- `add_email_account(email, password, quota=0)` - Create a new email account
- `delete_email_account(email)` - Delete an existing email account
- `list_email_accounts(domain)` - List all email accounts for a domain
- `change_password(email, new_password)` - Change an email account password
- `update_quota(email, quota)` - Update mailbox size limit
- `get_email_settings()` - Get email client configuration settings

### Email Forwarding Operations
- `create_email_forwarder(email, destination)` - Create an email forwarder
- `delete_email_forwarder(email, destination)` - Delete an email forwarder
- `list_email_forwarders(domain)` - List all forwarders for a domain

### DNS Management Operations
- `get_dns_records(domain)` - Retrieve all DNS records for a domain with line numbers
- `add_dns_record(domain, name, record_type, address, ttl=3600, record_class="IN")` - Add a new DNS record
- `edit_dns_record(domain, line, name, record_type, address, ttl=3600, record_class="IN")` - Edit an existing DNS record
- `delete_dns_record(domain, line)` - Delete a DNS record by line number

#### Supported DNS Record Types
- **A** - IPv4 address records
- **AAAA** - IPv6 address records  
- **CNAME** - Canonical name records
- **MX** - Mail exchange records
- **TXT** - Text records
- **NS** - Name server records
- **PTR** - Pointer records
- **SRV** - Service records
- **CAA** - Certificate Authority Authorization
- **TLSA** - Transport Layer Security Authentication

## Requirements

- Python 3.10 or higher
- cPanel hosting account with UAPI access
- WHM access with root privileges (for DNS management)
- Valid cPanel/WHM API token

## Installation

### Using uv (Recommended)

```bash
uv run --from git+https://github.com/ashrobertsdragon/cpanel-mcp.git cpanel-mcp
```

### Local Development

```bash
git clone https://github.com/ashrobertsdragon/cpanel-mcp.git
cd cpanel-mcp
cp .env.example .env
# Edit .env with your credentials
uv run python server.py
```

## Configuration

The server supports configuration via environment variables or `.env` file:

### Required Variables

- `CPANEL_USERNAME` - Your cPanel username
- `CPANEL_HOSTNAME` - Your cPanel/WHM hostname (e.g., `server.example.com`)
- `CPANEL_API_TOKEN` - Your cPanel/WHM API token

### Optional Variables

- `CPANEL_PORT` - cPanel port (default: 2083)
- `CPANEL_SSL` - Enable SSL connection (default: true)

### Environment File Setup

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your actual credentials:
   ```env
   CPANEL_USERNAME=your_cpanel_username
   CPANEL_HOSTNAME=your.server.hostname.com
   CPANEL_API_TOKEN=your_api_token_here
   CPANEL_PORT=2083
   CPANEL_SSL=true
   ```

## Getting API Tokens

### For cPanel UAPI (Email Management)
1. Log into your cPanel account
2. Navigate to **Security** → **Manage API Tokens**
3. Click **Create Token**
4. Give it a descriptive name (e.g., "MCP Email Server")
5. Set appropriate restrictions if needed
6. Copy the generated token

### For WHM API (DNS Management)
1. Log into your WHM account as root
2. Navigate to **Development** → **Manage API Tokens**
3. Click **Generate Token**
4. Give it a descriptive name (e.g., "MCP DNS Server")
5. Set appropriate ACL restrictions for DNS functions
6. Copy the generated token

**Note**: For full functionality, you need WHM root access. The same API token can be used for both cPanel and WHM if you have root privileges.

## Usage

### MCP Client Configuration

Add the server to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "cpanel-mcp": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/your-username/cpanel-mcp.git", "cpanel-mcp"],
      "env": {
        "CPANEL_USERNAME": "your_cpanel_username",
        "CPANEL_HOSTNAME": "your.server.hostname.com",
        "CPANEL_API_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

## Example Usage

Once connected to an MCP client, you can use natural language commands:

### Email Management Examples
- "Create a new email account support@example.com with password SecurePass123"
- "List all email accounts for example.com"
- "Set up email forwarding from info@example.com to admin@example.com"
- "Change the password for user@example.com to NewPassword456"
- "Delete the email account temp@example.com"
- "Update the quota for sales@example.com to 1000 MB"

### DNS Management Examples
- "Show me all DNS records for example.com"
- "Add an A record for app.example.com pointing to 192.168.1.100"
- "Create a CNAME record for www.example.com pointing to example.com"
- "Add an MX record for example.com with priority 10 pointing to mail.example.com"
- "Edit the DNS record on line 15 to point to a different IP address"
- "Delete the DNS record on line 23"
- "Add a TXT record for SPF: 'v=spf1 include:_spf.google.com ~all'"

## Security Considerations

- **API Token Security**: Never commit your API token to version control
- **Environment Variables**: Use environment variables or secure secret management
- **Network Security**: Ensure your cPanel server supports HTTPS (SSL)
- **Password Policy**: Use strong passwords for email accounts

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify your API token is correct and active
   - Check that your username matches your cPanel account
   - Ensure the hostname includes the correct domain/subdomain

2. **Connection Issues**
   - Verify the hostname and port are correct
   - Check if SSL is properly configured
   - Ensure your server allows API connections

3. **Permission Errors**
   - Verify your cPanel account has email management permissions
   - Check if the API token has the necessary privileges

## API Reference

The server uses both cPanel's UAPI and WHM API:

### cPanel UAPI (Email Management)
- **Email Module**: Core email account management
- **Functions Used**:
  - `add_pop` - Create email account
  - `del_pop` - Delete email account  
  - `list_pops` - List email accounts
  - `passwd_pop` - Change password
  - `edit_pop_quota` - Update quota
  - `get_client_settings` - Get email settings
  - `add_forwarder` - Create forwarder
  - `delete_forwarder` - Delete forwarder
  - `list_forwarders` - List forwarders

### WHM API (DNS Management)
- **DNS Zone Management**: DNS record operations
- **Functions Used**:
  - `dumpzone` - Get all DNS records for a domain
  - `addzonerecord` - Add a new DNS record
  - `editzonerecord` - Edit an existing DNS record
  - `removezonerecord` - Delete a DNS record

### Project Structure
```
src/
├── config.py          # Configuration management with validation
├── cpanel.py           # cPanel UAPI and WHM API client
├── routes.py           # MCP tool route definitions
└── server.py           # Main server and initialization
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Check the troubleshooting section above
- Review cPanel's UAPI documentation
- Open an issue in the project repository

## Changelog

### v0.2.0

- **DNS Management**: Complete DNS zone management with WHM API integration
- **Dual API Support**: Both cPanel UAPI and WHM API support  
- **Professional Structure**: Modular codebase with flat src/ structure
- **Enhanced Configuration**: .env file support with validation
- **Expanded Record Types**: Support for A, AAAA, CNAME, MX, TXT, NS, PTR, SRV, CAA, TLSA
- **Line-Based Editing**: Precise DNS record management using zone file line numbers
- **Improved Error Handling**: Comprehensive validation and error reporting

### v0.1.0

- Initial release
- Basic email account management
- Email forwarding support
- Quota and password management
- MCP integration