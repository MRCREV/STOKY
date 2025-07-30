"""
Currency utilities for stock exchanges
"""

def get_currency_from_symbol(symbol: str) -> str:
    """
    Get currency code based on stock symbol and exchange
    
    Args:
        symbol (str): Stock symbol (e.g., 'AAPL', 'PETR4.SA')
        
    Returns:
        str: Currency code (e.g., 'USD', 'BRL', 'EUR')
    """
    symbol_upper = symbol.upper()
    
    # Brazilian stocks (.SA suffix)
    if '.SA' in symbol_upper:
        return 'BRL'
    
    # London Stock Exchange (.L suffix)
    if '.L' in symbol_upper:
        return 'GBP'
    
    # Tokyo Stock Exchange (.T suffix)
    if '.T' in symbol_upper:
        return 'JPY'
    
    # Toronto Stock Exchange (.TO suffix)
    if '.TO' in symbol_upper:
        return 'CAD'
    
    # Australian Securities Exchange (.AX suffix)
    if '.AX' in symbol_upper:
        return 'AUD'
    
    # Swiss Exchange (.SW suffix)
    if '.SW' in symbol_upper:
        return 'CHF'
    
    # Euronext exchanges (.PA, .AS, .BR, .MI suffixes)
    if any(suffix in symbol_upper for suffix in ['.PA', '.AS', '.BR', '.MI']):
        return 'EUR'
    
    # Hong Kong Stock Exchange (.HK suffix)
    if '.HK' in symbol_upper:
        return 'HKD'
    
    # Shanghai/Shenzhen Stock Exchange (.SS, .SZ suffixes)
    if any(suffix in symbol_upper for suffix in ['.SS', '.SZ']):
        return 'CNY'
    
    # Seoul Stock Exchange (.KS suffix)
    if '.KS' in symbol_upper:
        return 'KRW'
    
    # Bombay Stock Exchange (.BO suffix) or National Stock Exchange (.NS suffix)
    if any(suffix in symbol_upper for suffix in ['.BO', '.NS']):
        return 'INR'
    
    # Mexican Stock Exchange (.MX suffix)
    if '.MX' in symbol_upper:
        return 'MXN'
    
    # Default to USD for US stocks and unknown exchanges
    return 'USD'

def get_currency_symbol(currency_code: str) -> str:
    """
    Get currency symbol from currency code
    
    Args:
        currency_code (str): Currency code (e.g., 'USD', 'BRL')
        
    Returns:
        str: Currency symbol (e.g., '$', 'R$')
    """
    currency_symbols = {
        'USD': '$',
        'BRL': 'R$',
        'EUR': '€',
        'GBP': '£',
        'JPY': '¥',
        'CAD': 'C$',
        'AUD': 'A$',
        'CHF': 'CHF',
        'CNY': '¥',
        'INR': '₹',
        'KRW': '₩',
        'MXN': 'MX$',
        'HKD': 'HK$'
    }
    return currency_symbols.get(currency_code, currency_code)

def format_currency_with_symbol(amount: float, symbol: str) -> str:
    """
    Format currency with proper symbol based on stock exchange
    
    Args:
        amount (float): Amount to format
        symbol (str): Stock symbol to determine currency
        
    Returns:
        str: Formatted currency string with proper symbol
    """
    currency_code = get_currency_from_symbol(symbol)
    currency_symbol = get_currency_symbol(currency_code)
    
    # For some currencies like JPY and KRW, we don't want decimal places
    if currency_code in ['JPY', 'KRW']:
        return f"{currency_symbol}{amount:,.0f}"
    else:
        return f"{currency_symbol}{amount:,.2f}"

def get_exchange_name(symbol: str) -> str:
    """
    Get exchange name from symbol
    
    Args:
        symbol (str): Stock symbol
        
    Returns:
        str: Exchange name
    """
    symbol_upper = symbol.upper()
    
    if '.SA' in symbol_upper:
        return 'B3 (São Paulo)'
    if '.L' in symbol_upper:
        return 'London Stock Exchange'
    if '.T' in symbol_upper:
        return 'Tokyo Stock Exchange'
    if '.TO' in symbol_upper:
        return 'Toronto Stock Exchange'
    if '.AX' in symbol_upper:
        return 'Australian Securities Exchange'
    if '.SW' in symbol_upper:
        return 'Swiss Exchange'
    if '.PA' in symbol_upper:
        return 'Euronext Paris'
    if '.AS' in symbol_upper:
        return 'Euronext Amsterdam'
    if '.BR' in symbol_upper:
        return 'Euronext Brussels'
    if '.MI' in symbol_upper:
        return 'Borsa Italiana'
    if '.HK' in symbol_upper:
        return 'Hong Kong Stock Exchange'
    if '.SS' in symbol_upper:
        return 'Shanghai Stock Exchange'
    if '.SZ' in symbol_upper:
        return 'Shenzhen Stock Exchange'
    if '.KS' in symbol_upper:
        return 'Korea Exchange'
    if '.BO' in symbol_upper:
        return 'Bombay Stock Exchange'
    if '.NS' in symbol_upper:
        return 'National Stock Exchange of India'
    if '.MX' in symbol_upper:
        return 'Mexican Stock Exchange'
    
    return 'NASDAQ/NYSE'
