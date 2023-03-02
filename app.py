import ccxt
from flask import Flask, render_template

app = Flask(__name__)

exchanges_list = ['binance', 'kraken', 'bithumb', 'hitbtc2', 'poloniex', 'coinbasepro', 'kucoin']

@app.route('/')
def index():
    # Get the EOS/USDT ticker from each exchange
    eos_prices = []
    for exchange_id in exchanges_list:
        try:
            exchange = getattr(ccxt, exchange_id)()
            ticker = exchange.fetch_ticker('EOS/USDT')
            eos_price = {
                'exchange': exchange_id,
                'price': ticker['last']
            }
            eos_prices.append(eos_price)
        except Exception as e:
            print(f"Error fetching data from {exchange_id}: {e}")
            pass

    # Render the template with the EOS prices
    return render_template('eos_prices.html', eos_prices=eos_prices)

if __name__ == '__main__':
    app.run(debug=True)
