<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Stock Advisor Backend Project

This is a FastAPI-based stock analysis and prediction backend using machine learning.

## Project Structure
- `app.py`: Main FastAPI application with all REST endpoints
- `model.py`: StockPredictor class containing ML logic for price prediction
- Technical indicators: SMA, RSI, MACD, Bollinger Bands
- Uses Random Forest Regressor for predictions
- Integrates with yfinance for real-time stock data

## Code Guidelines
- Use comprehensive error handling with HTTPException
- Include detailed logging for debugging
- Follow FastAPI best practices for endpoint definitions
- Use Pydantic models for request/response validation
- Maintain separation of concerns (API logic in app.py, ML logic in model.py)
- Include proper type hints throughout the codebase

## Key Libraries
- FastAPI for web framework
- yfinance for stock data
- scikit-learn for machine learning
- pandas/numpy for data manipulation
- uvicorn for ASGI server
