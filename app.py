import ccxt
from flask import Flask, render_template

app = Flask(__name__)

exchanges = ['binance', 'kraken', 'bithumb', 'hitbtc', 'poloniex', 'coinbase', 'kucoin']

@app.route('/')
def index():
    # Get the EOS/USDT ticker from each exchange
    eos_prices = []
    for exchange_id in exchanges:
        try:
            exchange = getattr(ccxt, exchange_id)()
            if 'eos' in exchange.load_markets():
                ticker = exchange.fetch_ticker('EOS/USDT')
                eos_price = {
                    'exchange': exchange_id,
                    'price': ticker['last']
                }
                eos_prices.append(eos_price)
        except:
            pass

    # Render the template with the EOS prices
    return render_template('eos_prices.html', eos_prices=eos_prices)

if __name__ == '__main__':
    app.run(debug=True)
