class Constants {
  // API Configuration
  static const String baseUrl = 'https://stoky.onrender.com'; // Live Render API
  // Previous local URLs:
  // static const String baseUrl = 'http://10.0.2.2:8000'; // Android emulator
  // For real device, use your computer's IP: 'http://192.168.1.XXX:8000'

  static const String appName = 'STOKY';
  static const String appVersion = '1.0.0';
  static const String appDescription = 'AI-Powered Stock Advisor';

  // API Endpoints
  static const String healthEndpoint = '/health';
  static const String stockInfoEndpoint = '/stock/info';
  static const String stockHistoryEndpoint = '/stock/history';
  static const String stockPredictEndpoint = '/stock/predict';
  static const String advancedPredictEndpoint = '/stock/predict-advanced';
  static const String modelInfoEndpoint = '/stock/model-info';
  static const String advancedModelInfoEndpoint = '/stock/advanced-model-info';

  // UI Constants
  static const double borderRadius = 12.0;
  static const double cardElevation = 4.0;
  static const double paddingSmall = 8.0;
  static const double paddingMedium = 16.0;
  static const double paddingLarge = 24.0;

  // Colors
  static const int primaryColorValue = 0xFF2563EB;
  static const int secondaryColorValue = 0xFF10B981;
  static const int errorColorValue = 0xFFEF4444;
  static const int warningColorValue = 0xFFF59E0B;
  static const int successColorValue = 0xFF10B981;

  // Animation Durations
  static const Duration shortAnimation = Duration(milliseconds: 200);
  static const Duration mediumAnimation = Duration(milliseconds: 400);
  static const Duration longAnimation = Duration(milliseconds: 600);

  // Cache Settings
  static const int cacheExpiryHours = 1;
  static const String stockDataCacheKey = 'stock_data_cache';
  static const String predictionCacheKey = 'prediction_cache';

  // Default Values
  static const String defaultCurrency = 'USD';
  static const String defaultExchange = 'NASDAQ/NYSE';
  static const int defaultPredictionDays = 7;
}
