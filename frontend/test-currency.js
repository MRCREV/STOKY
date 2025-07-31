// Test currency formatting for different symbols
// Note: This file tests the currency utilities - run with: node test-currency.js

// Mock the currency utilities for testing since we can't directly import TS
const CURRENCIES = {
  USD: { code: 'USD', symbol: '$', name: 'US Dollar', locale: 'en-US' },
  BRL: { code: 'BRL', symbol: 'R$', name: 'Brazilian Real', locale: 'pt-BR' },
  EUR: { code: 'EUR', symbol: '€', name: 'Euro', locale: 'de-DE' },
  GBP: { code: 'GBP', symbol: '£', name: 'British Pound', locale: 'en-GB' },
  JPY: { code: 'JPY', symbol: '¥', name: 'Japanese Yen', locale: 'ja-JP' },
  CAD: { code: 'CAD', symbol: 'C$', name: 'Canadian Dollar', locale: 'en-CA' },
  AUD: { code: 'AUD', symbol: 'A$', name: 'Australian Dollar', locale: 'en-AU' },
  HKD: { code: 'HKD', symbol: 'HK$', name: 'Hong Kong Dollar', locale: 'en-HK' }
};

const EXCHANGE_MAPPINGS = {
  '.SA': { exchange: 'B3 (São Paulo)', currency: 'BRL' },
  '.AS': { exchange: 'Euronext Amsterdam', currency: 'EUR' },
  '.L': { exchange: 'London Stock Exchange', currency: 'GBP' },
  '.T': { exchange: 'Tokyo Stock Exchange', currency: 'JPY' },
  '.TO': { exchange: 'Toronto Stock Exchange', currency: 'CAD' },
  '.AX': { exchange: 'Australian Securities Exchange', currency: 'AUD' },
  '.HK': { exchange: 'Hong Kong Stock Exchange', currency: 'HKD' }
};

function getCurrencyFromSymbol(symbol) {
  const suffix = Object.keys(EXCHANGE_MAPPINGS).find(s => symbol.endsWith(s));
  const currencyCode = suffix ? EXCHANGE_MAPPINGS[suffix].currency : 'USD';
  return CURRENCIES[currencyCode];
}

function getExchangeName(symbol) {
  const suffix = Object.keys(EXCHANGE_MAPPINGS).find(s => symbol.endsWith(s));
  return suffix ? EXCHANGE_MAPPINGS[suffix].exchange : 'NASDAQ/NYSE';
}

function formatCurrency(amount, symbol) {
  const currency = getCurrencyFromSymbol(symbol);
  return new Intl.NumberFormat(currency.locale, {
    style: 'currency',
    currency: currency.code
  }).format(amount);
}

// Test cases
const testSymbols = [
  'AAPL',      // US Dollar
  'PETR4.SA',  // Brazilian Real
  'ASML.AS',   // Euro
  'TSLA.L',    // British Pound
  '7203.T',    // Japanese Yen
  'SHOP.TO',   // Canadian Dollar
  'CBA.AX',    // Australian Dollar
  '0700.HK',   // Hong Kong Dollar
];

const testPrice = 32.44;

console.log('Currency Formatting Test:');
console.log('========================');

testSymbols.forEach(symbol => {
  const currency = getCurrencyFromSymbol(symbol);
  const exchange = getExchangeName(symbol);
  const formatted = formatCurrency(testPrice, symbol);
  
  console.log(`${symbol.padEnd(10)} | ${exchange.padEnd(25)} | ${currency.code} ${currency.symbol.padEnd(3)} | ${formatted}`);
});

console.log('');
console.log('Special case: PETR4.SA should show R$32.44, not $32.44');
console.log(`PETR4.SA formatted: ${formatCurrency(32.44, 'PETR4.SA')}`);
