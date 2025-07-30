'use client';

import React from 'react';
import { AdvancedPredictionResponse } from '@/lib/api';
import { formatCurrency, formatPercent, getChangeColor } from '@/lib/currency';
import { Brain, TrendingUp, TrendingDown, Calendar, Target } from 'lucide-react';

interface PredictionCardProps {
  prediction: AdvancedPredictionResponse | null;
  isLoading?: boolean;
  symbol?: string; // Add symbol prop to determine currency
}

export default function PredictionCard({ prediction, isLoading = false, symbol }: PredictionCardProps) {
  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6 border animate-pulse">
        <div className="flex items-center space-x-3 mb-4">
          <div className="h-8 w-8 bg-gray-200 rounded-full"></div>
          <div className="h-6 bg-gray-200 rounded w-32"></div>
        </div>
        <div className="space-y-4">
          <div className="h-8 bg-gray-200 rounded w-28"></div>
          <div className="h-6 bg-gray-200 rounded w-24"></div>
          <div className="h-4 bg-gray-200 rounded w-20"></div>
        </div>
      </div>
    );
  }

  if (!prediction) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6 border">
        <div className="flex items-center space-x-3 mb-4">
          <div className="p-2 bg-blue-100 rounded-full">
            <Brain className="h-5 w-5 text-blue-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">AI Prediction</h3>
          </div>
        </div>
        <div className="text-center py-8">
          <p className="text-gray-500">No prediction available</p>
        </div>
      </div>
    );
  }

  const isPositivePrediction = prediction.price_change_pct > 0;
  const PredictionIcon = isPositivePrediction ? TrendingUp : TrendingDown;
  
  // Get the stock symbol from prediction or prop
  const stockSymbol = prediction.symbol || symbol || '';
  
  // Custom currency formatter using the symbol
  const formatPrice = (price: number) => {
    return formatCurrency(price, stockSymbol);
  };

  const getConfidenceColor = (confidence: string) => {
    switch (confidence.toLowerCase()) {
      case 'high':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low':
        return 'bg-red-100 text-red-800 border-red-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 border hover:shadow-xl transition-all duration-200">
      <div className="flex items-center space-x-3 mb-4">
        <div className="p-2 bg-blue-100 rounded-full">
          <Brain className="h-5 w-5 text-blue-600" />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-gray-900">AI Prediction</h3>
          <p className="text-sm text-gray-600">{prediction.symbol}</p>
        </div>
      </div>

      <div className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="text-center p-3 bg-gray-50 rounded-lg">
            <p className="text-sm text-gray-600 mb-1">Current Price</p>
            <p className="text-xl font-bold text-gray-900">
              {formatPrice(prediction.current_price)}
            </p>
          </div>
          <div className="text-center p-3 bg-blue-50 rounded-lg">
            <p className="text-sm text-gray-600 mb-1">Predicted Price</p>
            <p className="text-xl font-bold text-blue-600">
              {formatPrice(prediction.predicted_price)}
            </p>
          </div>
        </div>

        <div className="flex items-center justify-center space-x-3 p-4 bg-gray-50 rounded-lg">
          <PredictionIcon className={`h-6 w-6 ${getChangeColor(prediction.price_change_pct)}`} />
          <div className="text-center">
            <p className="text-sm text-gray-600">Expected Change</p>
            <p className={`text-2xl font-bold ${getChangeColor(prediction.price_change_pct)}`}>
              {prediction.price_change_pct >= 0 ? '+' : ''}{formatPercent(prediction.price_change_pct)}
            </p>
            <p className={`text-sm font-medium ${getChangeColor(prediction.price_change_pct)}`}>
              {prediction.price_change_pct >= 0 ? '+' : ''}
              {formatPrice(prediction.predicted_price - prediction.current_price)}
            </p>
          </div>
        </div>

        <div className="space-y-3 pt-4 border-t border-gray-100">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Calendar className="h-4 w-4 text-gray-500" />
              <span className="text-sm text-gray-600">Prediction Date</span>
            </div>
            <span className="text-sm font-medium text-gray-900">
              {new Date(prediction.prediction_date).toLocaleDateString()}
            </span>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Target className="h-4 w-4 text-gray-500" />
              <span className="text-sm text-gray-600">Model Confidence</span>
            </div>
            <span className={`px-2 py-1 rounded-full text-xs font-medium border ${getConfidenceColor(prediction.model_confidence)}`}>
              {prediction.model_confidence.charAt(0).toUpperCase() + prediction.model_confidence.slice(1)}
            </span>
          </div>
        </div>

        <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
          <p className="text-xs text-yellow-800">
            <strong>Disclaimer:</strong> This prediction is based on historical data and technical indicators. 
            Past performance does not guarantee future results.
          </p>
        </div>
      </div>
    </div>
  );
}
