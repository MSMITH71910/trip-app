# 🚀 Heroku Deployment Guide for Trip Planner

This guide will help you deploy your Trip Planner application to Heroku.

## Prerequisites

1. **Heroku Account**: Sign up at [heroku.com](https://heroku.com)
2. **Heroku CLI**: Install from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git**: Make sure your project is in a Git repository

## Step-by-Step Deployment

### 1. Login to Heroku
```bash
heroku login
```

### 2. Create a New Heroku App
```bash
heroku create your-trip-planner-app-name
```
*Replace `your-trip-planner-app-name` with your desired app name (must be unique)*

### 3. Add PostgreSQL Database
```bash
heroku addons:create heroku-postgresql:mini
```

### 4. Set Environment Variables
```bash
# Set a secure secret key
heroku config:set DJANGO_SECRET_KEY="your-super-secret-key-here"

# Set debug to False for production
heroku config:set DJANGO_DEBUG=False

# Set your app name (for CSRF and ALLOWED_HOSTS)
heroku config:set HEROKU_APP_NAME=your-trip-planner-app-name
```

### 5. Deploy to Heroku
```bash
# Add Heroku remote (if not already added)
heroku git:remote -a your-trip-planner-app-name

# Deploy your code
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main
```

### 6. Run Database Migrations
```bash
heroku run python manage.py migrate
```

### 7. Create a Superuser (Optional)
```bash
heroku run python manage.py createsuperuser
```

### 8. Open Your App
```bash
heroku open
```

## Environment Variables Explained

| Variable | Description | Example |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Django secret key for security | `your-super-secret-key-here` |
| `DJANGO_DEBUG` | Debug mode (should be False in production) | `False` |
| `HEROKU_APP_NAME` | Your Heroku app name | `my-trip-planner` |
| `DATABASE_URL` | PostgreSQL database URL (auto-set by Heroku) | `postgres://...` |

## Post-Deployment Checklist

- [ ] App loads without errors
- [ ] User registration works
- [ ] User login works
- [ ] Trip creation works
- [ ] Photo uploads work
- [ ] Portfolio pages load
- [ ] Settings page works
- [ ] Dark/Light mode switching works

## Troubleshooting

### Common Issues

1. **Static Files Not Loading**
   ```bash
   heroku run python manage.py collectstatic --noinput
   ```

2. **Database Issues**
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py makemigrations
   heroku run python manage.py migrate
   ```

3. **View Logs**
   ```bash
   heroku logs --tail
   ```

4. **Reset Database (if needed)**
   ```bash
   heroku pg:reset DATABASE_URL
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

### Environment Variables Check
```bash
heroku config
```

## Custom Domain (Optional)

If you want to use a custom domain:

1. **Add your domain to Heroku**
   ```bash
   heroku domains:add www.yourdomain.com
   heroku domains:add yourdomain.com
   ```

2. **Update DNS settings** with your domain provider to point to Heroku

3. **Add SSL certificate**
   ```bash
   heroku certs:auto:enable
   ```

## Updating Your App

To deploy updates:

```bash
git add .
git commit -m "Your update message"
git push heroku main
```

If you have database changes:
```bash
heroku run python manage.py migrate
```

## Features Available After Deployment

✅ **User Portfolio System**
- Personal portfolio pages for each user
- Featured trips showcase
- Social media links integration
- Bio and location information

✅ **Comprehensive Settings**
- Privacy controls (Public, Registered Users, Private)
- Theme preferences (Light, Dark, Auto)
- Notification settings
- Display preferences

✅ **Dark Mode Support**
- Automatic theme detection
- User preference saving
- Consistent dark theme across all pages

✅ **Enhanced Security**
- HTTPS enforcement in production
- Secure cookie settings
- CSRF protection
- XSS protection

## Support

If you encounter issues:

1. Check the [Heroku documentation](https://devcenter.heroku.com/)
2. View your app logs: `heroku logs --tail`
3. Check your environment variables: `heroku config`
4. Ensure all migrations are applied: `heroku run python manage.py showmigrations`

## Cost Information

- **Heroku Dyno**: Free tier available (sleeps after 30 minutes of inactivity)
- **PostgreSQL**: Mini plan is free (10,000 rows limit)
- **Custom Domain**: Free
- **SSL Certificate**: Free with Heroku

For production use, consider upgrading to paid plans for better performance and no sleep mode.

---

**Happy Deploying! 🚀**