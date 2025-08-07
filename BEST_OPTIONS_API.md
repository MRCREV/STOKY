# Best Options for Stock Market - API Documentation

This document describes the new "Best Options for Stock Market" functionality implemented in the STOKY API. These endpoints help users identify, compare, and evaluate the best investment opportunities.

## 📋 Overview

The Best Options functionality includes four main features:

1. **Stock Screening** - Filter stocks based on specific criteria
2. **Stock Comparison** - Compare multiple stocks side by side
3. **Top Performers** - Find top performing stocks by category
4. **Investment Recommendations** - Get AI-powered investment advice

## 🔍 Stock Screening

**Endpoint:** `POST /stock/screen`

Screen stocks based on various financial criteria to find the best investment options.

### Request Body
```json
{
  "min_market_cap": 100000000000,     // Minimum market cap ($100B)
  "max_market_cap": 500000000000,     // Maximum market cap ($500B)
  "min_pe_ratio": 5.0,                // Minimum P/E ratio
  "max_pe_ratio": 25.0,               // Maximum P/E ratio
  "min_price": 50.0,                  // Minimum stock price
  "max_price": 200.0,                 // Maximum stock price
  "min_volume": 10000000,             // Minimum trading volume
  "symbols": ["AAPL", "GOOGL", "MSFT"] // Optional: specific symbols to screen
}
```

### Response
```json
[
  {
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "current_price": 150.25,
    "previous_close": 148.50,
    "change": 1.75,
    "change_percent": 1.18,
    "volume": 45000000,
    "market_cap": 2500000000000,
    "pe_ratio": 22.5,
    "dividend_yield": 0.52,
    "currency": "USD",
    "exchange": "NASDAQ"
  }
]
```

### Example Usage
```bash
curl -X POST "http://localhost:8000/stock/screen" \
     -H "Content-Type: application/json" \
     -d '{
       "min_market_cap": 100000000000,
       "max_pe_ratio": 30,
       "symbols": ["AAPL", "GOOGL", "MSFT", "AMZN"]
     }'
```

## ⚖️ Stock Comparison

**Endpoint:** `POST /stock/compare`

Compare multiple stocks side by side to identify the best performers.

### Request Body
```json
["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
```

### Response
```json
{
  "stocks": [
    {
      "symbol": "AAPL",
      "name": "Apple Inc.",
      "current_price": 150.25,
      "change_percent": 1.18,
      // ... other stock info
    }
  ],
  "comparison_date": "2025-08-07T16:30:00.000Z",
  "best_performer": {
    "symbol": "TSLA",
    "name": "Tesla, Inc.",
    "change_percent": 3.45,
    "current_price": 245.30
  },
  "worst_performer": {
    "symbol": "GOOGL",
    "name": "Alphabet Inc.",
    "change_percent": -0.85,
    "current_price": 2750.50
  }
}
```

### Example Usage
```bash
curl -X POST "http://localhost:8000/stock/compare" \
     -H "Content-Type: application/json" \
     -d '["AAPL", "GOOGL", "MSFT"]'
```

## 🏆 Top Performers

**Endpoint:** `GET /stock/top-performers`

Get top performing stocks in various categories.

### Query Parameters
- `category` (string): Performance category
  - `change` - Best daily price change percentage
  - `volume` - Highest trading volume
  - `market_cap` - Largest market capitalization
- `limit` (integer): Number of top performers to return (1-50, default: 10)

### Response
```json
{
  "category": "change",
  "timeframe": "1 day",
  "performers": [
    {
      "symbol": "TSLA",
      "name": "Tesla, Inc.",
      "current_price": 245.30,
      "change_percent": 5.67,
      "volume": 125000000,
      "market_cap": 780000000000,
      "currency": "USD"
    }
  ],
  "total_analyzed": 30,
  "generation_date": "2025-08-07T16:30:00.000Z"
}
```

### Example Usage
```bash
# Get top 5 stocks by price change
curl "http://localhost:8000/stock/top-performers?category=change&limit=5"

# Get top 10 stocks by volume
curl "http://localhost:8000/stock/top-performers?category=volume&limit=10"

# Get top 3 stocks by market cap
curl "http://localhost:8000/stock/top-performers?category=market_cap&limit=3"
```

## 💡 Investment Recommendations

**Endpoint:** `GET /stock/recommend/{symbol}`

Get AI-powered investment recommendation for a specific stock.

### Path Parameters
- `symbol` (string): Stock symbol (e.g., "AAPL")

