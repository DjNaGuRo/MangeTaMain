# Database Configuration Guide

## Environment Variables Setup

The database connection now uses environment variables for better security and configuration management.

### Method 1: Using a .env file (Recommended)

1. Copy the template file:
   ```bash
   cp .env.template .env
   ```

2. Edit the `.env` file with your actual database credentials:
   ```bash
   # Database Configuration
   DB_HOST=your-database-host.com
   DB_PORT=5432
   DB_NAME=your_database_name
   DB_USER=your_username
   DB_PASSWORD=your_secure_password
   DB_SSLMODE=require
   ```

3. The application will automatically load these variables when it starts.

### Method 2: System Environment Variables

Set the environment variables in your shell:

```bash
export DB_HOST=your-database-host.com
export DB_PORT=5432
export DB_NAME=your_database_name
export DB_USER=your_username
export DB_PASSWORD=your_secure_password
export DB_SSLMODE=require
```

### Method 3: Docker Environment Variables

If using Docker, you can pass environment variables:

```bash
docker run -e DB_HOST=your-host -e DB_USER=user -e DB_PASSWORD=pass your-app
```

## Required Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DB_HOST` | Database host | **None** | **Yes** |
| `DB_PORT` | Database port | **None** | **Yes** |
| `DB_NAME` | Database name | **None** | **Yes** |
| `DB_USER` | Database user | **None** | **Yes** |
| `DB_PASSWORD` | Database password | **None** | **Yes** |
| `DB_SSLMODE` | SSL mode | require | No |

⚠️  **SECURITY NOTE**: No default values are provided for sensitive credentials. All database connection variables must be explicitly set via environment variables or `.env` file.

## Security Notes

- Never commit the `.env` file to version control
- Use strong, unique passwords
- Rotate database credentials regularly
- Consider using connection pooling for production
- Use SSL/TLS connections (sslmode=require)

## Testing the Configuration

You can test your database configuration by running:

```python
from src.data_management_with_psql import init_database, get_table_info

# Test connection
init_database()
get_table_info()
```

## Troubleshooting

### Connection Issues
- Verify all environment variables are set correctly
- Check database host and port accessibility
- Ensure SSL certificates are valid
- Confirm user permissions on the database

### Environment Variable Issues
- Check if `.env` file exists and is readable
- Verify environment variable names (case-sensitive)
- Ensure no extra spaces in variable definitions

## Production Deployment

For production deployments:

1. **Never use default values** - always set explicit environment variables
2. **Use secrets management** - consider using services like:
   - AWS Secrets Manager
   - Azure Key Vault
   - HashiCorp Vault
   - Kubernetes Secrets

3. **Enable connection pooling** for better performance
4. **Monitor database connections** and set appropriate timeouts
5. **Use read replicas** for read-heavy workloads if available