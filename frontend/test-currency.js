// Test currency formatting for different symbols
const { formatCurrency, getCurrencyFromSymbol, getExchangeName } = require('./src/lib/currency.ts');

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
