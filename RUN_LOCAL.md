# Local Development Server for STOKY

## Run Locally (Immediate Solution)

### 1. Install Dependencies
```cmd
cd "C:\Users\LL3922\Desktop\VS Code\private projects\STOKY"
pip install fastapi uvicorn yfinance scikit-learn pandas numpy python-multipart requests
```

### 2. Start Server
```cmd
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Test API
- Local URL: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### 4. Make It Public with ngrok (Optional)
1. Download ngrok: https://ngrok.com/download
2. Run: `ngrok http 8000`
3. Use the public URL for your mobile app

## Quick Test Commands:
```cmd
# Test health endpoint
curl http://localhost:8000/health

# Test stock data
curl "http://localhost:8000/stock/AAPL"

# Test prediction
curl "http://localhost:8000/predict/AAPL?days=7"
```
