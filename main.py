from flask import Flask, request, jsonify
import yfinance as yf
from flask_cors import CORS

app = Flask(__name__)
# Esto permite que tu app de Project IDX pueda leer los datos de este servidor
CORS(app)

@app.route('/prices')
def get_prices():
    tickers_raw = request.args.get('tickers')
    if not tickers_raw:
        return jsonify({"error": "No se enviaron tickers"}), 400
    
    tickers = tickers_raw.split(',')
    
    try:
        # Descargamos los datos de Yahoo Finance
        data = yf.download(tickers, period="1d", interval="1m")['Close']
        
        results = []
        for ticker in tickers:
            try:
                # Si es un solo ticker, 'data' es una serie; si son varios, un DataFrame
                if len(tickers) == 1:
                    price = data.iloc[-1]
                else:
                    price = data[ticker].dropna().iloc[-1]
                
                results.append({
                    "ticker": ticker,
                    "price": round(float(price), 2),
                    "error": False
                })
            except:
                results.append({"ticker": ticker, "price": None, "error": True})
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Render usa el puerto 10000 por defecto
    app.run(host='0.0.0.0', port=10000)