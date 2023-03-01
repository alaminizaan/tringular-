import ccxt
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def scan_triangular_arbitrage():
    exchanges = ["binance", "bitfinex", "bittrex", "coinbasepro", "ftx", "huobipro", "kraken", "kucoin", "okex", "poloniex"]
    symbols = ["EOS/USDT", "USDT/EOS", "EOS/BTC", "BTC/EOS", "USDT/BTC", "BTC/USDT"]
    triangular_arbitrages = []
    for i in range(len(exchanges)):
        for j in range(len(exchanges)):
            for k in range(len(exchanges)):
                if i != j and i != k and j != k:
                    exchange1 = getattr(ccxt, exchanges[i])()
                    exchange2 = getattr(ccxt, exchanges[j])()
                    exchange3 = getattr(ccxt, exchanges[k])()
                    try:
                        for symbol in symbols:
                            orderbook1 = exchange1.fetch_order_book(symbol)
                            orderbook2 = exchange2.fetch_order_book(symbol)
                            orderbook3 = exchange3.fetch_order_book(symbol)
                            price1 = orderbook1['bids'][0][0]
                            price2 = orderbook2['asks'][0][0]
                            price3 = orderbook3['bids'][0][0]
                            if price1 > (price2 * price3):
                                profit = (price1 / (price2 * price3)) - 1
                                fees = exchange1.fees['trading']['maker'] + exchange2.fees['trading']['taker'] + exchange3.fees['trading']['maker']
                                if profit > fees:
                                    triangular_arbitrages.append((exchanges[i], exchanges[j], exchanges[k], symbol, profit))
                    except Exception as e:
                        print(e)
    return render_template("triangular_arbitrage.html", triangular_arbitrages=triangular_arbitrages)

if __name__ == "__main__":
    app.run()
