---
name: mysql_connect
description: Test MySQL database connectivity and execute queries for Ebury Brazil databases. Supports Cloud SQL and remote MySQL instances. Use when user says "test MySQL connection", "connect to database", "query MySQL", "check database access", "test Cloud SQL". Configured for ebb-money-flows-dev (34.39.195.206). Do NOT use for PostgreSQL (different driver needed) or production writes (read-only recommended).
license: CC-BY-4.0
metadata:
  author: Marcos Gomes
  version: 1.0.0
  requires:
    - pymysql
    - python-dotenv
  databases:
    - ebb-money-flows-dev (Cloud SQL)
---

# MySQL Connect Skill

Test MySQL database connectivity and execute queries safely.

## When to Use

Use this skill when:
- Test MySQL/Cloud SQL connectivity
- Verify database credentials
- Execute read-only queries
- Troubleshoot connection issues
- Check database availability

**Do NOT use for:**
- PostgreSQL databases (use psycopg2 instead)
- Production data modifications (read-only recommended)
- Schema migrations (use migration tools)
- Heavy data exports (use proper ETL tools)

## Prerequisites

- **pymysql** library installed
  ```bash
  pip install pymysql python-dotenv
  ```
- Database credentials
- Network access to database (VPN if required)

## Configuration

### Environment Variables

Create `.env` file:

```env
# Database connection
MYSQL_HOST=34.39.195.206
MYSQL_PORT=3306
MYSQL_USER=app_user
MYSQL_PASSWORD=secure_password
MYSQL_DATABASE=ebb_money_flows

# Optional
MYSQL_CHARSET=utf8mb4
MYSQL_CONNECT_TIMEOUT=10
```

### Cloud SQL Configuration

For **Google Cloud SQL**:

```env
# Option 1: Public IP with authorized networks
MYSQL_HOST=34.39.195.206
MYSQL_USER=app_user
MYSQL_PASSWORD=password

# Option 2: Cloud SQL Proxy
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
# Run proxy: cloud_sql_proxy -instances=PROJECT:REGION:INSTANCE=tcp:3306
```

## Usage

### Test Connection

```bash
cd skills/mysql_connect/
python main.py
```

### Output Example

```bash
$ python main.py
🔌 Testing MySQL connection...
Host: 34.39.195.206:3306
User: app_user
Database: ebb_money_flows

✓ Connection successful!
Server version: 8.0.31-google
Connection ping: OK

Testing query execution...
✓ Query executed successfully

Connection details:
  - Host: 34.39.195.206
  - Port: 3306
  - Database: ebb_money_flows
  - Character Set: utf8mb4
  - Connection ID: 12345
```

## Features

### 1. Connection Testing

Verifies:
- Host reachability
- Port accessibility
- Authentication credentials
- Database existence
- Network latency

### 2. Simple Queries

```python
# Example in main.py
cursor = connection.cursor()

# Check database version
cursor.execute("SELECT VERSION()")
version = cursor.fetchone()
print(f"MySQL version: {version[0]}")

# List tables
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
for table in tables:
    print(f"  - {table[0]}")

# Count records
cursor.execute("SELECT COUNT(*) FROM users")
count = cursor.fetchone()
print(f"Total users: {count[0]}")
```

### 3. Connection Health Check

```python
# Ping connection
connection.ping(reconnect=True)

# Get connection info
print(f"Thread ID: {connection.thread_id()}")
print(f "Character set: {connection.character_set_name()}")
```

## Common Tasks

### Test Connectivity

```python
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

try:
    connection = pymysql.connect(
        host=os.getenv('MYSQL_HOST'),
        port=int(os.getenv('MYSQL_PORT', 3306)),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE'),
        charset='utf8mb4',
        connect_timeout=10
    )
    print("✓ Connected successfully")
    connection.close()
except pymysql.Error as e:
    print(f"✗ Connection failed: {e}")
```

### Execute Read Query

```python
with connection.cursor() as cursor:
    # Safe read query
    sql = "SELECT id, name, email FROM users WHERE active = %s LIMIT 10"
    cursor.execute(sql, (True,))
    results = cursor.fetchall()
    
    for row in results:
        print(f"User {row[0]}: {row[1]} ({row[2]})")
```

### Check Database Schema

```python
# List all tables
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

# Describe table structure
cursor.execute("DESCRIBE users")
columns = cursor.fetchall()
for col in columns:
    print(f"{col[0]}: {col[1]}")
```

