import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Any
import logging
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.metrics import r2_score
import yfinance as yf
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedStockPredictor:
    """
    Advanced machine learning model for precise stock price predictions.
    
    Features:
    - Multiple algorithms ensemble
    - Advanced technical indicators
    - Time series validation
    - Feature importance analysis
    - Volatility modeling
    - Market sentiment indicators
    """
    
    def __init__(self, symbol: str):
        """
        Initialize the AdvancedStockPredictor with a stock symbol.
        
        Args:
            symbol (str): Stock symbol (e.g., 'AAPL', 'GOOGL')
        """
        self.symbol = symbol.upper()
        self.models = {}
        self.scaler = RobustScaler()
        self.is_trained = False
        self.feature_columns = []
        self.feature_importance = {}
        self.model_scores = {}
        
        # Initialize multiple models
        self._initialize_models()
        
    def _initialize_models(self):
        """Initialize multiple ML models for ensemble prediction."""
        self.models = {
            'random_forest': RandomForestRegressor(
                n_estimators=50,  # Reduced from 200
                max_depth=10,     # Reduced from 15
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=2          # Limited parallel jobs
            ),
            'gradient_boosting': GradientBoostingRegressor(
                n_estimators=50,  # Reduced from 150
                learning_rate=0.1,
                max_depth=6,      # Reduced from 8
                random_state=42
            ),
            'extra_trees': ExtraTreesRegressor(
                n_estimators=50,  # Reduced from 150
                max_depth=8,      # Reduced from 12
                min_samples_split=3,
                random_state=42,
                n_jobs=2          # Limited parallel jobs
            )
        }
        
    def fetch_stock_data(self, period: str = "3y") -> Optional[pd.DataFrame]:
        """
        Fetch historical stock data using yfinance.
        
        Args:
            period (str): Time period for data ('1y', '2y', '3y', '5y', etc.)
            
        Returns:
            pd.DataFrame: Historical stock data or None if error
        """
        try:
            logger.info("Fetching %s data for %s", period, self.symbol)
            ticker = yf.Ticker(self.symbol)
            data = ticker.history(period=period)
            
            if data.empty:
                logger.error("No data found for symbol %s", self.symbol)
                return None
                
            logger.info("Fetched %d trading days of data", len(data))
            return data
            
        except Exception as e:
            logger.error("Error fetching data for %s: %s", self.symbol, e)
            return None
    
    def calculate_advanced_sma(self, data: pd.DataFrame, periods: List[int]) -> pd.DataFrame:
        """Calculate multiple Simple Moving Averages."""
        df = data.copy()
        for period in periods:
            df[f'SMA_{period}'] = data['Close'].rolling(window=period).mean()
            df[f'SMA_{period}_slope'] = df[f'SMA_{period}'].diff()
        return df
    
    def calculate_ema(self, data: pd.DataFrame, periods: List[int]) -> pd.DataFrame:
        """Calculate Exponential Moving Averages."""
        df = data.copy()
        for period in periods:
            df[f'EMA_{period}'] = data['Close'].ewm(span=period).mean()
        return df
    
    def calculate_bollinger_bands(self, data: pd.DataFrame, period: int = 20, std_dev: int = 2) -> pd.DataFrame:
        """
        Calculate Bollinger Bands.
        
        Args:
            data: Stock data
            period: Period for moving average
            std_dev: Number of standard deviations
        """
        df = data.copy()
        sma = data['Close'].rolling(window=period).mean()
        std = data['Close'].rolling(window=period).std()
        
        df['BB_Upper'] = sma + (std * std_dev)
        df['BB_Lower'] = sma - (std * std_dev)
        df['BB_Middle'] = sma
        df['BB_Width'] = df['BB_Upper'] - df['BB_Lower']
        df['BB_Position'] = (data['Close'] - df['BB_Lower']) / df['BB_Width']
        
        return df
    
    def calculate_rsi(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index (RSI)."""
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, data: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        """Calculate MACD indicators."""
        df = data.copy()
        exp1 = data['Close'].ewm(span=fast).mean()
        exp2 = data['Close'].ewm(span=slow).mean()
        
        df['MACD'] = exp1 - exp2
        df['MACD_Signal'] = df['MACD'].ewm(span=signal).mean()
        df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
        
        return df
    
    def calculate_stochastic(self, data: pd.DataFrame, k_period: int = 14, d_period: int = 3) -> pd.DataFrame:
        """Calculate Stochastic Oscillator."""
        df = data.copy()
        low_min = data['Low'].rolling(window=k_period).min()
        high_max = data['High'].rolling(window=k_period).max()
        
        df['Stoch_K'] = 100 * (data['Close'] - low_min) / (high_max - low_min)
        df['Stoch_D'] = df['Stoch_K'].rolling(window=d_period).mean()
        
        return df
    
    def calculate_williams_r(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Williams %R."""
        high_max = data['High'].rolling(window=period).max()
        low_min = data['Low'].rolling(window=period).min()
        williams_r = -100 * (high_max - data['Close']) / (high_max - low_min)
        return williams_r
    
    def calculate_atr(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Average True Range (ATR) for volatility."""
        high_low = data['High'] - data['Low']
        high_close = np.abs(data['High'] - data['Close'].shift())
        low_close = np.abs(data['Low'] - data['Close'].shift())
        
        true_range = np.maximum(high_low, np.maximum(high_close, low_close))
        atr = true_range.rolling(window=period).mean()
        return atr
    
    def calculate_adx(self, data: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """Calculate Average Directional Index (ADX)."""
        df = data.copy()
        
        # Calculate True Range
        df['TR'] = self.calculate_atr(data, 1)
        
        # Calculate Directional Movement
        df['DM_Plus'] = np.where((data['High'] - data['High'].shift()) > (data['Low'].shift() - data['Low']),
                                np.maximum(data['High'] - data['High'].shift(), 0), 0)
        df['DM_Minus'] = np.where((data['Low'].shift() - data['Low']) > (data['High'] - data['High'].shift()),
                                 np.maximum(data['Low'].shift() - data['Low'], 0), 0)
        
        # Calculate Directional Indicators
        df['DI_Plus'] = 100 * (df['DM_Plus'].rolling(window=period).mean() / df['TR'].rolling(window=period).mean())
        df['DI_Minus'] = 100 * (df['DM_Minus'].rolling(window=period).mean() / df['TR'].rolling(window=period).mean())
        
        # Calculate ADX
        df['DX'] = 100 * np.abs(df['DI_Plus'] - df['DI_Minus']) / (df['DI_Plus'] + df['DI_Minus'])
        df['ADX'] = df['DX'].rolling(window=period).mean()
        
        return df[['DI_Plus', 'DI_Minus', 'ADX']]
    
    def calculate_volume_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate volume-based indicators."""
        df = data.copy()
        
        # Volume moving averages
        df['Volume_SMA_10'] = data['Volume'].rolling(window=10).mean()
        df['Volume_SMA_20'] = data['Volume'].rolling(window=20).mean()
        df['Volume_Ratio'] = data['Volume'] / df['Volume_SMA_20']
        
        # On-Balance Volume (OBV)
        df['OBV'] = (np.sign(data['Close'].diff()) * data['Volume']).fillna(0).cumsum()
        
        # Volume Price Trend (VPT)
        df['VPT'] = (data['Volume'] * data['Close'].pct_change()).fillna(0).cumsum()
        
        return df
    
    def calculate_price_patterns(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate price pattern indicators."""
        df = data.copy()
        
        # Price gaps
        df['Gap_Up'] = np.where(data['Open'] > data['High'].shift(), 1, 0)
        df['Gap_Down'] = np.where(data['Open'] < data['Low'].shift(), 1, 0)
        
        # Doji patterns
        body_size = np.abs(data['Close'] - data['Open'])
        candle_size = data['High'] - data['Low']
        df['Doji'] = np.where(body_size < (candle_size * 0.1), 1, 0)
        
        # Hammer patterns
        lower_shadow = np.minimum(data['Open'], data['Close']) - data['Low']
        upper_shadow = data['High'] - np.maximum(data['Open'], data['Close'])
        df['Hammer'] = np.where((lower_shadow > 2 * body_size) & (upper_shadow < body_size), 1, 0)
        
        return df
    
    def create_advanced_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Create comprehensive technical indicator features for machine learning.
        
        Args:
            data (pd.DataFrame): Raw stock data
            
        Returns:
            pd.DataFrame: Data with advanced technical indicator features
        """
        try:
            logger.info("Creating advanced features for %s", self.symbol)
            
            # Create a copy to avoid modifying original data
            df = data.copy()
            
            # Basic price features
            df['Price_Change'] = data['Close'].pct_change()
            df['Price_Change_2d'] = data['Close'].pct_change(periods=2)
            df['Price_Change_5d'] = data['Close'].pct_change(periods=5)
            df['High_Low_Ratio'] = data['High'] / data['Low']
            df['Open_Close_Ratio'] = data['Open'] / data['Close']
            
            # Moving averages
            sma_periods = [5, 10, 20, 50, 100, 200]
            ema_periods = [12, 26, 50, 100]
            
            df = self.calculate_advanced_sma(df, sma_periods)
            df = self.calculate_ema(df, ema_periods)
            
            # Price relative to moving averages
            for period in sma_periods:
                df[f'Price_SMA_{period}_Ratio'] = data['Close'] / df[f'SMA_{period}']
                
            # Bollinger Bands
            df = self.calculate_bollinger_bands(df)
            
            # Momentum indicators
            df['RSI'] = self.calculate_rsi(data)
            df['RSI_14'] = self.calculate_rsi(data, 14)
            df['RSI_21'] = self.calculate_rsi(data, 21)
            
            # MACD
            macd_df = self.calculate_macd(data)
            df = pd.concat([df, macd_df[['MACD', 'MACD_Signal', 'MACD_Histogram']]], axis=1)
            
            # Stochastic
            stoch_df = self.calculate_stochastic(data)
            df = pd.concat([df, stoch_df[['Stoch_K', 'Stoch_D']]], axis=1)
            
            # Williams %R
            df['Williams_R'] = self.calculate_williams_r(data)
            
            # Volatility indicators
            df['ATR'] = self.calculate_atr(data)
            df['ATR_Ratio'] = df['ATR'] / data['Close']
            
            # ADX
            adx_df = self.calculate_adx(data)
            df = pd.concat([df, adx_df], axis=1)
            
            # Volume indicators
            volume_df = self.calculate_volume_indicators(df)
            df = pd.concat([df, volume_df[['Volume_SMA_10', 'Volume_SMA_20', 'Volume_Ratio', 'OBV', 'VPT']]], axis=1)
            
            # Price patterns
            pattern_df = self.calculate_price_patterns(data)
            df = pd.concat([df, pattern_df[['Gap_Up', 'Gap_Down', 'Doji', 'Hammer']]], axis=1)
            
            # Lagged features
            for lag in [1, 2, 3, 5]:
                df[f'Close_Lag_{lag}'] = data['Close'].shift(lag)
                df[f'Volume_Lag_{lag}'] = data['Volume'].shift(lag)
                df[f'RSI_Lag_{lag}'] = df['RSI'].shift(lag)
            
            # Rolling statistics
            df['Close_Rolling_Std_10'] = data['Close'].rolling(window=10).std()
            df['Close_Rolling_Std_20'] = data['Close'].rolling(window=20).std()
            df['Volume_Rolling_Std_10'] = data['Volume'].rolling(window=10).std()
            
            # Market timing features
            df['Day_of_Week'] = df.index.dayofweek
            df['Month'] = df.index.month
            df['Quarter'] = df.index.quarter
            
            # Target variable (next day's closing price)
            df['Target'] = data['Close'].shift(-1)
            
            # Remove rows with NaN values
            df = df.dropna()
            
            logger.info("Created %d features from %d rows", len(df.columns), len(data))
            return df
            
        except Exception as e:
            logger.error("Error creating features: %s", e)
            return None
    
    def train_models(self, data: pd.DataFrame) -> bool:
        """
        Train multiple ML models using time series validation.
        
        Args:
            data (pd.DataFrame): Prepared data with features
            
        Returns:
            bool: True if training successful, False otherwise
        """
        try:
            logger.info("Starting model training with time series validation")
            
            # Prepare features and target
            feature_cols = [col for col in data.columns if col not in ['Target', 'Close', 'Open', 'High', 'Low', 'Volume']]
            self.feature_columns = feature_cols
            
            X = data[feature_cols]
            y = data['Target']
            
            logger.info("Training with %d features and %d samples", len(feature_cols), len(X))
            
            # Time series split for validation
            tscv = TimeSeriesSplit(n_splits=5)
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train each model
            for name, model in self.models.items():
                logger.info("Training %s", name)
                
                # Time series cross-validation
                cv_scores = []
                for train_idx, val_idx in tscv.split(X_scaled):
                    X_train, X_val = X_scaled[train_idx], X_scaled[val_idx]
                    y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
                    
                    # Train model
                    if name == 'neural_network':
                        # Scale target for neural network
                        y_scaler = StandardScaler()
                        y_train_scaled = y_scaler.fit_transform(y_train.values.reshape(-1, 1)).ravel()
                        model.fit(X_train, y_train_scaled)
                        y_pred_scaled = model.predict(X_val)
                        y_pred = y_scaler.inverse_transform(y_pred_scaled.reshape(-1, 1)).ravel()
                    else:
                        model.fit(X_train, y_train)
                        y_pred = model.predict(X_val)
                    
                    # Calculate score
                    score = r2_score(y_val, y_pred)
                    cv_scores.append(score)
                
                # Store average CV score
                avg_score = np.mean(cv_scores)
                self.model_scores[name] = avg_score
                logger.info("%s CV Score: %.4f", name, avg_score)
                
                # Final training on all data
                if name == 'neural_network':
                    y_scaler = StandardScaler()
                    y_scaled = y_scaler.fit_transform(y.values.reshape(-1, 1)).ravel()
                    model.fit(X_scaled, y_scaled)
                    # Store scaler for prediction
                    self.models[f'{name}_y_scaler'] = y_scaler
                else:
                    model.fit(X_scaled, y)
            
            # Calculate feature importance for tree-based models
            self._calculate_feature_importance()
            
            self.is_trained = True
            logger.info("Model training completed successfully")
            return True
            
        except Exception as e:
            logger.error("Error training models: %s", e)
            return False
    
    def _calculate_feature_importance(self):
        """Calculate feature importance from tree-based models."""
        try:
            tree_models = ['random_forest', 'gradient_boosting', 'extra_trees']
            importance_scores = {}
            
            for model_name in tree_models:
                if model_name in self.models:
                    importance = self.models[model_name].feature_importances_
                    for i, feature in enumerate(self.feature_columns):
                        if feature not in importance_scores:
                            importance_scores[feature] = []
                        importance_scores[feature].append(importance[i])
            
            # Average importance across models
            self.feature_importance = {
                feature: np.mean(scores) 
                for feature, scores in importance_scores.items()
            }
            
            # Sort by importance
            self.feature_importance = dict(
                sorted(self.feature_importance.items(), key=lambda x: x[1], reverse=True)
            )
            
        except Exception as e:
            logger.error("Error calculating feature importance: %s", e)
    
    def predict_ensemble(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Make ensemble predictions using multiple models.
        
        Args:
            data (pd.DataFrame): Current stock data
            
        Returns:
            Dict[str, Any]: Prediction results with confidence metrics
        """
        try:
            if not self.is_trained:
                raise ValueError("Models not trained. Call train_models() first.")
            
            # Prepare features
            features_df = self.create_advanced_features(data)
            if features_df is None or len(features_df) == 0:
                raise ValueError("Failed to create features")
            
            # Get latest features
            latest_features = features_df[self.feature_columns].iloc[-1:].values
            latest_features_scaled = self.scaler.transform(latest_features)
            
            # Get predictions from all models
            predictions = {}
            weights = {}
            
            for name, model in self.models.items():
                if name.endswith('_y_scaler'):
                    continue
                    
                try:
                    if name == 'neural_network':
                        pred_scaled = model.predict(latest_features_scaled)
                        y_scaler = self.models[f'{name}_y_scaler']
                        pred = y_scaler.inverse_transform(pred_scaled.reshape(-1, 1))[0, 0]
                    else:
                        pred = model.predict(latest_features_scaled)[0]
                    
                    predictions[name] = pred
                    weights[name] = self.model_scores.get(name, 0.5)
                    
                except Exception as e:
                    logger.warning(f"Error with {name} prediction: {e}")
                    continue
            
            if not predictions:
                raise ValueError("No successful predictions from any model")
            
            # Calculate weighted ensemble prediction
            total_weight = sum(weights.values())
            ensemble_pred = sum(pred * weights[name] for name, pred in predictions.items()) / total_weight
            
            # Calculate prediction confidence
            pred_values = list(predictions.values())
            prediction_std = np.std(pred_values)
            prediction_range = max(pred_values) - min(pred_values)
            
            # Confidence based on model agreement and performance
            confidence_score = 1 / (1 + prediction_std / ensemble_pred) * np.mean(list(weights.values()))
            
            if confidence_score > 0.8:
                confidence = "High"
            elif confidence_score > 0.6:
                confidence = "Medium"
            else:
                confidence = "Low"
            
            current_price = data['Close'].iloc[-1]
            price_change = ensemble_pred - current_price
            price_change_pct = (price_change / current_price) * 100
            
            return {
                'predicted_price': float(ensemble_pred),
                'current_price': float(current_price),
                'price_change': float(price_change),
                'price_change_pct': float(price_change_pct),
                'model_confidence': confidence,
                'confidence_score': float(confidence_score),
                'individual_predictions': predictions,
                'model_weights': weights,
                'prediction_std': float(prediction_std),
                'prediction_range': float(prediction_range),
                'prediction_date': datetime.now().isoformat(),
                'symbol': self.symbol
            }
            
        except Exception as e:
            logger.error("Error making prediction: %s", e)
            return None
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the trained models."""
        if not self.is_trained:
            return {"error": "Models not trained"}
        
        return {
            'is_trained': self.is_trained,
            'models': list(self.models.keys()),
            'feature_count': len(self.feature_columns),
            'model_scores': self.model_scores,
            'top_features': dict(list(self.feature_importance.items())[:10]) if self.feature_importance else {},
            'symbol': self.symbol
        }
    
    def train_and_predict(self, period: str = "3y") -> Optional[Dict[str, Any]]:
        """
        Complete workflow: fetch data, train models, and make prediction.
        
        Args:
            period (str): Data period for training
            
        Returns:
            Dict[str, Any]: Prediction results or None if error
        """
        try:
            # Fetch data
            data = self.fetch_stock_data(period)
            if data is None:
                return None
            
            # Create features and train
            features_df = self.create_advanced_features(data)
            if features_df is None:
                return None
            
            # Train models
            if not self.train_models(features_df):
                return None
            
            # Make prediction
            prediction = self.predict_ensemble(data)
            return prediction
            
        except Exception as e:
            logger.error("Error in train_and_predict: %s", e)
            return None
