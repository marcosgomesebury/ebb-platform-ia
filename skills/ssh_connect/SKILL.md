---
name: ssh_connect
description: Interactive SSH connection to Linux servers with password or key-based authentication. Supports command execution, file transfer, and interactive sessions. Use when user says "SSH to server", "connect to Linux", "access remote server", "run command on server". Supports server 10.23.129.3 (marcos user). Do NOT use for RDP/Windows (use rdp_connect skill) or database connections (use mysql_connect skill).
license: CC-BY-4.0
metadata:
  author: Marcos Gomes
  version: 1.0.0
  requires:
    - paramiko
    - python-dotenv
  servers:
    - 10.23.129.3 (Linux/SSH)
---

# SSH Connect Skill

Interactive SSH connection to Linux servers using Python paramiko library.

## When to Use

Use this skill when:
- Need SSH access to Linux servers
- Execute commands on remote machines
- Interactive shell session required
- File transfer via SFTP
- Automated server management

**Do NOT use for:**
- Windows RDP connections (use rdp_connect skill)
- Direct database queries (use mysql_connect skill)
- Kubernetes access (use kubernetes_debug skill)

## Prerequisites

- **paramiko** library installed
  ```bash
  pip install paramiko python-dotenv
  ```
- SSH access to target servers
- Valid credentials (password or SSH key)

## Configuration

### Environment Variables

Create `.env` file:

```env
# Server details
SSH_HOST=10.23.129.3
SSH_PORT=22
SSH_USER=marcos

# Authentication (choose one)
SSH_PASS=your_password_here
# OR
SSH_KEY_PATH=/home/user/.ssh/id_rsa
```

### Authentication Methods

#### 1. Password Authentication
```env
SSH_HOST=10.23.129.3
SSH_USER=marcos
SSH_PASS=secure_password
```

#### 2. SSH Key Authentication (Recommended)
```env
SSH_HOST=10.23.129.3
SSH_USER=marcos
SSH_KEY_PATH=/home/marcos/.ssh/id_rsa
```

## Usage

### Interactive Mode

```bash
cd skills/ssh_connect/
python main.py
```

**Interactive session allows**:
- Run any command
- Navigate directories
- View files
- Execute scripts
- Type `exit` to disconnect

### Example Session

```bash
$ python main.py
🔌 Connecting to SSH server...
Host: 10.23.129.3
User: marcos
✓ Connected successfully

marcos@server:~$ ls -la
total 48
drwxr-xr-x 5 marcos marcos 4096 Mar 16 10:30 .
drwxr-xr-x 3 root   root   4096 Jan 15 08:00 ..
-rw-r--r-- 1 marcos marcos  220 Jan 15 08:00 .bash_logout
...

marcos@server:~$ uptime
 10:30:15 up 45 days, 3:24, 2 users, load average: 0.15, 0.20, 0.18

marcos@server:~$ exit
Disconnected.
```

## Features

### 1. Command Execution

Execute any shell command:
```bash
marcos@server:~$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   25G   23G  53% /
...
```

### 2. File Navigation

```bash
marcos@server:~$ cd /var/log
marcos@server:/var/log$ ls -lh
total 2.5M
-rw-r--r-- 1 root root 1.2M Mar 16 10:00 syslog
...
```

### 3. Log Viewing

```bash
marcos@server:~$ tail -f /var/log/application.log
[2026-03-16 10:30:00] INFO: Application started
[2026-03-16 10:30:05] DEBUG: Processing request...
^C (Ctrl+C to stop)
```

### 4. Process Management

```bash
marcos@server:~$ ps aux | grep python
marcos   12345  0.5  2.1 ...

marcos@server:~$ kill -9 12345
```

## Common Tasks

### Check Server Resources

```bash
marcos@server:~$ free -h
              total        used        free      shared  buff/cache   available
Mem:            16G         8G         2G         1G         5G          6G
Swap:          2.0G        100M        1.9G

marcos@server:~$ df -h | grep -v tmpfs
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   25G   23G  53% /
```

