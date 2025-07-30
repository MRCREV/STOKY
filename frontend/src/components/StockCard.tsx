'use client';

import React from 'react';
import { StockInfo } from '@/lib/api';
import { formatLargeNumber, getChangeBgColor } from '@/lib/utils';
import { formatCurrency, formatPercent, getChangeColor, getExchangeName, getCurrencyFromSymbol } from '@/lib/currency';
import { TrendingUp, TrendingDown, Minus, DollarSign, BarChart3, Users } from 'lucide-react';

interface StockCardProps {
  stockInfo: StockInfo | null;
  isLoading?: boolean;
}

export default function StockCard({ stockInfo, isLoading = false }: StockCardProps) {
  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6 border animate-pulse">
        <div className="flex justify-between items-start mb-4">
          <div>
            <div className="h-6 bg-gray-200 rounded w-20 mb-2"></div>
            <div className="h-4 bg-gray-200 rounded w-32"></div>
          </div>
          <div className="h-8 w-8 bg-gray-200 rounded"></div>
        </div>
        <div className="space-y-3">
          <div className="h-8 bg-gray-200 rounded w-24"></div>
          <div className="h-6 bg-gray-200 rounded w-20"></div>
        </div>
      </div>
    );
  }

  // Add null check for stockInfo
  if (!stockInfo) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6 border">
        <div className="text-center py-8">
          <p className="text-gray-500">No stock data available</p>
        </div>
      </div>
    );
  }

  const changeIcon = stockInfo.change > 0 ? TrendingUp : stockInfo.change < 0 ? TrendingDown : Minus;
  const ChangeIcon = changeIcon;
  
  // Get exchange name for this stock (use backend data if available, otherwise detect from symbol)
  const exchangeName = stockInfo.exchange || getExchangeName(stockInfo.symbol);
  
  // Custom currency formatter using the symbol (use backend currency if available)
  const formatPrice = (price: number) => {
    return formatCurrency(price, stockInfo.symbol);
  };

  return (
    <div className={`bg-white rounded-lg shadow-lg p-6 border transition-all duration-200 hover:shadow-xl ${getChangeBgColor(stockInfo.change)}`}>
      {/* Header */}
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-bold text-gray-900">{stockInfo.symbol}</h3>
          <p className="text-sm text-gray-600 truncate max-w-48">{stockInfo.name}</p>
          <p className="text-xs text-gray-500">{exchangeName}</p>
        </div>
        <div className={`p-2 rounded-full ${stockInfo.change >= 0 ? 'bg-green-100' : 'bg-red-100'}`}>
          <ChangeIcon className={`h-5 w-5 ${getChangeColor(stockInfo.change)}`} />
        </div>
      </div>

      {/* Price Information */}
      <div className="space-y-3">
        <div>
          <div className="flex items-baseline space-x-2">
            <p className="text-2xl font-bold text-gray-900">
              {formatPrice(stockInfo.current_price)}
            </p>
            <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
              {stockInfo.currency || getCurrencyFromSymbol(stockInfo.symbol).code}
            </span>
          </div>
          <div className="flex items-center space-x-2 text-sm">
            <span className={`font-medium ${getChangeColor(stockInfo.change)}`}>
              {stockInfo.change >= 0 ? '+' : ''}{formatPrice(stockInfo.change)}
            </span>
            <span className={`font-medium ${getChangeColor(stockInfo.change)}`}>
              ({stockInfo.change_percent >= 0 ? '+' : ''}{formatPercent(stockInfo.change_percent)})
            </span>
          </div>
        </div>

        {/* Additional Metrics */}
        <div className="grid grid-cols-1 gap-3 mt-4">
          <div className="flex items-center justify-between py-2 border-t border-gray-100">
            <div className="flex items-center space-x-2">
              <BarChart3 className="h-4 w-4 text-gray-500" />
              <span className="text-sm text-gray-600">Volume</span>
            </div>
            <span className="text-sm font-medium text-gray-900">
              {formatLargeNumber(stockInfo.volume)}
            </span>
          </div>

          {stockInfo.market_cap && (
            <div className="flex items-center justify-between py-2 border-t border-gray-100">
              <div className="flex items-center space-x-2">
                <DollarSign className="h-4 w-4 text-gray-500" />
                <span className="text-sm text-gray-600">Market Cap</span>
              </div>
              <span className="text-sm font-medium text-gray-900">
                {formatLargeNumber(stockInfo.market_cap)}
              </span>
            </div>
          )}

          {stockInfo.pe_ratio && (
            <div className="flex items-center justify-between py-2 border-t border-gray-100">
              <div className="flex items-center space-x-2">
                <Users className="h-4 w-4 text-gray-500" />
                <span className="text-sm text-gray-600">P/E Ratio</span>
              </div>
              <span className="text-sm font-medium text-gray-900">
                {stockInfo.pe_ratio.toFixed(2)}
              </span>
            </div>
          )}

          {stockInfo.dividend_yield && (
            <div className="flex items-center justify-between py-2 border-t border-gray-100">
              <div className="flex items-center space-x-2">
                <DollarSign className="h-4 w-4 text-gray-500" />
                <span className="text-sm text-gray-600">Dividend Yield</span>
              </div>
              <span className="text-sm font-medium text-gray-900">
                {formatPercent(stockInfo.dividend_yield * 100)}
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
