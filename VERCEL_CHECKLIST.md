# Vercel Deployment Checklist ✅

## Pre-Deployment Setup

### 1. Database Setup
- [ ] Create PostgreSQL database (Neon, Supabase, or Railway)
- [ ] Copy the DATABASE_URL connection string
- [ ] Test database connection locally

### 2. Environment Variables
- [ ] Generate a secure DJANGO_SECRET_KEY (50+ characters)
- [ ] Set DJANGO_DEBUG=False for production
- [ ] Prepare DATABASE_URL

### 3. Code Preparation
- [ ] Commit all changes to Git
- [ ] Push to GitHub repository
- [ ] Verify all files are included (check .gitignore)

## Vercel Deployment Steps

### 1. Connect Repository
- [ ] Go to [vercel.com/dashboard](https://vercel.com/dashboard)
- [ ] Click "New Project"
- [ ] Import your GitHub repository
- [ ] Select the repository

### 2. Configure Environment Variables
In Vercel dashboard, add these environment variables:
- [ ] `DJANGO_SECRET_KEY` = your-secure-secret-key
- [ ] `DJANGO_DEBUG` = False
- [ ] `DATABASE_URL` = your-postgresql-connection-string

### 3. Deploy
- [ ] Click "Deploy"
- [ ] Wait for build to complete
- [ ] Check build logs for any errors

## Post-Deployment Setup

### 1. Database Migration
Run migrations using one of these methods:

**Option A: Local to Production**
```bash
export DATABASE_URL="your-production-database-url"
python manage.py migrate
python manage.py createsuperuser  # Optional
```

**Option B: Using Management Command**
```bash
python manage.py setup_production --create-superuser
```

### 2. Test Your Deployment
- [ ] Visit your Vercel URL
- [ ] Test user registration
- [ ] Test login/logout
- [ ] Create a test trip
- [ ] Upload a test photo
- [ ] Verify all features work

### 3. Custom Domain (Optional)
- [ ] Add custom domain in Vercel dashboard
- [ ] Update DNS settings
- [ ] Verify SSL certificate

## Troubleshooting

### Common Issues:
- **Build fails**: Check Python version in vercel.json
- **Database errors**: Verify DATABASE_URL format
- **Static files missing**: Check build_files.sh execution
- **CSRF errors**: Verify domain in ALLOWED_HOSTS

### Useful Commands:
```bash
# Test locally with production settings
export DJANGO_DEBUG=False
python manage.py check --deploy

# Test static files collection
python manage.py collectstatic --dry-run

# Test database connection
python manage.py dbshell
```

## Success Criteria ✅

Your deployment is successful when:
- [ ] Site loads without errors
- [ ] User registration works
- [ ] Database operations work
- [ ] Static files load correctly
- [ ] Media uploads work (temporarily)
- [ ] All main features are functional

## Next Steps

After successful deployment:
1. Set up monitoring and error tracking
2. Configure media storage (AWS S3/Cloudinary)
3. Set up automated backups
4. Configure custom domain
5. Set up staging environment

---

**Need Help?**
- Check [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) for detailed instructions
- Review Vercel documentation: [vercel.com/docs](https://vercel.com/docs)
- Check application logs in Vercel dashboard