### View Logs

```bash
# System logs
marcos@server:~$ sudo tail -100 /var/log/syslog

# Application logs
marcos@server:~$ tail -50 /app/logs/app.log

# Follow logs in real-time
marcos@server:~$ tail -f /var/log/application.log
```

### Check Network Connectivity

```bash
marcos@server:~$ ping -c 4 google.com
PING google.com (142.250.217.46) 56(84) bytes of data.
64 bytes from gru06s65-in-f14.1e100.net: icmp_seq=1 ttl=117 time=2.45 ms
...

marcos@server:~$ curl -I https://api.example.com
HTTP/2 200
...
```

### Service Management

```bash
# Check service status
marcos@server:~$ sudo systemctl status nginx
● nginx.service - A high performance web server
   Active: active (running) since Mon 2026-01-15 08:00:00 -03

# Restart service
marcos@server:~$ sudo systemctl restart nginx

# View service logs
marcos@server:~$ sudo journalctl -u nginx -f
```

## Server Inventory

### Server: 10.23.129.3
- **Type**: Linux (Ubuntu/Debian)
- **Purpose**: General purpose server
- **User**: marcos
- **Access**: SSH (password or key)
- **Port**: 22

## Troubleshooting

### Connection Timeout

**Error**: `Socket timeout` or `Connection refused`

**Solutions**:
1. Verify server IP is correct
2. Check VPN connection
3. Verify firewall allows SSH (port 22)
4. Test connectivity:
   ```bash
   ping 10.23.129.3
   telnet 10.23.129.3 22
   ```

### Authentication Failed

**Error**: `Authentication failed`

**Solutions**:
1. Verify username in `.env`
2. Check password (no typos)
3. If using SSH key:
   - Verify key path is correct
   - Check key permissions: `chmod 600 ~/.ssh/id_rsa`
   - Ensure public key is in `~/.ssh/authorized_keys` on server

### Permission Denied

**Error**: `Permission denied` when running commands

**Solutions**:
1. Check user has required permissions
2. Use `sudo` for privileged commands
3. Verify file/directory ownership

### Host Key Verification

**Warning**: `The authenticity of host '10.23.129.3' can't be established`

**Solution**: Script uses `AutoAddPolicy` to automatically accept new host keys. First connection will add to `~/.ssh/known_hosts`.

## Security Notes

### Password Storage
- `.env` file is git-ignored
- Never commit real credentials
- Use SSH keys instead of passwords when possible
- Rotate credentials regularly

### SSH Key Best Practices
```bash
# Generate new SSH key pair
ssh-keygen -t ed25519 -C "marcos@ebury"

# Copy public key to server
ssh-copy-id -i ~/.ssh/id_ed25519.pub marcos@10.23.129.3

# Test connection
ssh -i ~/.ssh/id_ed25519 marcos@10.23.129.3
```

## Advanced Usage

### File Transfer (SFTP)

```python
# In Python script
import paramiko

client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('10.23.129.3', username='marcos', password='password')

# Upload file
sftp = client.open_sftp()
sftp.put('/local/file.txt', '/remote/file.txt')

# Download file
sftp.get('/remote/data.csv', '/local/data.csv')

sftp.close()
client.close()
```

### Automated Command Execution

```python
# Execute multiple commands
commands = [
    'uptime',
    'df -h',
    'free -h'
]

for cmd in commands:
    stdin, stdout, stderr = client.exec_command(cmd)
    print(stdout.read().decode())
```

## Related Skills

- **rdp_connect**: For Windows server access
- **mysql_connect**: For database connections
- **kubernetes_debug**: For K8s troubleshooting

## References

- Paramiko documentation: https://www.paramiko.org/
- SSH best practices: Internal security wiki
- Server inventory: IT documentation
