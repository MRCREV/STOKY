# Stock Advisor Frontend

A modern React/Next.js dashboard for the Stock Advisor API, featuring real-time stock data, interactive charts, and AI-powered price predictions.

## Features

- 🔍 **Stock Search** - Search and analyze any stock symbol
- 📊 **Interactive Charts** - Beautiful price charts with historical data
- 🤖 **AI Predictions** - Machine learning-based price predictions
- 📱 **Responsive Design** - Works perfectly on desktop and mobile
- ⚡ **Real-time Data** - Live stock information from Yahoo Finance
- 🎨 **Modern UI** - Clean, professional interface with Tailwind CSS

## Tech Stack

- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework
- **Recharts** - Interactive chart library
- **Lucide React** - Beautiful icon set
- **Radix UI** - Accessible UI components

## Getting Started

### Prerequisites

- Node.js 18+ installed
- Stock Advisor API running on http://localhost:8000

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open http://localhost:3000 in your browser

### Environment Variables

Create a `.env.local` file in the frontend directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## API Integration

The frontend connects to the Stock Advisor FastAPI backend and provides a beautiful, responsive interface for stock analysis and predictions.
