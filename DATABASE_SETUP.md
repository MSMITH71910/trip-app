# 🗄️ Database Setup for Vercel

## 🎯 **This Will Fix Your 500 Error!**

The 500 error is because Django can't connect to a database. Here's how to fix it:

## 📋 **Step 1: Get Free PostgreSQL Database**

### **Option A: Neon (Recommended)**
1. Go to [neon.tech](https://neon.tech)
2. Click "Sign Up" (free)
3. Create account with GitHub or email
4. Click "Create Project"
5. Choose a project name (e.g., "trip-app-db")
6. Select region (US East is fine)
7. Click "Create Project"

### **Copy Connection String:**
After creating the project, you'll see a connection string like:
```
postgresql://username:password@ep-example-123456.us-east-1.aws.neon.tech/neondb?sslmode=require
```

**Copy this entire string!**

## 📋 **Step 2: Add to Vercel**

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click on your "trip-app" project
3. Click "Settings" tab
4. Click "Environment Variables" in sidebar
5. Click "Add New"
6. Enter:
   - **Name:** `DATABASE_URL`
   - **Value:** `postgresql://your-connection-string-from-neon`
   - **Environment:** Production
7. Click "Save"

**Vercel will automatically redeploy when you add this!**

## 📋 **Step 3: Run Migrations**

```bash
cd ~/trip-app
source venv/bin/activate

# Use your REAL Neon connection string (replace the example below)
export DATABASE_URL="postgresql://username:password@ep-example-123456.us-east-1.aws.neon.tech/neondb?sslmode=require"

# Run migrations
python manage.py migrate

# Create admin user (optional)
python manage.py createsuperuser
```

## 📋 **Step 4: Test Your App**

After adding DATABASE_URL to Vercel (wait 2-3 minutes for redeploy):

1. **Check health endpoint:**
   ```
   https://your-app.vercel.app/health/
   ```
   Should show: `"database": "OK"`

2. **Visit your main app:**
   ```
   https://your-app.vercel.app/
   ```
   Should work perfectly! 🎉

## 🔧 **Alternative Database Options:**

### **Option B: Supabase**
1. Go to [supabase.com](https://supabase.com)
2. Create project
3. Settings → Database → Connection string
4. Copy and use as DATABASE_URL

### **Option C: Railway**
1. Go to [railway.app](https://railway.app)
2. Create PostgreSQL database
3. Copy connection string
4. Use as DATABASE_URL

## ✅ **Environment Variables Checklist:**

Make sure these are ALL set in Vercel:
```
DJANGO_SECRET_KEY=+2i!*%t#3g%u1gb5hm2etdv4&ayt*6o8$7#-zyef&jd&=^rxk(
DJANGO_DEBUG=False
DATABASE_URL=postgresql://your-neon-connection-string
```

## 🎯 **Expected Result:**

After adding DATABASE_URL:
- ✅ Vercel automatically redeploys
- ✅ Health check shows "database": "OK"
- ✅ Your Django Trip Planner works perfectly!
- ✅ You can register users, create trips, upload photos

## 📞 **Still Having Issues?**

1. Check `/health/` endpoint for specific errors
2. Verify all 3 environment variables are set in Vercel
3. Make sure DATABASE_URL is the complete connection string from Neon
4. Check Vercel function logs for detailed error messages

**The database setup will fix your 500 error! 🚀**