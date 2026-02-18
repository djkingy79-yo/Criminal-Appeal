# Configuration Guide

This document provides detailed instructions for configuring the Criminal Appeal application, including database setup, firewall configuration, and network security.

## Table of Contents

1. [Database Configuration](#database-configuration)
2. [Firewall Configuration](#firewall-configuration)
3. [Network Security](#network-security)
4. [Testing Connectivity](#testing-connectivity)
5. [Troubleshooting](#troubleshooting)

## Database Configuration

### Environment Variables

The application uses environment variables to securely manage database credentials. Copy `.env.example` to `.env` and configure the following variables:

```bash
# Database Connection Settings
DB_HOST=localhost              # Database server hostname or IP address
DB_PORT=5432                   # Database server port (default: 5432 for PostgreSQL)
DB_NAME=criminal_appeal        # Database name
DB_USER=postgres               # Database username
DB_PASSWORD=your-password-here # Database password (keep this secure!)

# Connection Pool Settings
DB_POOL_SIZE=5                 # Number of connections to maintain in the pool
DB_MAX_OVERFLOW=10             # Maximum number of connections above pool_size
DB_POOL_TIMEOUT=30             # Seconds to wait before timing out on pool
DB_CONNECT_TIMEOUT=10          # Seconds to wait for database connection
```

### Setting Up the Database

1. **Install PostgreSQL**:
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   
   # macOS with Homebrew
   brew install postgresql
   
   # Start the service
   sudo systemctl start postgresql  # Linux
   brew services start postgresql   # macOS
   ```

2. **Create Database and User**:
   ```bash
   # Switch to postgres user
   sudo -u postgres psql
   
   # Create database
   CREATE DATABASE criminal_appeal;
   
   # Create user with password
   CREATE USER postgres WITH PASSWORD 'your-secure-password';
   
   # Grant privileges
   GRANT ALL PRIVILEGES ON DATABASE criminal_appeal TO postgres;
   
   # Exit psql
   \q
   ```

3. **Configure PostgreSQL for Remote Access** (if needed):
   
   Edit `postgresql.conf`:
   ```conf
   # Find and modify the listen_addresses setting
   listen_addresses = '*'  # Listen on all network interfaces
   # OR specify specific IPs:
   # listen_addresses = 'localhost,192.168.1.100'
   ```
   
   Edit `pg_hba.conf` to allow connections:
   ```conf
   # Allow connections from specific IP ranges
   host    all             all             192.168.1.0/24          md5
   host    all             all             10.0.0.0/8              md5
   
   # For development only (NOT recommended for production)
   # host    all             all             0.0.0.0/0               md5
   ```
   
   Restart PostgreSQL:
   ```bash
   sudo systemctl restart postgresql  # Linux
   brew services restart postgresql   # macOS
   ```

## Firewall Configuration

### Whitelisting IP Addresses

#### On Ubuntu/Debian (UFW)

1. **Allow specific IP to access PostgreSQL**:
   ```bash
   # Allow single IP
   sudo ufw allow from 192.168.1.100 to any port 5432
   
   # Allow IP range (subnet)
   sudo ufw allow from 192.168.1.0/24 to any port 5432
   
   # Allow multiple specific IPs
   sudo ufw allow from 10.0.0.5 to any port 5432
   sudo ufw allow from 10.0.0.10 to any port 5432
   ```

2. **Allow API access (HTTP/HTTPS)**:
   ```bash
   sudo ufw allow 5000/tcp  # Flask API
   sudo ufw allow 80/tcp    # HTTP
   sudo ufw allow 443/tcp   # HTTPS
   ```

3. **Enable firewall**:
   ```bash
   sudo ufw enable
   sudo ufw status verbose
   ```

#### On CentOS/RHEL (firewalld)

1. **Allow specific IP to access PostgreSQL**:
   ```bash
   # Add rich rule for specific IP
   sudo firewall-cmd --permanent --add-rich-rule='
     rule family="ipv4"
     source address="192.168.1.100"
     port protocol="tcp" port="5432" accept'
   
   # For IP range
   sudo firewall-cmd --permanent --add-rich-rule='
     rule family="ipv4"
     source address="192.168.1.0/24"
     port protocol="tcp" port="5432" accept'
   ```

2. **Allow API ports**:
   ```bash
   sudo firewall-cmd --permanent --add-port=5000/tcp
   sudo firewall-cmd --permanent --add-service=http
   sudo firewall-cmd --permanent --add-service=https
   ```

3. **Reload firewall**:
   ```bash
   sudo firewall-cmd --reload
   sudo firewall-cmd --list-all
   ```

#### On Windows (Windows Firewall)

1. **Open Windows Firewall with Advanced Security**

2. **Create Inbound Rule for PostgreSQL**:
   - Click "Inbound Rules" → "New Rule"
   - Rule Type: Port
   - Protocol: TCP, Port: 5432
   - Action: Allow the connection
   - Profile: Select appropriate profiles (Domain, Private, Public)
   - Name: "PostgreSQL Database Access"
   - Description: "Allow access to PostgreSQL on port 5432"

3. **Configure IP Restrictions**:
   - Right-click the rule → Properties
   - Scope tab → Remote IP address
   - Select "These IP addresses" and add specific IPs or ranges
   - Example: 192.168.1.100, 192.168.1.0/24

### Opening Required Ports

| Service         | Port  | Protocol | Purpose                          |
|-----------------|-------|----------|----------------------------------|
| PostgreSQL      | 5432  | TCP      | Database connections             |
| Flask API       | 5000  | TCP      | Application API endpoints        |
| HTTP            | 80    | TCP      | Web server (if applicable)       |
| HTTPS           | 443   | TCP      | Secure web server (if applicable)|

### Cloud Provider Firewall Configuration

#### AWS Security Groups

```bash
# Using AWS CLI
aws ec2 authorize-security-group-ingress \
    --group-id sg-xxxxxxxxx \
    --protocol tcp \
    --port 5432 \
    --cidr 192.168.1.0/24

aws ec2 authorize-security-group-ingress \
    --group-id sg-xxxxxxxxx \
    --protocol tcp \
    --port 5000 \
    --cidr 0.0.0.0/0
```

#### Google Cloud Platform (GCP) Firewall Rules

```bash
# Create firewall rule for PostgreSQL
gcloud compute firewall-rules create allow-postgresql \
    --allow tcp:5432 \
    --source-ranges 192.168.1.0/24 \
    --description "Allow PostgreSQL access from specific subnet"

# Create firewall rule for API
gcloud compute firewall-rules create allow-api \
    --allow tcp:5000 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow API access"
```

#### Azure Network Security Groups

```bash
# Create NSG rule for PostgreSQL
az network nsg rule create \
    --resource-group myResourceGroup \
    --nsg-name myNSG \
    --name allow-postgresql \
    --priority 1000 \
    --source-address-prefixes 192.168.1.0/24 \
    --destination-port-ranges 5432 \
    --access Allow \
    --protocol Tcp
```

## Network Security

### Best Practices

1. **Principle of Least Privilege**:
   - Only whitelist IPs that absolutely need access
   - Use specific IP addresses rather than broad ranges when possible
   - Regularly review and update whitelist

2. **Use SSL/TLS for Database Connections**:
   ```python
   # In config.py, modify get_database_url() to include SSL
   return f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}?sslmode=require"
   ```

3. **Change Default Ports** (Optional but recommended):
   - Consider using non-standard ports to reduce automated attacks
   - Update `DB_PORT` in `.env` file accordingly

4. **Enable Database Authentication**:
   - Always use strong passwords
   - Consider certificate-based authentication for production
   - Implement password rotation policies

5. **Monitor and Log**:
   - Enable PostgreSQL logging
   - Monitor failed connection attempts
   - Set up alerts for suspicious activity

6. **Network Segmentation**:
   - Place database servers in a private subnet
   - Use a bastion host or VPN for administrative access
   - Keep application and database tiers separate

### VPN Configuration (Recommended for Production)

For production environments, consider using a VPN for database access:

1. **OpenVPN Setup**:
   ```bash
   # Install OpenVPN
   sudo apt install openvpn
   
   # Configure client
   sudo openvpn --config client.ovpn
   ```

2. **SSH Tunnel** (Quick alternative):
   ```bash
   # Create SSH tunnel to database server
   ssh -L 5432:localhost:5432 user@database-server
   
   # Update DB_HOST in .env
   DB_HOST=localhost
   ```

## Testing Connectivity

### Using the Test Script

Run the provided test script to verify database connectivity:

```bash
# Make the script executable
chmod +x test_db_connection.py

# Run the test
python test_db_connection.py
```

The script will:
- Validate configuration variables
- Test connection using psycopg2
- Test connection using SQLAlchemy
- Display detailed error messages if connection fails

### Manual Testing

#### Using psql Command Line

```bash
# Test connection
psql -h localhost -p 5432 -U postgres -d criminal_appeal

# Or with full connection string
psql postgresql://postgres:password@localhost:5432/criminal_appeal
```

#### Using Python

```python
import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="criminal_appeal",
        user="postgres",
        password="your-password"
    )
    print("Connection successful!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
```

### Network Connectivity Tests

1. **Test port accessibility**:
   ```bash
   # Using telnet
   telnet database-server 5432
   
   # Using nc (netcat)
   nc -zv database-server 5432
   
   # Using nmap
   nmap -p 5432 database-server
   ```

2. **Check firewall rules**:
   ```bash
   # UFW
   sudo ufw status verbose
   
   # firewalld
   sudo firewall-cmd --list-all
   
   # iptables
   sudo iptables -L -n -v
   ```

## Troubleshooting

### Common Issues and Solutions

#### 1. Connection Refused

**Symptoms**: `Connection refused` error when trying to connect

**Solutions**:
- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Check if PostgreSQL is listening: `sudo netstat -tlnp | grep 5432`
- Verify firewall allows connections
- Check `postgresql.conf` has correct `listen_addresses`

#### 2. Timeout Errors

**Symptoms**: Connection times out

**Solutions**:
- Check firewall rules on both client and server
- Verify network connectivity: `ping database-server`
- Check if port is accessible: `telnet database-server 5432`
- Increase `DB_CONNECT_TIMEOUT` in `.env`

#### 3. Authentication Failed

**Symptoms**: `authentication failed for user` error

**Solutions**:
- Verify username and password in `.env`
- Check `pg_hba.conf` allows the connection method (md5, trust, etc.)
- Ensure user has proper database permissions
- Verify password special characters are properly escaped

#### 4. Database Does Not Exist

**Symptoms**: `database "criminal_appeal" does not exist`

**Solutions**:
- Create the database: `CREATE DATABASE criminal_appeal;`
- Verify `DB_NAME` in `.env` matches actual database name
- Check user has access to the database

#### 5. SSL/TLS Errors

**Symptoms**: SSL-related errors

**Solutions**:
- If SSL is not configured, remove `sslmode` from connection string
- Install required certificates
- Set `sslmode=disable` for development (not recommended for production)

### Getting Help

If you continue to experience issues:

1. Check the logs:
   - PostgreSQL logs: `/var/log/postgresql/`
   - Application logs
   - System logs: `journalctl -xe`

2. Review the error messages in the test script output

3. Consult the [PostgreSQL documentation](https://www.postgresql.org/docs/)

4. Open an issue in the repository with:
   - Error messages
   - Configuration (without sensitive data)
   - Steps to reproduce

## Security Checklist

Before deploying to production:

- [ ] Change all default passwords
- [ ] Use strong, unique passwords for database
- [ ] Enable SSL/TLS for database connections
- [ ] Implement firewall rules with IP whitelisting
- [ ] Use environment variables for all sensitive data
- [ ] Never commit `.env` file to version control
- [ ] Regularly update and patch the database server
- [ ] Enable database connection logging
- [ ] Implement backup and recovery procedures
- [ ] Use VPN or bastion host for database access
- [ ] Review and audit firewall rules regularly
- [ ] Implement intrusion detection/prevention
- [ ] Set up monitoring and alerting

## Additional Resources

- [PostgreSQL Security Best Practices](https://www.postgresql.org/docs/current/security.html)
- [Flask Security Considerations](https://flask.palletsprojects.com/en/2.3.x/security/)
- [OWASP Database Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Database_Security_Cheat_Sheet.html)
- [Cloud Security Best Practices](https://aws.amazon.com/security/best-practices/)
