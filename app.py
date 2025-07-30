from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging
import yfinance as yf
from datetime import datetime, timedelta
import uvicorn

from model import StockPredictor
from advanced_model import AdvancedStockPredictor
from currency_utils import get_currency_from_symbol, get_exchange_name

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Stock Advisor API",
    description="A FastAPI backend for stock analysis and price prediction",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for frontend compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class StockInfoResponse(BaseModel):
    symbol: str
    name: str
    current_price: float
    previous_close: float
    change: float
    change_percent: float
    volume: int
    market_cap: Optional[int] = None
    pe_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    currency: str
    exchange: str

class PredictionResponse(BaseModel):
    symbol: str
    current_price: float
    predicted_price: float
    price_change_pct: float
    prediction_date: str
    model_confidence: str

class AdvancedPredictionResponse(BaseModel):
    symbol: str
    current_price: float
    predicted_price: float
    price_change: float
    price_change_pct: float
    prediction_date: str
    model_confidence: str
    confidence_score: float
    individual_predictions: Dict[str, float]
    model_weights: Dict[str, float]
    prediction_std: float
    prediction_range: float

class HistoricalDataResponse(BaseModel):
    symbol: str
    data: List[Dict[str, Any]]
    period: str
    total_records: int

class ErrorResponse(BaseModel):
    error: str
    message: str
    symbol: Optional[str] = None

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        dict: API status and timestamp
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Stock Advisor API",
        "version": "1.0.0"
    }

# Get basic stock information
@app.get("/stock/info/{symbol}", response_model=StockInfoResponse)
async def get_stock_info(symbol: str):
    """
    Get basic stock information including current price, volume, and key metrics.
    
    Args:
        symbol (str): Stock symbol (e.g., 'AAPL', 'GOOGL')
        
    Returns:
        StockInfoResponse: Basic stock information
        
    Raises:
        HTTPException: If stock symbol is invalid or data cannot be fetched
    """
    try:
        logger.info(f"Fetching stock info for {symbol}")
        
        # Validate and clean symbol
        symbol = symbol.upper().strip()
        if not symbol or len(symbol) > 10:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid stock symbol: {symbol}"
            )
        
        # Fetch stock data
        ticker = yf.Ticker(symbol)
        info = ticker.info
        hist = ticker.history(period="2d")
        
        if hist.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No data found for stock symbol: {symbol}"
            )
        
        # Extract current and previous prices
        current_price = float(hist['Close'].iloc[-1])
        previous_close = float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
        
        # Calculate change
        change = current_price - previous_close
        change_percent = (change / previous_close) * 100 if previous_close != 0 else 0.0
        
        # Get currency and exchange information
        currency = get_currency_from_symbol(symbol)
        exchange = get_exchange_name(symbol)
        
        # Build response
        stock_info = StockInfoResponse(
            symbol=symbol,
            name=info.get('longName', symbol),
            current_price=current_price,
            previous_close=previous_close,
            change=change,
            change_percent=change_percent,
            volume=int(hist['Volume'].iloc[-1]),
            market_cap=info.get('marketCap'),
            pe_ratio=info.get('trailingPE'),
            dividend_yield=info.get('dividendYield'),
            currency=currency,
            exchange=exchange
        )
        
        logger.info(f"Successfully fetched info for {symbol}")
        return stock_info
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching stock info for {symbol}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal error while fetching stock info for {symbol}"
        )

# Get historical stock data
@app.get("/stock/history/{symbol}", response_model=HistoricalDataResponse)
async def get_stock_history(
    symbol: str,
    period: str = Query(default="1y", description="Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)")
):
    """
    Get historical stock price data.
    
    Args:
        symbol (str): Stock symbol
        period (str): Time period for historical data
        
    Returns:
        HistoricalDataResponse: Historical stock data
        
    Raises:
        HTTPException: If symbol is invalid or data cannot be fetched
    """
    try:
        logger.info(f"Fetching historical data for {symbol} with period {period}")
        
        # Validate symbol
        symbol = symbol.upper().strip()
        if not symbol:
            raise HTTPException(status_code=400, detail="Stock symbol is required")
        
        # Validate period
        valid_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
        if period not in valid_periods:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid period. Must be one of: {', '.join(valid_periods)}"
            )
        
        # Fetch historical data
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        
        if hist.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No historical data found for {symbol}"
            )
        
        # Convert to list of dictionaries
        data_list = []
        for date, row in hist.iterrows():
            data_list.append({
                "date": date.strftime('%Y-%m-%d'),
                "open": float(row['Open']),
                "high": float(row['High']),
                "low": float(row['Low']),
                "close": float(row['Close']),
                "volume": int(row['Volume'])
            })
        
        response = HistoricalDataResponse(
            symbol=symbol,
            data=data_list,
            period=period,
            total_records=len(data_list)
        )
        
        logger.info(f"Successfully fetched {len(data_list)} historical records for {symbol}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching historical data for {symbol}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal error while fetching historical data for {symbol}"
        )

