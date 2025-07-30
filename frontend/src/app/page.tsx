'use client';

import React, { useState, useEffect } from 'react';
import { apiService, StockInfo, HistoricalDataResponse, AdvancedPredictionResponse } from '@/lib/api';
import StockSearch from '@/components/StockSearch';
import StockCard from '@/components/StockCard';
import StockChart from '@/components/StockChart';
import PredictionCard from '@/components/PredictionCard';
import { Activity, AlertCircle, CheckCircle, TrendingUp } from 'lucide-react';

export default function Dashboard() {
  const [currentSymbol, setCurrentSymbol] = useState<string>('AAPL');
  const [stockInfo, setStockInfo] = useState<StockInfo | null>(null);
  const [historicalData, setHistoricalData] = useState<HistoricalDataResponse | null>(null);
  const [prediction, setPrediction] = useState<AdvancedPredictionResponse | null>(null);
  const [apiStatus, setApiStatus] = useState<'checking' | 'online' | 'offline'>('checking');
  
  const [loadingStates, setLoadingStates] = useState({
    stockInfo: false,
    historicalData: false,
    prediction: false,
  });

  const [errors, setErrors] = useState({
    stockInfo: '',
    historicalData: '',
    prediction: '',
  });

  // Check API health on component mount
  useEffect(() => {
    checkApiHealth();
  }, []);

  // Load data when symbol changes
  useEffect(() => {
    if (currentSymbol && apiStatus === 'online') {
      loadStockData(currentSymbol);
    }
  }, [currentSymbol, apiStatus]);

  const checkApiHealth = async () => {
    try {
      await apiService.getHealth();
      setApiStatus('online');
    } catch (error) {
      console.error('API health check failed:', error);
      setApiStatus('offline');
    }
  };

  const loadStockData = async (symbol: string) => {
    // Reset previous data and errors
    setStockInfo(null);
    setHistoricalData(null);
    setPrediction(null);
    setErrors({ stockInfo: '', historicalData: '', prediction: '' });

    // Load stock info
    setLoadingStates(prev => ({ ...prev, stockInfo: true }));
    try {
      const info = await apiService.getStockInfo(symbol);
      setStockInfo(info);
    } catch (error) {
      console.error('Error loading stock info:', error);
      setErrors(prev => ({ 
        ...prev, 
        stockInfo: error instanceof Error ? error.message : 'Failed to load stock information' 
      }));
    } finally {
      setLoadingStates(prev => ({ ...prev, stockInfo: false }));
    }

    // Load historical data
    setLoadingStates(prev => ({ ...prev, historicalData: true }));
    try {
      const historical = await apiService.getHistoricalData(symbol, '1y');
      setHistoricalData(historical);
    } catch (error) {
      console.error('Error loading historical data:', error);
      setErrors(prev => ({ 
        ...prev, 
        historicalData: error instanceof Error ? error.message : 'Failed to load historical data' 
      }));
    } finally {
      setLoadingStates(prev => ({ ...prev, historicalData: false }));
    }

    // Load advanced prediction with fallback
    setLoadingStates(prev => ({ ...prev, prediction: true }));
    try {
      const pred = await apiService.getAdvancedPrediction(symbol, '1y'); // Use smaller dataset
      setPrediction(pred);
    } catch (error) {
      console.error('Error loading advanced prediction, trying basic prediction:', error);
      // Fallback to basic prediction
      try {
        const basicPred = await apiService.getPrediction(symbol, 1);
        // Convert basic prediction to advanced format
        const enhancedPred = {
          ...basicPred,
          price_change: basicPred.predicted_price - basicPred.current_price,
          confidence_score: basicPred.model_confidence === 'High' ? 0.9 : 
                           basicPred.model_confidence === 'Medium' ? 0.7 : 0.5,
          individual_predictions: { 'basic_model': basicPred.predicted_price },
          model_weights: { 'basic_model': 1.0 },
          prediction_std: 0,
          prediction_range: 0
        };
        setPrediction(enhancedPred);
      } catch (fallbackError) {
        console.error('Both advanced and basic prediction failed:', fallbackError);
        setErrors(prev => ({ 
          ...prev, 
          prediction: fallbackError instanceof Error ? fallbackError.message : 'Failed to generate prediction' 
        }));
      }
    } finally {
      setLoadingStates(prev => ({ ...prev, prediction: false }));
    }
  };

  const handleSearch = (symbol: string) => {
    setCurrentSymbol(symbol);
  };

  const ErrorDisplay = ({ error, title }: { error: string; title: string }) => (
    <div className="bg-white rounded-lg shadow-lg p-6 border border-red-200">
      <div className="flex items-center space-x-3 mb-2">
        <AlertCircle className="h-5 w-5 text-red-500" />
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
      </div>
      <p className="text-red-600 text-sm">{error}</p>
      <button
        onClick={() => loadStockData(currentSymbol)}
        className="mt-3 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
      >
        Retry
      </button>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <TrendingUp className="h-6 w-6 text-blue-600" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">Stock Advisor</h1>
                <p className="text-sm text-gray-500">AI-Powered Stock Analysis & Prediction</p>
              </div>
            </div>
            
            {/* API Status */}
            <div className="flex items-center space-x-2">
              {apiStatus === 'checking' && (
                <>
                  <Activity className="h-4 w-4 text-yellow-500 animate-spin" />
                  <span className="text-sm text-yellow-600">Checking API...</span>
                </>
              )}
              {apiStatus === 'online' && (
                <>
                  <CheckCircle className="h-4 w-4 text-green-500" />
                  <span className="text-sm text-green-600">API Online</span>
                </>
              )}
              {apiStatus === 'offline' && (
                <>
                  <AlertCircle className="h-4 w-4 text-red-500" />
                  <span className="text-sm text-red-600">API Offline</span>
                  <button
                    onClick={checkApiHealth}
                    className="ml-2 px-2 py-1 text-xs bg-red-100 text-red-700 rounded hover:bg-red-200"
                  >
                    Retry
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {apiStatus === 'offline' ? (
          <div className="text-center py-12">
            <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-gray-900 mb-2">API Unavailable</h2>
            <p className="text-gray-600 mb-4">
              Unable to connect to the Stock Advisor API. Please ensure the backend server is running.
            </p>
            <button
              onClick={checkApiHealth}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Check Again
            </button>
          </div>
        ) : (
          <div className="space-y-8">
            {/* Search Section */}
            <StockSearch 
              onSearch={handleSearch}
              isLoading={Object.values(loadingStates).some(Boolean)}
              currentSymbol={currentSymbol}
            />

            {/* Main Dashboard Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Left Column - Stock Info & Prediction */}
              <div className="space-y-6">
                {/* Stock Info Card */}
                {errors.stockInfo ? (
                  <ErrorDisplay error={errors.stockInfo} title="Stock Information" />
                ) : (
                  <StockCard 
                    stockInfo={stockInfo!} 
                    isLoading={loadingStates.stockInfo} 
                  />
                )}

                {/* Prediction Card */}
                {errors.prediction ? (
                  <ErrorDisplay error={errors.prediction} title="Price Prediction" />
                ) : (
                  <PredictionCard 
                    prediction={prediction!} 
                    isLoading={loadingStates.prediction}
                    symbol={currentSymbol}
                  />
                )}
              </div>

              {/* Right Column - Chart */}
              <div className="lg:col-span-2">
                {errors.historicalData ? (
                  <ErrorDisplay error={errors.historicalData} title="Price Chart" />
                ) : (
                  <StockChart 
                    data={historicalData?.data || []} 
                    symbol={currentSymbol}
                    isLoading={loadingStates.historicalData}
                  />
                )}
              </div>
            </div>

            {/* Additional Info Section */}
            {stockInfo && !loadingStates.stockInfo && (
              <div className="bg-white rounded-lg shadow-lg p-6 border">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Market Summary</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
                  <div className="p-4 bg-blue-50 rounded-lg">
                    <p className="text-sm text-gray-600">Previous Close</p>
                    <p className="text-xl font-bold text-gray-900">
                      ${stockInfo.previous_close.toFixed(2)}
                    </p>
                  </div>
                  <div className="p-4 bg-green-50 rounded-lg">
                    <p className="text-sm text-gray-600">Daily Volume</p>
                    <p className="text-xl font-bold text-gray-900">
                      {stockInfo.volume.toLocaleString()}
                    </p>
                  </div>
                  <div className="p-4 bg-purple-50 rounded-lg">
                    <p className="text-sm text-gray-600">Market Cap</p>
                    <p className="text-xl font-bold text-gray-900">
                      {stockInfo.market_cap 
                        ? `$${(stockInfo.market_cap / 1e9).toFixed(1)}B` 
                        : 'N/A'
                      }
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-sm text-gray-500">
            <p>
              Stock Advisor Dashboard • Powered by FastAPI & Machine Learning
            </p>
            <p className="mt-1">
              Data provided by Yahoo Finance • Predictions are for educational purposes only
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
