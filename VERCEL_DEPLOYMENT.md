# Vercel Deployment Guide

This guide will help you deploy your Django Trip Planner application to Vercel.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **PostgreSQL Database**: You'll need a PostgreSQL database (recommended: Neon, Supabase, or Railway)

## Step 1: Prepare Your Database

### Option A: Neon (Recommended)
1. Go to [neon.tech](https://neon.tech) and create a free account
2. Create a new project
3. Copy the connection string (it looks like: `postgresql://username:password@hostname/database`)

### Option B: Supabase
1. Go to [supabase.com](https://supabase.com) and create a free account
2. Create a new project
3. Go to Settings > Database and copy the connection string

### Option C: Railway
1. Go to [railway.app](https://railway.app) and create a free account
2. Create a new PostgreSQL database
3. Copy the connection string from the database settings

## Step 2: Deploy to Vercel

1. **Connect GitHub Repository**:
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your GitHub repository

2. **Configure Environment Variables**:
   In the Vercel dashboard, add these environment variables:
   ```
   DJANGO_SECRET_KEY=your-super-secret-key-here
   DJANGO_DEBUG=False
   DATABASE_URL=your-postgresql-connection-string
   ```

3. **Deploy**:
   - Click "Deploy"
   - Vercel will automatically build and deploy your application

## Step 3: Run Database Migrations

After your first deployment, you need to run migrations:

1. Go to your Vercel dashboard
2. Navigate to your project
3. Go to the "Functions" tab
4. You'll need to run migrations manually using a one-time script or through your database provider's interface

### Alternative: Local Migration to Production Database
```bash
# Set your production database URL locally
export DATABASE_URL="your-postgresql-connection-string"

# Run migrations
python manage.py migrate

# Create a superuser (optional)
python manage.py createsuperuser
```

## Step 4: Configure Custom Domain (Optional)

1. In your Vercel project dashboard, go to "Settings" > "Domains"
2. Add your custom domain
3. Update your environment variables to include your domain in `ALLOWED_HOSTS`

## Important Notes

### Static Files
- Static files are handled automatically by Vercel
- The `build_files.sh` script collects static files during deployment

### Media Files
- User-uploaded files (profile photos, trip photos) will be stored temporarily
- For production, consider using a cloud storage service like AWS S3 or Cloudinary

### Database Limitations
- SQLite doesn't work on Vercel (serverless environment)
- You must use PostgreSQL or another external database

### Environment Variables
Make sure to set these in your Vercel dashboard:
- `DJANGO_SECRET_KEY`: A secure secret key
- `DJANGO_DEBUG`: Set to `False` for production
- `DATABASE_URL`: Your PostgreSQL connection string

## Troubleshooting

### Common Issues:

1. **Build Fails**: Check the build logs in Vercel dashboard
2. **Database Connection**: Ensure your DATABASE_URL is correct
3. **Static Files**: Make sure `collectstatic` runs successfully
4. **CSRF Errors**: Verify your domain is in `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`

### Getting Help:
- Check Vercel's documentation: [vercel.com/docs](https://vercel.com/docs)
- Review Django deployment best practices
- Check the application logs in Vercel dashboard

## File Structure for Vercel

Your project now includes these Vercel-specific files:
- `vercel.json`: Vercel configuration
- `build_files.sh`: Build script for static files
- `app.py`: WSGI application entry point
- Updated `settings.py`: Vercel-compatible settings

## Next Steps

1. Test your deployed application thoroughly
2. Set up monitoring and error tracking
3. Configure a proper media storage solution for production
4. Set up automated backups for your database
5. Consider setting up a staging environment

Your Django Trip Planner should now be successfully deployed on Vercel! 🎉