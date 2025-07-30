import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Any
import logging
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import yfinance as yf
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockPredictor:
    """
    A machine learning model for predicting stock prices using technical indicators.
    
    This class fetches historical stock data, computes technical indicators,
    trains a Random Forest model, and makes price predictions.
    """
    
    def __init__(self, symbol: str):
        """
        Initialize the StockPredictor with a stock symbol.
        
        Args:
            symbol (str): Stock symbol (e.g., 'AAPL', 'GOOGL')
        """
        self.symbol = symbol.upper()
        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            max_depth=10,
            min_samples_split=5
        )
        self.is_trained = False
        self.feature_columns = []
        
    def fetch_stock_data(self, period: str = "2y") -> Optional[pd.DataFrame]:
        """
        Fetch historical stock data using yfinance.
        
        Args:
            period (str): Time period for data ('1y', '2y', '5y', etc.)
            
        Returns:
            pd.DataFrame: Historical stock data or None if error
        """
        try:
            logger.info(f"Fetching data for {self.symbol} with period {period}")
            ticker = yf.Ticker(self.symbol)
            data = ticker.history(period=period)
            
            if data.empty:
                logger.error(f"No data found for symbol {self.symbol}")
                return None
                
            logger.info(f"Successfully fetched {len(data)} records for {self.symbol}")
            return data
            
        except Exception as e:
            logger.error(f"Error fetching data for {self.symbol}: {str(e)}")
            return None
    
    def calculate_sma(self, data: pd.DataFrame, window: int = 20) -> pd.Series:
        """Calculate Simple Moving Average."""
        return data['Close'].rolling(window=window).mean()
    
    def calculate_rsi(self, data: pd.DataFrame, window: int = 14) -> pd.Series:
        """
        Calculate Relative Strength Index (RSI).
        
        Args:
            data (pd.DataFrame): Stock data
            window (int): RSI calculation window
            
        Returns:
            pd.Series: RSI values
        """
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, data: pd.DataFrame, 
                      fast_period: int = 12, 
                      slow_period: int = 26, 
                      signal_period: int = 9) -> Dict[str, pd.Series]:
        """
        Calculate MACD (Moving Average Convergence Divergence).
        
        Args:
            data (pd.DataFrame): Stock data
            fast_period (int): Fast EMA period
            slow_period (int): Slow EMA period
            signal_period (int): Signal line EMA period
            
        Returns:
            Dict[str, pd.Series]: MACD line, signal line, and histogram
        """
        exp1 = data['Close'].ewm(span=fast_period).mean()
        exp2 = data['Close'].ewm(span=slow_period).mean()
        macd_line = exp1 - exp2
        signal_line = macd_line.ewm(span=signal_period).mean()
        histogram = macd_line - signal_line
        
        return {
            'macd': macd_line,
            'signal': signal_line,
            'histogram': histogram
        }
    
    def create_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Create technical indicator features for machine learning.
        
        Args:
            data (pd.DataFrame): Raw stock data
            
        Returns:
            pd.DataFrame: Data with technical indicator features
        """
        try:
            logger.info(f"Creating features for {self.symbol}")
            
            # Create a copy to avoid modifying original data
            df = data.copy()
            
            # Basic price features
            df['Price_Change'] = df['Close'].pct_change()
            df['High_Low_Ratio'] = df['High'] / df['Low']
            df['Volume_Change'] = df['Volume'].pct_change()
            
            # Moving averages
            df['SMA_5'] = self.calculate_sma(df, 5)
            df['SMA_10'] = self.calculate_sma(df, 10)
            df['SMA_20'] = self.calculate_sma(df, 20)
            df['SMA_50'] = self.calculate_sma(df, 50)
            
            # Price relative to moving averages
            df['Price_SMA_5_Ratio'] = df['Close'] / df['SMA_5']
            df['Price_SMA_20_Ratio'] = df['Close'] / df['SMA_20']
            
            # RSI
            df['RSI'] = self.calculate_rsi(df)
            
            # MACD
            macd_data = self.calculate_macd(df)
            df['MACD'] = macd_data['macd']
            df['MACD_Signal'] = macd_data['signal']
            df['MACD_Histogram'] = macd_data['histogram']
            
            # Bollinger Bands
            sma_20 = df['SMA_20']
            std_20 = df['Close'].rolling(window=20).std()
            df['BB_Upper'] = sma_20 + (std_20 * 2)
            df['BB_Lower'] = sma_20 - (std_20 * 2)
            df['BB_Position'] = (df['Close'] - df['BB_Lower']) / (df['BB_Upper'] - df['BB_Lower'])
            
            # Volatility
            df['Volatility'] = df['Close'].rolling(window=20).std()
            
            # Target variable (next day's closing price)
            df['Target'] = df['Close'].shift(-1)
            
            # Remove rows with NaN values
            df_clean = df.dropna()
            
            if df_clean.empty:
                logger.error("No valid data after feature creation")
                return None
                
            logger.info(f"Created {len(df_clean)} feature records")
            return df_clean
            
        except Exception as e:
            logger.error(f"Error creating features: {str(e)}")
            return None
    
    def train_model(self, data: pd.DataFrame) -> bool:
        """
        Train the Random Forest model with the provided data.
        
        Args:
            data (pd.DataFrame): Data with features and target
            
        Returns:
            bool: True if training successful, False otherwise
        """
        try:
            logger.info(f"Training model for {self.symbol}")
            
            # Define feature columns (exclude target and non-feature columns)
            exclude_columns = ['Target', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']
            self.feature_columns = [col for col in data.columns if col not in exclude_columns]
            
            # Prepare features and target
            X = data[self.feature_columns]
            y = data['Target']
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, shuffle=False
            )
            
            # Train model
            self.model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = self.model.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            
            logger.info(f"Model training completed. MAE: {mae:.2f}, RMSE: {rmse:.2f}")
            
            self.is_trained = True
            return True
            
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            return False
    
    def predict_price(self, days_ahead: int = 1) -> Optional[Dict[str, Any]]:
        """
        Predict future stock prices.
        
        Args:
            days_ahead (int): Number of days to predict ahead
            
        Returns:
            Dict[str, Any]: Prediction results or None if error
        """
        try:
            if not self.is_trained:
                logger.error("Model not trained. Call train_model() first.")
                return None
            
            # Fetch latest data
            latest_data = self.fetch_stock_data(period="6mo")
            if latest_data is None:
                return None
            
            # Create features
            featured_data = self.create_features(latest_data)
            if featured_data is None or featured_data.empty:
                return None
            
            # Get the most recent feature values
            latest_features = featured_data[self.feature_columns].iloc[-1:].fillna(0)
            
            # Make prediction
            predicted_price = self.model.predict(latest_features)[0]
            current_price = latest_data['Close'].iloc[-1]
            
            # Calculate prediction confidence (simplified)
            price_change_pct = ((predicted_price - current_price) / current_price) * 100
            
            prediction_result = {
                'symbol': self.symbol,
                'current_price': float(current_price),
                'predicted_price': float(predicted_price),
                'price_change_pct': float(price_change_pct),
                'prediction_date': (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d'),
                'model_confidence': 'medium'  # This could be enhanced with proper confidence intervals
            }
            
            logger.info(f"Prediction for {self.symbol}: ${predicted_price:.2f} ({price_change_pct:+.2f}%)")
            return prediction_result
            
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            return None
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the trained model.
        
        Returns:
            Dict[str, Any]: Model information
        """
        if not self.is_trained:
            return {'error': 'Model not trained'}
        
        feature_importance = dict(zip(
            self.feature_columns, 
            self.model.feature_importances_
        ))
        
        # Sort by importance
        sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'model_type': 'Random Forest Regressor',
            'n_estimators': self.model.n_estimators,
            'is_trained': self.is_trained,
            'feature_count': len(self.feature_columns),
            'top_features': sorted_features[:5],
            'symbol': self.symbol
        }
