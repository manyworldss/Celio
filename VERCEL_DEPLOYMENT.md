# Vercel Deployment Guide for Celio

This guide will help you deploy the Celio Django application to Vercel with blob storage support.

## Prerequisites

1. A Vercel account (https://vercel.com)
2. Vercel CLI installed (`npm i -g vercel`)
3. A PostgreSQL database (Vercel Postgres, Neon, or other)
4. Vercel Blob storage setup

## Step 1: Install Dependencies

Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Step 2: Environment Variables

In your Vercel dashboard, go to Settings > Environment Variables and add:

### Required Variables:
- `DJANGO_SECRET_KEY`: Your Django secret key
- `DJANGO_DEBUG`: `False`
- `DJANGO_ALLOWED_HOSTS`: `.vercel.app,localhost,127.0.0.1`
- `DATABASE_URL`: Your PostgreSQL connection string
- `VERCEL_BLOB_TOKEN`: Your Vercel blob storage token
- `CSRF_TRUSTED_ORIGINS`: `https://*.vercel.app`
- `RAILWAY_ENVIRONMENT`: `production`

### Example values:
```
DJANGO_SECRET_KEY=your-very-long-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=.vercel.app,localhost,127.0.0.1
DATABASE_URL=postgres://username:password@host:port/database
VERCEL_BLOB_TOKEN=vercel_blob_rw_xxxxxxxxxx
CSRF_TRUSTED_ORIGINS=https://*.vercel.app
RAILWAY_ENVIRONMENT=production
```

## Step 3: Database Setup

### Option A: Vercel Postgres
1. Go to your Vercel dashboard
2. Navigate to Storage tab
3. Create a new Postgres database
4. Copy the connection string to `DATABASE_URL`

### Option B: External PostgreSQL (Neon, etc.)
1. Create a PostgreSQL database
2. Get the connection string
3. Add it as `DATABASE_URL` environment variable

## Step 4: Vercel Blob Storage

1. In Vercel dashboard, go to Storage
2. Create a new Blob store
3. Get the token and add it as `VERCEL_BLOB_TOKEN`

## Step 5: Deploy

### Method 1: Vercel CLI
```bash
# Login to Vercel
vercel login

# Deploy
vercel --prod
```

### Method 2: Git Integration
1. Push your code to GitHub
2. Connect your repository in Vercel dashboard
3. Deploy automatically on push

## Step 6: Run Migrations

After deployment, run migrations:
```bash
vercel env pull .env.local
python manage.py migrate
```

Or use Vercel's serverless functions to run migrations.

## Step 7: Upload Media to Blob Storage

Use the management command to upload videos:
```bash
python manage.py upload_video
```

## Troubleshooting

### Common Issues:

1. **Static files not loading**
   - Ensure `STATIC_ROOT` is set to `staticfiles_build/static`
   - Run `python manage.py collectstatic`

2. **Database connection errors**
   - Verify `DATABASE_URL` is correct
   - Ensure database allows connections from Vercel

3. **CSRF errors**
   - Check `CSRF_TRUSTED_ORIGINS` includes your domain
   - Verify `DJANGO_ALLOWED_HOSTS` is set correctly

4. **Blob storage issues**
   - Verify `VERCEL_BLOB_TOKEN` is correct
   - Check blob store permissions

## File Structure

Key files for Vercel deployment:
- `vercel.json` - Vercel configuration
- `build_files.sh` - Build script
- `.vercelignore` - Files to ignore during deployment
- `requirements.txt` - Python dependencies
- `.env.vercel` - Environment variables template

## Performance Tips

1. Use Vercel's Edge Network for static files
2. Enable compression in WhiteNoise
3. Use database connection pooling
4. Optimize images before uploading to blob storage

## Security Notes

- Never commit environment variables to Git
- Use strong secret keys
- Enable HTTPS only in production
- Regularly rotate API tokens

For more help, check the Vercel documentation: https://vercel.com/docs