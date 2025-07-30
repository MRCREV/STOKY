# 📈 STOKY - AI-Powered Stock Advisor

> **Advanced Stock Analysis & Prediction Platform with Multi-Currency Support**

STOKY is a full-stack application that combines real-time stock data, advanced machine learning predictions, and beautiful data visualization to help you make informed investment decisions. Built with FastAPI backend and Next.js frontend.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)
![Next.js](https://img.shields.io/badge/Next.js-15-black.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)
![ML](https://img.shields.io/badge/ML-Scikit--Learn-orange.svg)

## 🌟 Features

### 🎯 **Core Functionality**
- **Real-time Stock Data** - Live prices, volume, market cap, P/E ratios
- **AI Price Predictions** - Advanced ensemble ML models with confidence scoring
- **Multi-Currency Support** - Automatic currency detection for global stocks
- **Interactive Charts** - Beautiful price history visualization with technical indicators
- **Exchange Detection** - Automatic identification of stock exchanges worldwide

### 🤖 **Machine Learning Models**
- **Basic Model**: Random Forest Regressor with technical indicators
- **Advanced Model**: Ensemble of 5 algorithms (Random Forest, Gradient Boosting, Extra Trees)
- **Technical Indicators**: 50+ indicators including SMA, EMA, RSI, MACD, Bollinger Bands
- **Confidence Scoring**: Model confidence assessment for predictions
- **Feature Importance**: Understanding which factors drive predictions

### 🌍 **Global Stock Support**
- **US Markets**: NASDAQ, NYSE (USD $)
- **Brazilian Market**: B3 São Paulo (BRL R$)
- **European Markets**: Euronext, London, Swiss (EUR €, GBP £, CHF)
- **Asian Markets**: Tokyo, Hong Kong, Seoul (JPY ¥, HKD HK$, KRW ₩)
- **And more**: 12+ currencies, 20+ exchanges

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/STOKY.git
cd STOKY
```

### 2. Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI server
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📁 Project Structure

```
STOKY/
├── 🐍 Backend (Python/FastAPI)
│   ├── app.py                 # Main FastAPI application
│   ├── model.py              # Basic ML model
│   ├── advanced_model.py     # Advanced ensemble ML model
│   ├── currency_utils.py     # Multi-currency support
│   ├── utils.py              # Utility functions
│   └── requirements.txt      # Python dependencies
│
├── ⚛️ Frontend (Next.js/TypeScript)
│   ├── src/
│   │   ├── app/              # Next.js app router
│   │   ├── components/       # React components
│   │   │   ├── StockCard.tsx     # Stock information display
│   │   │   ├── StockChart.tsx    # Price chart visualization
│   │   │   ├── PredictionCard.tsx # AI prediction display
│   │   │   └── StockSearch.tsx   # Stock search component
│   │   └── lib/
│   │       ├── api.ts            # API service layer
│   │       ├── currency.ts       # Currency utilities
│   │       └── utils.ts          # Utility functions
│   └── package.json          # Node.js dependencies
│
└── 📚 Documentation
    ├── README.md                 # This file
    ├── CURRENCY_IMPLEMENTATION.md # Currency system details
    └── QUICK_START.md           # Quick setup guide
```

## 🛠️ API Endpoints

### Stock Information
- `GET /stock/info/{symbol}` - Basic stock information
- `GET /stock/history/{symbol}` - Historical price data

### AI Predictions
- `GET /stock/predict/{symbol}` - Basic price prediction
- `GET /stock/predict-advanced/{symbol}` - Advanced ensemble prediction

### Model Information
- `GET /stock/model-info/{symbol}` - Basic model details
- `GET /stock/advanced-model-info/{symbol}` - Advanced model analysis

### System
- `GET /health` - API health check

## 💰 Multi-Currency Examples

| Symbol | Market | Currency | Display |
|--------|--------|----------|---------|
| AAPL | NASDAQ | USD | $150.25 |
| PETR4.SA | B3 São Paulo | BRL | R$32,44 |
| ASML.AS | Euronext Amsterdam | EUR | €650,80 |
| VOD.L | London Stock Exchange | GBP | £75.50 |
| 7203.T | Tokyo Stock Exchange | JPY | ¥2,500 |
| SHOP.TO | Toronto Stock Exchange | CAD | C$85.30 |

## 🤖 Machine Learning Details

### Technical Indicators Used
- **Trend**: SMA, EMA, MACD, ADX
- **Momentum**: RSI, Stochastic Oscillator
- **Volatility**: Bollinger Bands, ATR
- **Volume**: Volume SMA, Price-Volume Trend
- **Custom**: Price position, volatility ratios

### Model Performance
- **Training Period**: 3 years of historical data
- **Prediction Horizon**: 1-30 days ahead
- **Validation**: Time series cross-validation
- **Confidence Scoring**: Ensemble agreement analysis

## 🚀 Deployment

### Local Production
```bash
# Start both services
./start_both.bat  # Windows
# or
python -m uvicorn app:app --host 0.0.0.0 --port 8000 &
cd frontend && npm run build && npm start
```

### Docker (Coming Soon)
```bash
docker-compose up
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This application is for educational and informational purposes only. The predictions provided by the AI models should not be considered as financial advice. Always do your own research and consult with qualified financial advisors before making investment decisions.

## 🙏 Acknowledgments

- [yfinance](https://github.com/ranaroussi/yfinance) for stock data
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [Next.js](https://nextjs.org/) for the frontend framework
- [scikit-learn](https://scikit-learn.org/) for machine learning models
- [Recharts](https://recharts.org/) for data visualization

---

**Built with ❤️ for the trading community**

## Development

To run in development mode with auto-reload:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Production Considerations

For production deployment:
1. Update CORS origins to specific domains
2. Add authentication if required
3. Implement rate limiting
4. Add monitoring and logging
5. Use environment variables for configuration
6. Consider caching for frequently requested data

## License

This project is for educational and demonstration purposes.
