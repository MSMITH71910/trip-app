# 🔍 Vercel 500 Error Debug Guide

## 🚨 **Current Issue:**
- Build succeeded ✅
- Runtime error: `500: INTERNAL_SERVER_ERROR`
- Function invocation failed

## 🔧 **Debug Steps:**

### 1. **Check Vercel Function Logs**
1. Go to your Vercel dashboard
2. Click on your project
3. Go to "Functions" tab
4. Click on the failed function to see detailed logs
5. Look for specific error messages

### 2. **Verify Environment Variables**
Make sure these are set in Vercel dashboard:

**Required Variables:**
```
DJANGO_SECRET_KEY=+2i!*%t#3g%u1gb5hm2etdv4&ayt*6o8$7#-zyef&jd&=^rxk(
DJANGO_DEBUG=False
DATABASE_URL=postgresql://username:password@hostname/database
```

**To check/add:**
1. Vercel Dashboard → Your Project → Settings → Environment Variables
2. Make sure all 3 variables are present
3. Make sure DATABASE_URL is a valid PostgreSQL connection string

### 3. **Common Issues & Solutions:**

#### **Issue A: Missing DATABASE_URL**
**Error:** Database connection failed
**Solution:** Add PostgreSQL database URL to environment variables

#### **Issue B: Invalid SECRET_KEY**
**Error:** Django configuration error
**Solution:** Use the provided secret key exactly as shown

#### **Issue C: Database Not Set Up**
**Error:** Database tables don't exist
**Solution:** Run migrations (see below)

#### **Issue D: Static Files Missing**
**Error:** Static files not found
**Solution:** Already handled by WhiteNoise

## 🗄️ **Database Setup (Most Likely Issue):**

### **Option 1: Neon Database (Recommended)**
1. Go to [neon.tech](https://neon.tech)
2. Create free account
3. Create new project
4. Copy connection string like:
   ```
   postgresql://username:password@hostname/database
   ```
5. Add to Vercel environment variables as `DATABASE_URL`

### **Option 2: Supabase Database**
1. Go to [supabase.com](https://supabase.com)
2. Create project
3. Settings → Database → Connection string
4. Copy and add to Vercel

### **Option 3: Railway Database**
1. Go to [railway.app](https://railway.app)
2. Create PostgreSQL database
3. Copy connection string
4. Add to Vercel

## 🔄 **After Adding Database:**

### **Run Migrations:**
```bash
# Set your production database URL locally
export DATABASE_URL="your-postgresql-connection-string"

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### **Redeploy:**
1. After adding DATABASE_URL to Vercel
2. Go to Vercel dashboard
3. Click "Redeploy" to restart with new environment variables

## 🔍 **Debug Checklist:**

- [ ] Environment variables are set in Vercel
- [ ] DATABASE_URL is valid PostgreSQL connection
- [ ] Database exists and is accessible
- [ ] Migrations have been run
- [ ] Function logs show specific error details

## 📞 **Get Specific Error Details:**

1. **Check Vercel Function Logs:**
   - Dashboard → Project → Functions → Click on failed function
   - Look for Python traceback or Django error

2. **Enable Debug Mode Temporarily:**
   - Set `DJANGO_DEBUG=True` in Vercel (temporarily)
   - Redeploy to see detailed error page
   - **Remember to set back to False after debugging**

## 🎯 **Most Likely Solution:**

The error is probably because:
1. **DATABASE_URL is missing** - Add PostgreSQL database
2. **Database tables don't exist** - Run migrations
3. **Invalid environment variables** - Double-check all values

Follow the database setup steps above and the error should resolve! 🚀