# Fly.io Deployment Guide for Celio

This guide will help you deploy the Celio Django application to Fly.io.

## Prerequisites

1. A Fly.io account (https://fly.io)
2. Fly CLI installed (`flyctl`)
3. A PostgreSQL database (Fly Postgres or external)

## Step 1: Install Fly CLI

### Windows (PowerShell)
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

### macOS/Linux
```bash
curl -L https://fly.io/install.sh | sh
```

## Step 2: Login to Fly.io

```bash
flyctl auth login
```

## Step 3: Create a Fly.io App

```bash
flyctl apps create celio
```

## Step 4: Set Environment Variables

Set the required environment variables:

```bash
# Django Secret Key (generate a new one)
flyctl secrets set DJANGO_SECRET_KEY="your-super-secret-key"

# Database URL (if using external database)
flyctl secrets set DATABASE_URL="postgres://username:password@host:port/database"

# Django Settings
flyctl secrets set DJANGO_DEBUG="False"
flyctl secrets set DJANGO_ALLOWED_HOSTS=".fly.dev,.internal"
```

## Step 5: Create a PostgreSQL Database (Optional)

If you need a database, create one with Fly Postgres:

```bash
# Create a Postgres cluster
flyctl postgres create --name celio-db

# Attach it to your app
flyctl postgres attach --app celio celio-db
```

This will automatically set the `DATABASE_URL` secret.

## Step 6: Deploy

```bash
flyctl deploy
```

Or use the helper script:

```bash
python deploy.py
```

## Step 7: Open Your App

```bash
flyctl open
```

## Configuration Files

The following files are configured for Fly.io deployment:

- `fly.toml` - Fly.io app configuration
- `Dockerfile` - Container configuration
- `.flyignore` - Files to exclude from deployment
- `.dockerignore` - Files to exclude from Docker build

## Environment Variables

### Required:
- `DJANGO_SECRET_KEY` - Django secret key
- `DATABASE_URL` - PostgreSQL connection string (auto-set if using Fly Postgres)

### Optional:
- `DJANGO_DEBUG` - Set to "False" for production (default: False)
- `DJANGO_ALLOWED_HOSTS` - Comma-separated list of allowed hosts

## Useful Commands

```bash
# Check app status
flyctl status

# View logs
flyctl logs

# SSH into the app
flyctl ssh console

# Scale the app
flyctl scale count 2

# Update secrets
flyctl secrets set KEY=value

# List secrets
flyctl secrets list
```

## Troubleshooting

### Common Issues:

1. **Static files not loading**
   - Ensure `STATIC_ROOT` is set to `staticfiles`
   - Check that `collectstatic` runs during build

2. **Database connection errors**
   - Verify `DATABASE_URL` is correct
   - Ensure database allows connections from Fly.io

3. **CSRF errors**
   - Check `CSRF_TRUSTED_ORIGINS` includes your Fly.io domain
   - Verify `ALLOWED_HOSTS` is set correctly

4. **App won't start**
   - Check logs with `flyctl logs`
   - Verify all required environment variables are set

### Health Checks

The app includes health checks configured in `fly.toml`. If your app fails health checks:

1. Ensure your Django app responds to GET requests on `/`
2. Check that the app starts within the timeout period
3. Verify the internal port (8000) is correct

## Security Notes

- Never commit secrets to Git
- Use strong secret keys
- Enable HTTPS only in production
- Regularly rotate API tokens

## Performance Tips

1. Use Fly's global network for better performance
2. Enable compression in WhiteNoise
3. Use database connection pooling
4. Consider using Fly's Redis for caching

For more help, check the Fly.io documentation: https://fly.io/docs/django/