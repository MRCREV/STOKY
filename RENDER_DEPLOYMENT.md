# Render Deployment Guide for STOKY

## Prerequisites
- GitHub repository with your code (✅ Already done)
- Render account (free tier available)

## Step-by-Step Deployment Process

### 1. Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up using your GitHub account
3. This will automatically connect your GitHub repositories

### 2. Create New Web Service
1. Click "New +" in your Render dashboard
2. Select "Web Service"
3. Choose "Build and deploy from a Git repository"
4. Connect your GitHub account if not already connected
5. Select your STOKY repository

### 3. Configure Service Settings
Fill in the following settings:

**Basic Settings:**
- **Name**: `stoky-api` (or your preferred name)
- **Region**: Choose closest to your users (US East is default)
- **Branch**: `main` (or your default branch)
- **Root Directory**: Leave empty (since files are in root)
- **Runtime**: `Python 3`

**Build & Deploy:**
- **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
- **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`

**Advanced Settings:**
- **Auto-Deploy**: Enable (recommended)
- **Health Check Path**: `/health`

### 4. Environment Variables (Optional)
If your app needs environment variables:
1. Scroll to "Environment Variables" section
2. Add any required variables
3. Common ones for stock APIs:
   - `PYTHONPATH=/opt/render/project/src`
   - `LOG_LEVEL=info`

### 5. Deploy
1. Click "Create Web Service"
2. Render will automatically:
   - Clone your repository
   - Install dependencies from requirements.txt
   - Build and start your application
   - Provide you with a public URL

### 6. Monitor Deployment
- Watch the deployment logs in real-time
- First deployment may take 5-10 minutes
- Your API will be available at: `https://your-service-name.onrender.com`

## Post-Deployment

### Test Your API
Once deployed, test these endpoints:
- Health check: `https://your-service-name.onrender.com/health`
- API docs: `https://your-service-name.onrender.com/docs`
- Stock prediction: `https://your-service-name.onrender.com/predict/AAPL`

### Update Your Frontend
Update your Flutter and Next.js apps to use the new Render URL instead of localhost:8000

## Configuration Files Summary

Your project already includes all necessary files:
- ✅ `render.yaml` - Render service configuration
- ✅ `requirements.txt` - Python dependencies with pinned versions
- ✅ `runtime.txt` - Python version specification (3.11.0)
- ✅ `app.py` - FastAPI app with health endpoint and proper CORS
- ✅ Health endpoint at `/health` for Render health checks

## Free Tier Limitations
- Service spins down after 15 minutes of inactivity
- Takes ~30 seconds to spin back up (cold start)
- 750 hours/month free (enough for development/testing)

## Troubleshooting

### Common Issues:
1. **Build fails**: Check requirements.txt for version conflicts
2. **Service won't start**: Verify start command and port binding
3. **Health check fails**: Ensure `/health` endpoint returns 200 status

### View Logs:
- Go to your service dashboard on Render
- Click "Logs" tab to see real-time application logs
- Use logs to debug any deployment issues

## Next Steps After Deployment
1. Update mobile app API endpoints
2. Update Next.js frontend API base URL
3. Test all functionality with the live API
4. Consider upgrading to paid plan for production use

Your STOKY backend is now ready for cloud deployment! 🚀