### Response
```json
{
  "symbol": "AAPL",
  "score": 75.5,
  "recommendation": "BUY",
  "reasons": [
    "Strong positive momentum (+2.5% today)",
    "AI predicts +4.2% price increase",
    "High trading volume indicates strong interest",
    "Large-cap stock provides stability"
  ],
  "technical_signals": {
    "momentum": "BULLISH",
    "ai_prediction": "POSITIVE",
    "volume": "HIGH",
    "market_cap": "LARGE_CAP"
  },
  "risk_level": "MEDIUM"
}
```

### Recommendation Logic
- **Score Range:** 0-100
  - 70-100: BUY recommendation
  - 55-69: HOLD recommendation
  - 0-54: SELL recommendation

- **Risk Levels:**
  - LOW: Stable, low volatility stocks
  - MEDIUM: Moderate volatility, balanced risk
  - HIGH: High volatility, speculative stocks

### Example Usage
```bash
curl "http://localhost:8000/stock/recommend/AAPL"
```

## 🧠 AI Analysis Factors

The recommendation engine considers multiple factors:

### Technical Indicators
- Daily price change momentum
- AI prediction confidence and direction
- Trading volume analysis
- Market capitalization for stability assessment

### Scoring System
- **Momentum Analysis:** +/-15 points for strong moves (>5%)
- **AI Predictions:** +/-20 points for significant predictions (>3%)
- **Volume Analysis:** +5 points for high volume
- **Stability Factor:** +5 points for large-cap stocks

### Risk Assessment
- High volatility (>10% daily change) = HIGH risk
- Moderate movement = MEDIUM risk
- Stable movement = LOW risk

## 🚀 Use Cases

### Portfolio Screening
Use the screening endpoint to find stocks that meet your investment criteria:
```bash
# Find large-cap tech stocks under $300
curl -X POST "http://localhost:8000/stock/screen" \
     -H "Content-Type: application/json" \
     -d '{
       "min_market_cap": 50000000000,
       "max_price": 300,
       "symbols": ["AAPL", "GOOGL", "MSFT", "META", "NVDA"]
     }'
```

### Daily Winners Analysis
Find today's best performing stocks:
```bash
curl "http://localhost:8000/stock/top-performers?category=change&limit=10"
```

### Investment Decision Support
Get comprehensive analysis for investment decisions:
```bash
# Compare top tech stocks
curl -X POST "http://localhost:8000/stock/compare" \
     -H "Content-Type: application/json" \
     -d '["AAPL", "GOOGL", "MSFT", "META"]'

# Get recommendation for each
curl "http://localhost:8000/stock/recommend/AAPL"
curl "http://localhost:8000/stock/recommend/GOOGL"
```

## ⚠️ Important Notes

1. **Data Dependencies:** All endpoints require real-time stock data from yfinance
2. **Rate Limiting:** Consider implementing rate limiting for production use
3. **Market Hours:** Recommendations are based on latest available data
4. **Risk Disclaimer:** These are analytical tools, not financial advice
5. **Network Requirements:** Requires internet access to fetch stock data

## 🔧 Error Handling

All endpoints return consistent error responses:

```json
{
  "detail": "Error message describing what went wrong"
}
```

Common error codes:
- `400`: Bad request (invalid parameters)
- `404`: Stock symbol not found
- `422`: Unable to process data (insufficient information)
- `500`: Internal server error

## 📈 Integration Examples

### Python Client
```python
import requests

# Screen for value stocks
response = requests.post(
    "http://localhost:8000/stock/screen",
    json={
        "max_pe_ratio": 20,
        "min_market_cap": 10000000000,
        "symbols": ["AAPL", "GOOGL", "MSFT"]
    }
)
screened_stocks = response.json()

# Get recommendations for each
for stock in screened_stocks:
    rec_response = requests.get(f"http://localhost:8000/stock/recommend/{stock['symbol']}")
    recommendation = rec_response.json()
    print(f"{stock['symbol']}: {recommendation['recommendation']} (Score: {recommendation['score']})")
```

### JavaScript/TypeScript
```typescript
// Compare stocks
const symbols = ['AAPL', 'GOOGL', 'MSFT'];
const comparison = await fetch('http://localhost:8000/stock/compare', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(symbols)
}).then(res => res.json());

console.log(`Best performer: ${comparison.best_performer.symbol}`);
```

This comprehensive functionality makes it easy for users to "check the best options for stock market" by providing screening, comparison, performance analysis, and AI-powered recommendations all in one API.