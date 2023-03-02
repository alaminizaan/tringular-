import ccxt
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Create a list of all exchanges supporting EOS/USDT
    exchanges = [exchange for exchange in ccxt.exchanges if 'eos' in getattr(ccxt, exchange)().load_markets() and 'usdt' in getattr(ccxt, exchange)().load_markets()['EOS']]

    # Get the EOS/USDT ticker from each exchange
    eos_prices = []
    for exchange_id in exchanges:
        try:
            exchange = getattr(ccxt, exchange_id)()
            ticker = exchange.fetch_ticker('EOS/USDT')
            eos_price = {
                'exchange': exchange_id,
                'price': ticker['last']
            }
            eos_prices.append(eos_price)
        except ccxt.BaseError as e:
            print(f"Error fetching ticker from {exchange_id}: {e}")
            continue

    # Render the template with the EOS prices
    return render_template('eos_prices.html', eos_prices=eos_prices)

if __name__ == '__main__':
    app.run(debug=True)