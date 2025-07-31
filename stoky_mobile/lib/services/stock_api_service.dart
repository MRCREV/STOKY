import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/stock_model.dart';

class ApiService {
  // Updated to use live Render API
  static const String baseUrl = 'https://stoky.onrender.com'; // Live API
  // Previous local URLs:
  // static const String baseUrl = 'http://10.105.22.220:8001'; // Local IP
  // static const String baseUrl = 'http://10.0.2.2:8000'; // Android emulator localhost

  static Future<StockModel?> getStockInfo(String symbol) async {
    try {
      print('🌐 Fetching stock info for: $symbol');
      print('🔗 API URL: $baseUrl/stock/info/$symbol');

      final response = await http.get(
        Uri.parse('$baseUrl/stock/info/$symbol'),
        headers: {'Content-Type': 'application/json'},
      ).timeout(const Duration(seconds: 30)); // Increased timeout

      print('📡 HTTP Status: ${response.statusCode}');
      print('📄 Response body: ${response.body}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        print('✅ JSON parsed successfully');
        final stockModel = StockModel.fromJson(data);
        print(
            '✅ StockModel created: ${stockModel.symbol} - ${stockModel.name}');
        return stockModel;
      } else {
        print('❌ Error fetching stock info: ${response.statusCode}');
        print('❌ Error body: ${response.body}');
        return null;
      }
    } catch (e) {
      print('❌ Exception fetching stock info: $e');
      print('❌ Exception type: ${e.runtimeType}');
      if (e.toString().contains('SocketException')) {
        print('🌐 Network connection issue');
      } else if (e.toString().contains('TimeoutException')) {
        print('⏰ Request timed out');
      } else if (e.toString().contains('FormatException')) {
        print('📄 JSON parsing error');
      }
      return null;
    }
  }

  static Future<PredictionModel?> getPrediction(String symbol) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/stock/predict/$symbol'),
        headers: {'Content-Type': 'application/json'},
      ).timeout(const Duration(seconds: 15));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return PredictionModel.fromJson(data);
      } else {
        print('Error fetching prediction: ${response.statusCode}');
        return null;
      }
    } catch (e) {
      print('Error fetching prediction: $e');
      return null;
    }
  }

  static Future<List<String>> searchStocks(String query) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/search?q=$query'),
        headers: {'Content-Type': 'application/json'},
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return List<String>.from(data['results'] ?? []);
      } else {
        print('Error searching stocks: ${response.statusCode}');
        return [];
      }
    } catch (e) {
      print('Error searching stocks: $e');
      return [];
    }
  }

  static Future<Map<String, dynamic>?> getHistoricalData(String symbol,
      {String period = '1mo'}) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/history/$symbol?period=$period'),
        headers: {'Content-Type': 'application/json'},
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        print('Error fetching historical data: ${response.statusCode}');
        return null;
      }
    } catch (e) {
      print('Error fetching historical data: $e');
      return null;
    }
  }
}
