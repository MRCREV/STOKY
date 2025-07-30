'use client';

import React, { useState } from 'react';
import { Search, X } from 'lucide-react';

interface StockSearchProps {
  onSearch: (symbol: string) => void;
  isLoading?: boolean;
  currentSymbol?: string;
}

export default function StockSearch({ onSearch, isLoading = false, currentSymbol }: StockSearchProps) {
  const [symbol, setSymbol] = useState(currentSymbol || '');
  const [error, setError] = useState('');

  const popularStocks = [
    'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 
    'META', 'NVDA', 'NFLX', 'SPY', 'QQQ'
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const trimmedSymbol = symbol.trim().toUpperCase();
    
    if (!trimmedSymbol) {
      setError('Please enter a stock symbol');
      return;
    }
    
    if (trimmedSymbol.length > 10) {
      setError('Stock symbol too long (max 10 characters)');
      return;
    }
    
    // Basic validation for stock symbol format
    if (!/^[A-Z0-9.-]+$/.test(trimmedSymbol)) {
      setError('Invalid stock symbol format');
      return;
    }
    
    setError('');
    onSearch(trimmedSymbol);
  };

  const handlePopularStockClick = (stockSymbol: string) => {
    setSymbol(stockSymbol);
    setError('');
    onSearch(stockSymbol);
  };

  const clearSearch = () => {
    setSymbol('');
    setError('');
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 border">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Stock Search</h2>
      
      {/* Search Form */}
      <form onSubmit={handleSubmit} className="mb-4">
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            value={symbol}
            onChange={(e) => {
              setSymbol(e.target.value.toUpperCase());
              if (error) setError('');
            }}
            placeholder="Enter stock symbol (e.g., AAPL, GOOGL)"
            className={`block w-full pl-10 pr-10 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
              error 
                ? 'border-red-300 bg-red-50' 
                : 'border-gray-300 bg-white'
            }`}
            disabled={isLoading}
            maxLength={10}
          />
          {symbol && (
            <button
              type="button"
              onClick={clearSearch}
              className="absolute inset-y-0 right-0 pr-3 flex items-center"
            >
              <X className="h-5 w-5 text-gray-400 hover:text-gray-600" />
            </button>
          )}
        </div>
        
        {error && (
          <p className="mt-2 text-sm text-red-600">{error}</p>
        )}
        
        <button
          type="submit"
          disabled={isLoading || !symbol.trim()}
          className={`mt-3 w-full px-4 py-2 rounded-lg font-medium transition-colors ${
            isLoading || !symbol.trim()
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'
          }`}
        >
          {isLoading ? 'Searching...' : 'Search Stock'}
        </button>
      </form>

      {/* Popular Stocks */}
      <div>
        <h3 className="text-sm font-medium text-gray-700 mb-3">Popular Stocks</h3>
        <div className="flex flex-wrap gap-2">
          {popularStocks.map((stock) => (
            <button
              key={stock}
              onClick={() => handlePopularStockClick(stock)}
              disabled={isLoading}
              className={`px-3 py-1 text-sm font-medium rounded-full border transition-colors ${
                currentSymbol === stock
                  ? 'bg-blue-100 text-blue-800 border-blue-200'
                  : 'bg-gray-50 text-gray-700 border-gray-200 hover:bg-gray-100'
              } ${
                isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:shadow-sm'
              }`}
            >
              {stock}
            </button>
          ))}
        </div>
      </div>

      {/* Current Symbol Display */}
      {currentSymbol && (
        <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
          <p className="text-sm text-blue-800">
            <span className="font-medium">Currently viewing:</span> {currentSymbol}
          </p>
        </div>
      )}
    </div>
  );
}
