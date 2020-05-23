//TradingView Widget function create
function createGraph(symbol){

  new TradingView.widget(
    {
      "autosize": true,
      "symbol": symbol,
      "interval": "D",
      "timezone": "Europe/Istanbul",
      "theme": "light",
      "style": "3",
      "locale": "en",
      "toolbar_bg": "#f1f3f6",
      "enable_publishing": false,
      "allow_symbol_change": true,
      "container_id": "tradingview_0cb0e"
    }
  ); 
}

//If user in stocks page

if (window.location.href.indexOf('stocks') > -1) {
  var input = "AKBNK";
  var symbol = `BIST:${input}`;
  createGraph(symbol);
  $('#stckPgBtn').click(function (e) 
  {
    var input = $('#livestock #selecto').val();
    var symbol = `BIST:${input}`;
    createGraph(symbol);
  });

}

//If user in currencies page
if (window.location.href.indexOf('currencies') > -1) {
  var currency = "USDTRY";
  var symbol = `FX:${currency}`;
  createGraph(symbol);
  $('#stckPgBtn').click(function (e) {
    var currency = $('#livestock #selecto').val();
    var symbol = `FX:${currency}`;
    createGraph(symbol);
  });
}
// If user in cryptos page

if (window.location.href.indexOf('cryptos') > -1) {
  var currency = "BTCUSD";
  var symbol = `BITFINEX:${currency}`;
  createGraph(symbol);
  $('#stckPgBtn').click(function (e) {
    var currency = $('#livestock #selecto').val();
    var symbol = `BITFINEX:${currency}`;
    createGraph(symbol);
  });
}


