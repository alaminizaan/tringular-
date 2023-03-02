import ccxt
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    # Get page number from request
    page = request.args.get('page', 1, type=int)

    # Set number of results per page
    per_page = 5

    # Create a list of all exchanges supporting EOS
    eos_exchanges = []
    for exchange_id in ccxt.exchanges:
        try:
            exchange = getattr(ccxt, exchange_id)()
            if 'EOS/USDT' in exchange.load_markets():
                eos_exchanges.append(exchange_id)
        except:
            pass

    # Get the EOS/USDT ticker from each exchange for the current page
    eos_prices = []
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    for exchange_id in eos_exchanges[start_index:end_index]:
        try:
            exchange = getattr(ccxt, exchange_id)()
            ticker = exchange.fetch_ticker('EOS/USDT')
            eos_price = {
                'exchange': exchange_id,
                'price': ticker['last']
            }
            eos_prices.append(eos_price)
        except:
            pass

    # Render the template with the EOS prices and pagination
    return render_template('eos_prices.html', eos_prices=eos_prices, page=page, per_page=per_page, total=len(eos_exchanges))

if __name__ == '__main__':
    app.run(debug=True)
