# Stock Advisor Backend - Quick Start Guide

## 🚀 Your FastAPI Stock Advisor Backend is Ready!

### Project Overview
You now have a fully functional stock analysis and prediction backend with the following features:

✅ **FastAPI REST API** with comprehensive endpoints  
✅ **Machine Learning** price prediction using Random Forest  
✅ **Technical Indicators** (SMA, RSI, MACD, Bollinger Bands)  
✅ **Real-time Stock Data** via yfinance  
✅ **Error Handling** with clear messages  
✅ **CORS Support** for frontend integration  
✅ **API Documentation** with Swagger UI  

### 📁 Project Structure
```
STOKY/
├── app.py              # Main FastAPI application with all endpoints
├── model.py            # StockPredictor class with ML logic
├── utils.py            # Utility functions for validation and formatting
├── test_setup.py       # Test script to verify setup
├── start_api.bat       # Windows batch file to start the server
├── requirements.txt    # Python dependencies
├── README.md          # Detailed documentation
├── .env.example       # Environment configuration template
└── .github/
    └── copilot-instructions.md  # GitHub Copilot instructions
```

### 🛠️ Available API Endpoints

1. **Health Check**
   - `GET /health` - Check if API is running

2. **Stock Information**
   - `GET /stock/info/{symbol}` - Get current stock info (price, volume, metrics)
   - `GET /stock/history/{symbol}?period=1y` - Get historical price data
   - `GET /stock/predict/{symbol}?days_ahead=5` - Predict future prices
   - `GET /stock/model-info/{symbol}` - Get ML model information

### 🚦 How to Start the API

#### Option 1: Use VS Code Task
1. Press `Ctrl+Shift+P`
2. Type "Tasks: Run Task"
3. Select "Run Stock Advisor API"

#### Option 2: Use Command Line
```bash
cd "C:\Users\LL3922\Desktop\VS Code\private projects\STOKY"
C:/Python313/python.exe app.py
```

#### Option 3: Use Batch File
Double-click `start_api.bat` file

### 🌐 Access Your API

Once started, your API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc

### 🧪 Test the API

Try these example requests:

1. **Health Check**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **Get Apple Stock Info**:
   ```bash
   curl http://localhost:8000/stock/info/AAPL
   ```

3. **Get Historical Data**:
   ```bash
   curl "http://localhost:8000/stock/history/AAPL?period=1y"
   ```

4. **Predict Stock Price**:
   ```bash
   curl "http://localhost:8000/stock/predict/AAPL?days_ahead=5"
   ```

### 🔧 Machine Learning Features

The prediction model includes:
- **Technical Indicators**: SMA (5,10,20,50), RSI, MACD, Bollinger Bands
- **Price Features**: Price changes, volume changes, volatility
- **ML Algorithm**: Random Forest Regressor (100 estimators)
- **Training Data**: 2 years of historical data
- **Feature Engineering**: 15+ technical indicators as features

### 📋 Next Steps

1. **Start the API** using one of the methods above
2. **Test the endpoints** using the Swagger UI at `/docs`
3. **Customize the model** by modifying parameters in `model.py`
4. **Add authentication** if needed for production use
5. **Deploy to cloud** (AWS, Azure, GCP) for production

### 🐛 Troubleshooting

- **Import Errors**: Run `C:/Python313/python.exe test_setup.py` to verify setup
- **Package Issues**: Re-run `pip install -r requirements.txt`
- **Port Conflicts**: Change port in `app.py` (line with `uvicorn.run`)
- **Stock Symbol Errors**: Ensure you use valid symbols (e.g., AAPL, GOOGL, MSFT)

### 📚 Documentation

- **Detailed README**: See `README.md` for comprehensive documentation
- **API Reference**: Visit `/docs` when server is running
- **Code Comments**: All functions include detailed docstrings

---

**🎉 Congratulations! Your Stock Advisor Backend is ready for development and testing!**
