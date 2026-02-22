from flask import Flask, request, jsonify
import yfinance as yf
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/prices')
def get_prices():
    tickers_raw = request.args.get('tickers')
    if not tickers_raw:
        return jsonify({"error": "No se enviaron tickers"}), 400
    
    tickers = [t.strip() for t in tickers_raw.split(',')]
    results = []

    try:
        # Usamos la lógica de Colab: 5 días para asegurar datos de cierre
        data = yf.download(tickers, period="5d", interval="1d", group_by='ticker', progress=False)
        
        for ticker in tickers:
            try:
                # Lógica dropna() de Colab para saltar el fin de semana
                if len(tickers) == 1:
                    series = data['Close'].dropna()
                else:
                    series = data[ticker]['Close'].dropna()
                
                if not series.empty:
                    price = series.iloc[-1]
                    results.append({
                        "ticker": ticker,
                        "price": round(float(price), 2),
                        "error": False
                    })
                else:
                    results.append({"ticker": ticker, "price": None, "error": True})
            except:
                results.append({"ticker": ticker, "price": None, "error": True})
        
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
