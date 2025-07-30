'use client';

import React from 'react';
import { XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts';
import { HistoricalData } from '@/lib/api';
import { formatCurrency } from '@/lib/utils';

interface StockChartProps {
  data: HistoricalData[];
  symbol: string;
  isLoading?: boolean;
}

export default function StockChart({ data, symbol, isLoading = false }: StockChartProps) {
  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6 border">
        <div className="h-6 bg-gray-200 rounded w-32 mb-4 animate-pulse"></div>
        <div className="h-64 bg-gray-100 rounded animate-pulse"></div>
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6 border">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Price Chart - {symbol}</h3>
        <div className="h-64 flex items-center justify-center bg-gray-50 rounded">
          <p className="text-gray-500">No chart data available</p>
        </div>
      </div>
    );
  }

  // Format data for the chart
  const chartData = data.map(item => ({
    ...item,
    date: new Date(item.date).toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric' 
    }),
    fullDate: item.date,
  }));

  // Determine if the stock is up or down overall
  const firstPrice = data[0]?.close || 0;
  const lastPrice = data[data.length - 1]?.close || 0;
  const isPositive = lastPrice >= firstPrice;

  const CustomTooltip = ({ active, payload }: { active?: boolean; payload?: Array<{ payload: HistoricalData & { date: string; fullDate: string } }> }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-4 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-medium text-gray-900">{data.fullDate}</p>
          <div className="space-y-1 mt-2">
            <p className="text-sm">
              <span className="text-gray-600">Open: </span>
              <span className="font-medium">{formatCurrency(data.open)}</span>
            </p>
            <p className="text-sm">
              <span className="text-gray-600">High: </span>
              <span className="font-medium">{formatCurrency(data.high)}</span>
            </p>
            <p className="text-sm">
              <span className="text-gray-600">Low: </span>
              <span className="font-medium">{formatCurrency(data.low)}</span>
            </p>
            <p className="text-sm">
              <span className="text-gray-600">Close: </span>
              <span className="font-medium">{formatCurrency(data.close)}</span>
            </p>
            <p className="text-sm">
              <span className="text-gray-600">Volume: </span>
              <span className="font-medium">{data.volume.toLocaleString()}</span>
            </p>
          </div>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 border">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Price Chart - {symbol}</h3>
        <div className="flex items-center space-x-4">
          <div className="text-right">
            <p className="text-sm text-gray-600">Current</p>
            <p className="font-semibold">{formatCurrency(lastPrice)}</p>
          </div>
          <div className={`px-3 py-1 rounded-full text-sm font-medium ${
            isPositive ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
          }`}>
            {isPositive ? '↗' : '↘'} {Math.abs(((lastPrice - firstPrice) / firstPrice) * 100).toFixed(2)}%
          </div>
        </div>
      </div>

      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id={`colorPrice-${symbol}`} x1="0" y1="0" x2="0" y2="1">
                <stop 
                  offset="5%" 
                  stopColor={isPositive ? "#10b981" : "#ef4444"} 
                  stopOpacity={0.3}
                />
                <stop 
                  offset="95%" 
                  stopColor={isPositive ? "#10b981" : "#ef4444"} 
                  stopOpacity={0}
                />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
            <XAxis 
              dataKey="date" 
              stroke="#6b7280"
              fontSize={12}
              tickLine={false}
              axisLine={false}
            />
            <YAxis 
              stroke="#6b7280"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              tickFormatter={(value) => `$${value.toFixed(0)}`}
            />
            <Tooltip content={<CustomTooltip />} />
            <Area
              type="monotone"
              dataKey="close"
              stroke={isPositive ? "#10b981" : "#ef4444"}
              strokeWidth={2}
              fill={`url(#colorPrice-${symbol})`}
              dot={false}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
