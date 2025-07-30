# Render Deployment Guide for STOKY

## Deploy to Render (Recommended)

Render is more reliable for Python apps than Railway. Follow these steps:

### 1. Go to Render.com
- Sign up/login with your GitHub account
- Click "New +" → "Web Service"

### 2. Connect Repository
- Select "Connect a repository"
- Choose your STOKY repository (MRCREV/STOKY)

### 3. Configure Deployment
- **Name**: stoky-backend
- **Region**: Choose closest to you
- **Branch**: master
- **Root Directory**: . (leave empty for root)
- **Runtime**: Python 3
- **Build Command**: pip install -r requirements.txt
- **Start Command**: python -m uvicorn app:app --host 0.0.0.0 --port $PORT

### 4. Environment Variables
Add these in Render dashboard:
- PYTHON_VERSION: 3.11.0

### 5. Deploy
Click "Create Web Service" - deployment usually takes 2-3 minutes

### 6. Test Your API
Once deployed, you'll get a URL like: https://stoky-backend.onrender.com
Test: https://stoky-backend.onrender.com/docs

## Why Render is Better:
- ✅ Better Python support
- ✅ Automatic HTTPS
- ✅ More reliable builds
- ✅ Free tier with 750 hours/month
- ✅ Fewer dependency conflicts
