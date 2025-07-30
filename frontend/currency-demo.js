/**
 * Currency Formatting Demonstration
 * This shows how different stock symbols map to their currencies
 */

// Simulate the currency detection logic
function demonstrateCurrencyMapping() {
  const examples = [
    {
      symbol: 'AAPL',
      expected: 'USD ($)',
      exchange: 'NASDAQ/NYSE',
      price: 150.25,
      formatted: '$150.25'
    },
    {
      symbol: 'PETR4.SA',
      expected: 'BRL (R$)',
      exchange: 'B3 (São Paulo)',
      price: 32.44,
      formatted: 'R$32.44'
    },
    {
      symbol: 'ASML.AS',
      expected: 'EUR (€)',
      exchange: 'Euronext Amsterdam',
      price: 650.80,
      formatted: '€650.80'
    },
    {
      symbol: 'VOD.L',
      expected: 'GBP (£)',
      exchange: 'London Stock Exchange',
      price: 75.50,
      formatted: '£75.50'
    },
    {
      symbol: '7203.T',
      expected: 'JPY (¥)',
      exchange: 'Tokyo Stock Exchange',
      price: 2500,
      formatted: '¥2,500'
    },
    {
      symbol: 'SHOP.TO',
      expected: 'CAD (C$)',
      exchange: 'Toronto Stock Exchange',
      price: 85.30,
      formatted: 'C$85.30'
    },
    {
      symbol: '0700.HK',
      expected: 'HKD (HK$)',
      exchange: 'Hong Kong Stock Exchange',
      price: 320.50,
      formatted: 'HK$320.50'
    }
  ];

  console.log('Stock Symbol Currency Mapping:');
  console.log('===============================');
  
  examples.forEach(example => {
    console.log(`${example.symbol.padEnd(12)} | ${example.exchange.padEnd(25)} | ${example.expected.padEnd(12)} | ${example.formatted}`);
  });
  
  console.log('\nKey Features:');
  console.log('- Automatic currency detection based on stock exchange suffix');
  console.log('- Proper locale formatting (e.g., JPY without decimals)');
  console.log('- Exchange name display for context');
  console.log('- Brazilian stocks (.SA) now show R$ instead of $');
}

demonstrateCurrencyMapping();