## Database Inventory

### ebb-money-flows-dev
- **Host**: 34.39.195.206 (Cloud SQL public IP)
- **Project**: ebb-money-flows-dev
- **Purpose**: Development database for money flows domain
- **Access**: VPN required or authorized networks
- **Services**: ebb-account, ebb-pix-spi, ebb-conciliacao

## Troubleshooting

### Connection Timeout

**Error**: `(2003, "Can't connect to MySQL server on '34.39.195.206' (110)")` 

**Solutions**:
1. **Check VPN**: Ensure VPN is connected
   ```bash
   ping 34.39.195.206
   ```

2. **Verify authorized networks** (Cloud SQL):
   - Go to Cloud SQL instance
   - Check "Connections" → "Authorized networks"
   - Add your IP if missing

3. **Test port accessibility**:
   ```bash
   nc -zv 34.39.195.206 3306
   telnet 34.39.195.206 3306
   ```

4. **Use Cloud SQL Proxy**:
   ```bash
   cloud_sql_proxy -instances=ebb-money-flows-dev:southamerica-east1:main=tcp:3306
   
   # Then connect to localhost
   MYSQL_HOST=127.0.0.1 python main.py
   ```

### Authentication Failed

**Error**: `(1045, "Access denied for user 'app_user'@'...' (using password: YES)")`

**Solutions**:
1. Verify username in `.env`
2. Check password (no typos, special characters escaped)
3. Verify user exists in database:
   ```sql
   SELECT user, host FROM mysql.user WHERE user = 'app_user';
   ```
4. Check user permissions:
   ```sql
   SHOW GRANTS FOR 'app_user'@'%';
   ```

### Database Not Found

**Error**: `(1049, "Unknown database 'ebb_money_flows'")`

**Solutions**:
1. Verify database name spelling
2. List available databases:
   ```sql
   SHOW DATABASES;
   ```
3. Create database if needed (with proper permissions)

### SSL/TLS Issues

**Error**: SSL connection required

**Solution**: Enable SSL in connection:
```python
connection = pymysql.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    ssl={'ssl': True}  # Enable SSL
)
```

## Security Notes

### Credentials

- `.env` file is git-ignored
- Never commit database passwords
- Use Secret Manager for production
- Rotate passwords regularly
- Use least-privilege accounts (read-only when possible)

### Read-Only User

Create read-only user for testing:

```sql
CREATE USER 'readonly'@'%' IDENTIFIED BY 'secure_password';
GRANT SELECT ON ebb_money_flows.* TO 'readonly'@'%';
FLUSH PRIVILEGES;
```

### Query Safety

```python
# ✓ GOOD: Use parameterized queries
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# ✗ BAD: SQL injection risk
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

## Cloud SQL Proxy (Recommended)

### Setup

```bash
# Install Cloud SQL Proxy
curl -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.8.0/cloud-sql-proxy.linux.amd64
chmod +x cloud-sql-proxy

# Start proxy
./cloud-sql-proxy ebb-money-flows-dev:southamerica-east1:main
```

### Benefits
- No IP allowlisting needed
- Encrypted connection
- IAM authentication support
- Easier local development

### Configuration with Proxy
```env
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=app_user
MYSQL_PASSWORD=password
MYSQL_DATABASE=ebb_money_flows
```

## Common Queries

### Database Health

```sql
-- Show database size
SELECT 
    table_schema AS 'Database',
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)'
FROM information_schema.tables
WHERE table_schema = 'ebb_money_flows'
GROUP BY table_schema;

-- Show table sizes
SELECT 
    table_name AS 'Table',
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.tables
WHERE table_schema = 'ebb_money_flows'
ORDER BY (data_length + index_length) DESC;

-- Active connections
SHOW PROCESSLIST;

-- Server status
SHOW STATUS LIKE 'Threads_connected';
SHOW STATUS LIKE 'Uptime';
```

## Related Skills

- **kubernetes_debug**: For application database connection issues
- **ssh_connect**: For MySQL CLI access via bastion host
- **firestore_query**: For NoSQL database queries

## References

- PyMySQL documentation: https://pymysql.readthedocs.io/
- Cloud SQL Proxy: https://cloud.google.com/sql/docs/mysql/sql-proxy
- MySQL best practices: Internal database wiki
