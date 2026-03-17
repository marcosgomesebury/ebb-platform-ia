---
name: rdp_connect
description: Automated RDP connection to Windows servers for Ebury Brazil infrastructure. Supports multiple server configurations with environment variables. Use when user says "connect to Windows server", "RDP to conciliacao", "access Windows machine", "remote desktop". Prioritizes RDP_SERVER_EBB_CONCILIACAO_USER for specific server access. Do NOT use for SSH connections (use ssh_connect skill) or Linux servers (use ssh_connect skill).
license: CC-BY-4.0
metadata:
  author: Marcos Gomes
  version: 1.0.0
  requires:
    - xfreerdp
    - python-dotenv
  servers:
    - 10.23.129.4 (Windows/conciliacao)
---

# RDP Connect Skill

Automated RDP (Remote Desktop Protocol) connection to Windows servers in Ebury Brazil infrastructure.

## When to Use

Use this skill when:
- Need to connect to Windows servers
- Access reconciliation (conciliacao) server
- Remote desktop access required
- Windows-based troubleshooting

**Do NOT use for:**
- SSH connections to Linux (use ssh_connect skill)
- Database connections (use mysql_connect skill)
- Kubernetes access (use kubernetes_debug skill)

## Prerequisites

- **xfreerdp** installed (RDP client for Linux)
  ```bash
  sudo apt-get install freerdp2-x11
  ```
- Environment variables configured in `.env`
- Network access to target servers

## Configuration

### Environment Variables

Create `.env` file in skill directory:

```env
# Primary server IP
RDP_SERVER=10.23.129.4

# User for conciliacao server (prioritized)
RDP_SERVER_EBB_CONCILIACAO_USER=marcos_gomes

# Alternative user
RDP_USER=marcos

# Password
RDP_PASS=your_password_here

# Domain (optional)
RDP_DOMAIN=EBURY
```

### Variable Priority

Script prioritizes variables in this order:
1. `RDP_SERVER_EBB_CONCILIACAO_USER` (specific user for conciliacao server)
2. `RDP_USER` (fallback user)

This allows different credentials for different servers.

## Usage

### Basic Connection

```bash
cd skills/rdp_connect/
python main.py
```

### What Happens

1. Loads environment variables from `.env`
2. Determines server IP from `RDP_SERVER`
3. Selects username (prioritizes `RDP_SERVER_EBB_CONCILIACAO_USER`)
4. Executes `xfreerdp` with configured credentials
5. Opens RDP session

### xfreerdp Options Used

```bash
xfreerdp /v:<server> /u:<username> /p:<password> \
  /cert-ignore \           # Ignore certificate warnings
  +clipboard \             # Enable clipboard sharing
  /dynamic-resolution      # Auto-adjust resolution
```

## Server Inventory

### Conciliação Server
- **IP**: 10.23.129.4
- **Purpose**: Reconciliation operations
- **User**: marcos_gomes (RDP_SERVER_EBB_CONCILIACAO_USER)
- **Access**: RDP only

## Troubleshooting

### Connection Refused

**Error**: `unable to connect to <server>:3389`

**Solutions**:
1. Verify server IP is correct
2. Check VPN connection (if required)
3. Verify firewall allows RDP (port 3389)
4. Test with ping:
   ```bash
   ping 10.23.129.4
   ```

### Authentication Failed

**Error**: `Authentication failure`

**Solutions**:
1. Verify credentials in `.env`
2. Check password for special characters (escape if needed)
3. Verify domain is correct (or omit if not needed)
4. Try with explicit domain: `DOMAIN\username`

### Certificate Warnings

**Error**: Certificate verification failed

**Solution**: Script uses `/cert-ignore` flag to bypass self-signed certificates. This is normal for internal infrastructure.

### Special Characters in Password

If password contains special characters, they may need escaping:

```env
# If password contains: ! @ # $ % & * ( )
# Wrap in single quotes in .env
RDP_PASS='P@ssw0rd!123'
```

## Security Notes

### Password Storage

- `.env` file is **git-ignored** (never commit)
- Use `.env.example` as template (no real credentials)
- Rotate passwords regularly
- Consider using secret manager for production

### Access Control

- RDP access requires VPN connection
- Credentials are role-based (specific users per server)
- Audit RDP sessions regularly

## Common Tasks

### Connect to Conciliação Server
```bash
# Ensure .env has correct values
RDP_SERVER=10.23.129.4
RDP_SERVER_EBB_CONCILIACAO_USER=marcos_gomes
RDP_PASS=<your_password>

# Connect
python main.py
```

### Update Credentials
```bash
# Edit .env file
nano .env

# Update password
RDP_PASS=new_password

# Reconnect
python main.py
```

### Test Connection
```bash
# Check server is reachable
ping 10.23.129.4

# Check RDP port is open
nc -zv 10.23.129.4 3389
```

## Output Example

```bash
$ python main.py
🔌 Connecting to RDP server...
Server: 10.23.129.4
User: marcos_gomes
Opening RDP session...
✓ Connected successfully
```

## Related Skills

- **ssh_connect**: For Linux server access
- **mysql_connect**: For database connections
- **kubernetes_debug**: For Kubernetes troubleshooting

## References

- xfreerdp documentation: `man xfreerdp`
- Windows Server access procedures: Internal wiki
- VPN setup: IT documentation
