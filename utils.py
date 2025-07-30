"""
Utility functions for the Stock Advisor backend.
Contains helper functions for data validation, formatting, and common operations.
"""

import re
from typing import List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def validate_stock_symbol(symbol: str) -> tuple[bool, str]:
    """
    Validate a stock symbol format.
    
    Args:
        symbol (str): Stock symbol to validate
        
    Returns:
        tuple[bool, str]: (is_valid, cleaned_symbol or error_message)
    """
    if not symbol:
        return False, "Stock symbol cannot be empty"
    
    # Clean and normalize symbol
    cleaned = symbol.upper().strip()
    
    # Basic validation: alphanumeric, dots, and hyphens allowed
    if not re.match(r'^[A-Z0-9.-]+$', cleaned):
        return False, "Stock symbol contains invalid characters"
    
    # Length check
    if len(cleaned) > 10:
        return False, "Stock symbol too long (max 10 characters)"
    
    if len(cleaned) < 1:
        return False, "Stock symbol too short"
    
    return True, cleaned

def validate_period(period: str) -> bool:
    """
    Validate a time period for historical data.
    
    Args:
        period (str): Time period string
        
    Returns:
        bool: True if valid period
    """
    valid_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    return period in valid_periods

def format_currency(amount: float, currency: str = "USD") -> str:
    """
    Format a number as currency.
    
    Args:
        amount (float): Amount to format
        currency (str): Currency code
        
    Returns:
        str: Formatted currency string
    """
    if currency == "USD":
        return f"${amount:,.2f}"
    else:
        return f"{amount:,.2f} {currency}"

def calculate_percent_change(current: float, previous: float) -> float:
    """
    Calculate percentage change between two values.
    
    Args:
        current (float): Current value
        previous (float): Previous value
        
    Returns:
        float: Percentage change
    """
    if previous == 0:
        return 0.0
    return ((current - previous) / previous) * 100

def format_large_number(number: int) -> str:
    """
    Format large numbers with appropriate suffixes (K, M, B, T).
    
    Args:
        number (int): Number to format
        
    Returns:
        str: Formatted number string
    """
    if number >= 1_000_000_000_000:
        return f"{number / 1_000_000_000_000:.1f}T"
    elif number >= 1_000_000_000:
        return f"{number / 1_000_000_000:.1f}B"
    elif number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number / 1_000:.1f}K"
    else:
        return str(number)

def get_trading_days_between(start_date: datetime, end_date: datetime) -> int:
    """
    Calculate the number of trading days between two dates.
    Approximation: assumes 5 trading days per week.
    
    Args:
        start_date (datetime): Start date
        end_date (datetime): End date
        
    Returns:
        int: Approximate number of trading days
    """
    days_diff = (end_date - start_date).days
    weeks = days_diff // 7
    remaining_days = days_diff % 7
    
    # Approximate trading days (5 days per week)
    trading_days = weeks * 5 + min(remaining_days, 5)
    return max(trading_days, 0)

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default if denominator is zero.
    
    Args:
        numerator (float): Numerator
        denominator (float): Denominator
        default (float): Default value if division by zero
        
    Returns:
        float: Result of division or default value
    """
    if denominator == 0:
        return default
    return numerator / denominator

def log_api_call(endpoint: str, symbol: Optional[str] = None, **params):
    """
    Log API call information for monitoring and debugging.
    
    Args:
        endpoint (str): API endpoint name
        symbol (str, optional): Stock symbol if applicable
        **params: Additional parameters to log
    """
    log_msg = f"API Call: {endpoint}"
    if symbol:
        log_msg += f" | Symbol: {symbol}"
    
    if params:
        param_str = " | ".join([f"{k}: {v}" for k, v in params.items()])
        log_msg += f" | Params: {param_str}"
    
    logger.info(log_msg)

def create_error_response(error_type: str, message: str, symbol: Optional[str] = None) -> dict:
    """
    Create a standardized error response.
    
    Args:
        error_type (str): Type of error
        message (str): Error message
        symbol (str, optional): Stock symbol if applicable
        
    Returns:
        dict: Standardized error response
    """
    response = {
        "error": error_type,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }
    
    if symbol:
        response["symbol"] = symbol
    
    return response

def get_market_status() -> dict:
    """
    Get basic market status information.
    Note: This is a simplified version. In production, you might want to
    integrate with a real-time market status API.
    
    Returns:
        dict: Market status information
    """
    now = datetime.now()
    
    # Simple market hours check (NYSE: 9:30 AM - 4:00 PM ET, Monday-Friday)
    # This is a simplified check and doesn't account for holidays
    weekday = now.weekday()  # 0 = Monday, 6 = Sunday
    hour = now.hour
    
    is_market_hours = (
        weekday < 5 and  # Monday to Friday
        9 <= hour < 16   # 9 AM to 4 PM (simplified)
    )
    
    return {
        "is_market_open": is_market_hours,
        "current_time": now.isoformat(),
        "timezone": "EST",  # Simplified
        "next_market_open": "Next business day 9:30 AM EST" if not is_market_hours else "Market is open",
        "note": "This is a simplified market status check"
    }