# Predict future stock prices
@app.get("/stock/predict/{symbol}", response_model=PredictionResponse)
async def predict_stock_price(
    symbol: str,
    days_ahead: int = Query(default=1, ge=1, le=30, description="Number of days to predict ahead (1-30)")
):
    """
    Predict future stock prices using machine learning.
    
    Args:
        symbol (str): Stock symbol
        days_ahead (int): Number of days to predict ahead (1-30)
        
    Returns:
        PredictionResponse: Price prediction results
        
    Raises:
        HTTPException: If prediction fails or symbol is invalid
    """
    try:
        logger.info(f"Generating prediction for {symbol}, {days_ahead} days ahead")
        
        # Validate symbol
        symbol = symbol.upper().strip()
        if not symbol:
            raise HTTPException(status_code=400, detail="Stock symbol is required")
        
        # Initialize predictor
        predictor = StockPredictor(symbol)
        
        # Fetch and prepare data
        stock_data = predictor.fetch_stock_data(period="2y")
        if stock_data is None:
            raise HTTPException(
                status_code=404,
                detail=f"Unable to fetch data for stock symbol: {symbol}"
            )
        
        # Create features
        featured_data = predictor.create_features(stock_data)
        if featured_data is None or featured_data.empty:
            raise HTTPException(
                status_code=422,
                detail=f"Unable to create features for {symbol}. Insufficient data."
            )
        
        # Train model
        if not predictor.train_model(featured_data):
            raise HTTPException(
                status_code=500,
                detail=f"Failed to train prediction model for {symbol}"
            )
        
        # Generate prediction
        prediction = predictor.predict_price(days_ahead=days_ahead)
        if prediction is None:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate prediction for {symbol}"
            )
        
        response = PredictionResponse(**prediction)
        logger.info(f"Successfully generated prediction for {symbol}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error predicting stock price for {symbol}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal error while predicting stock price for {symbol}"
        )

# Advanced ML Prediction with Ensemble Models
@app.get("/stock/predict-advanced/{symbol}", response_model=AdvancedPredictionResponse)
async def predict_stock_price_advanced(
    symbol: str,
    period: str = Query(default="3y", description="Training data period (1y, 2y, 3y, 5y)")
):
    """
    Predict future stock prices using advanced ensemble machine learning.
    
    This endpoint uses multiple algorithms (Random Forest, Gradient Boosting, 
    Neural Networks, SVR, Extra Trees) with advanced technical indicators
    for more precise predictions.
    
    Args:
        symbol (str): Stock symbol
        period (str): Training data period (1y, 2y, 3y, 5y)
        
    Returns:
        AdvancedPredictionResponse: Detailed prediction results with confidence metrics
        
    Raises:
        HTTPException: If prediction fails or symbol is invalid
    """
    try:
        logger.info(f"Generating advanced prediction for {symbol} with {period} training data")
        
        # Validate symbol
        symbol = symbol.upper().strip()
        if not symbol:
            raise HTTPException(status_code=400, detail="Stock symbol is required")
        
        # Initialize advanced predictor
        try:
            predictor = AdvancedStockPredictor(symbol)
        except Exception as e:
            logger.error(f"Failed to initialize advanced predictor: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize advanced predictor: {str(e)}"
            )
        
        # Train and predict in one step
        try:
            prediction = predictor.train_and_predict(period=period)
        except Exception as e:
            logger.error(f"Failed during training/prediction: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed during advanced prediction training: {str(e)}"
            )
        
        if prediction is None:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate advanced prediction for {symbol}"
            )
        
        response = AdvancedPredictionResponse(**prediction)
        logger.info(f"Successfully generated advanced prediction for {symbol}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating advanced prediction for {symbol}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal error while generating advanced prediction for {symbol}: {str(e)}"
        )

# Get model information
@app.get("/stock/model-info/{symbol}")
async def get_model_info(symbol: str):
    """
    Get information about the trained model for a specific stock.
    
    Args:
        symbol (str): Stock symbol
        
    Returns:
        dict: Model information and feature importance
    """
    try:
        logger.info(f"Getting model info for {symbol}")
        
        symbol = symbol.upper().strip()
        predictor = StockPredictor(symbol)
        
        # Fetch and prepare data
        stock_data = predictor.fetch_stock_data(period="1y")
        if stock_data is None:
            raise HTTPException(
                status_code=404,
                detail=f"Unable to fetch data for {symbol}"
            )
        
        featured_data = predictor.create_features(stock_data)
        if featured_data is None:
            raise HTTPException(
                status_code=422,
                detail=f"Unable to create features for {symbol}"
            )
        
        # Train model
        if not predictor.train_model(featured_data):
            raise HTTPException(
                status_code=500,
                detail=f"Failed to train model for {symbol}"
            )
        
        model_info = predictor.get_model_info()
        return model_info
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting model info for {symbol}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal error while getting model info for {symbol}"
        )

# Get advanced model information
@app.get("/stock/model-info-advanced/{symbol}")
async def get_advanced_model_info(
    symbol: str,
    period: str = Query(default="3y", description="Training data period")
):
    """
    Get information about the trained advanced ensemble models for a specific stock.
    
    Args:
        symbol (str): Stock symbol
        period (str): Training data period
        
    Returns:
        dict: Advanced model information, scores, and feature importance
    """
    try:
        logger.info(f"Getting advanced model info for {symbol}")
        
        symbol = symbol.upper().strip()
        predictor = AdvancedStockPredictor(symbol)
        
        # Train models to get info
        _ = predictor.train_and_predict(period=period)
        
        model_info = predictor.get_model_info()
        return model_info
        
    except Exception as e:
        logger.error(f"Error getting advanced model info for {symbol}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal error while getting advanced model info for {symbol}"
        )

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors.
    """
    logger.error(f"Unhandled error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later."
        }
    )

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
