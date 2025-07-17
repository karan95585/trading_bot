# app.py
from flask import Flask, jsonify
import os
import threading

# import the start() from your trading module
from trading_bot import start as start_trader

app = Flask(__name__)

# Launch the trading loop in background
threading.Thread(target=start_trader, daemon=True).start()

@app.route("/healthz")
def healthz():
    return jsonify(status="ok")

# Optional: expose an endpoint to query current P&L, etc.
# @app.route("/status")
# def status():
#     return jsonify(...)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # bind to 0.0.0.0 so Render can see the port
    app.run(host="0.0.0.0", port=port)
