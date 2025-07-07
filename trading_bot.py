import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time

# Strategy settings
symbol = 'RELIANCE.NS'
starting_cash = 100000
quantity = 10

# Portfolio state
portfolio = {
    "cash": starting_cash,
    "holdings": 0,
    "avg_buy_price": 0,
    "history": []
}

def buy_stock(price, time_stamp):
    global portfolio
    total_cost = quantity * price
    if portfolio["cash"] >= total_cost:
        prev_qty = portfolio["holdings"]
        prev_cost = portfolio["avg_buy_price"] * prev_qty

        portfolio["cash"] -= total_cost
        portfolio["holdings"] += quantity
        portfolio["avg_buy_price"] = (prev_cost + total_cost) / portfolio["holdings"]

        portfolio["history"].append({
            "type": "BUY",
            "qty": quantity,
            "price": price,
            "time": time_stamp
        })
        print(f"✅ Bought {quantity} at ₹{price:.2f}")
    else:
        print("❌ Not enough cash")

def sell_stock(price, time_stamp):
    global portfolio
    if portfolio["holdings"] >= quantity:
        portfolio["cash"] += quantity * price
        portfolio["holdings"] -= quantity
        if portfolio["holdings"] == 0:
            portfolio["avg_buy_price"] = 0

        portfolio["history"].append({
            "type": "SELL",
            "qty": quantity,
            "price": price,
            "time": time_stamp
        })
        print(f"✅ Sold {quantity} at ₹{price:.2f}")
    else:
        print("❌ Not enough shares to sell")

# -----------------------------------
# 📈 Historical backtest on 5 days
# -----------------------------------
print("🔍 Running historical backtest...")

data = yf.download(symbol, period="5d", interval="1m")
data.dropna(inplace=True)
data["SMA20"] = data["Close"].rolling(window=20).mean()

for idx in range(20, len(data)):
    price = data["Close"].iloc[idx].item()
    sma20 = data["SMA20"].iloc[idx].item()
    time_stamp = data.index[idx]

    if np.isnan(sma20):
        continue

    buy_threshold = sma20 * 0.99
    sell_threshold = sma20 * 1.01

    if price < buy_threshold:
        buy_stock(price, time_stamp)
    elif portfolio["holdings"] > 0 and (price >= sell_threshold or price >= portfolio["avg_buy_price"] + 5):
        sell_stock(price, time_stamp)

# Log initial backtest
history_df = pd.DataFrame(portfolio["history"])
history_df.to_csv("trade_log.csv", index=False)
print("\n📊 Portfolio after backtest:")
print(f"Cash: ₹{portfolio['cash']:.2f}")
print(f"Holdings: {portfolio['holdings']} shares at avg ₹{portfolio['avg_buy_price']:.2f}")

# Plot initial strategy
plt.figure(figsize=(12,6))
plt.plot(data.index, data["Close"], label="Price")
plt.plot(data.index, data["SMA20"], label="SMA20", linestyle="--")

for trade in portfolio["history"]:
    if trade["type"] == "BUY":
        plt.scatter(trade["time"], trade["price"], color="green", marker="^", s=100, label="Buy")
    else:
        plt.scatter(trade["time"], trade["price"], color="red", marker="v", s=100, label="Sell")

plt.title(f"Trading Strategy on {symbol}")
plt.xlabel("Time")
plt.ylabel("Price (₹)")
plt.legend(["Price", "SMA20", "Buy", "Sell"])
plt.tight_layout()
plt.savefig("trade_chart.png")
print("📈 Initial strategy chart saved to trade_chart.png")

# -----------------------------------
# 🔄 Keep running live
# -----------------------------------
print("\n🚀 Starting live trading. Press Ctrl+C to stop.")
try:
    while True:
        new_data = yf.download(symbol, period="2d", interval="1m")
        new_data.dropna(inplace=True)
        new_data["SMA20"] = new_data["Close"].rolling(window=20).mean()

        last_row = new_data.iloc[-1]
        price = last_row["Close"].item()
        sma20 = last_row["SMA20"].item()
        time_stamp = last_row.name

        if np.isnan(sma20):
            print(f"⏳ {time_stamp} SMA not ready yet.")
        else:
            buy_threshold = sma20 * 0.99
            sell_threshold = sma20 * 1.01

            if price < buy_threshold:
                buy_stock(price, time_stamp)
            elif portfolio["holdings"] > 0 and (price >= sell_threshold or price >= portfolio["avg_buy_price"] + 5):
                sell_stock(price, time_stamp)
            else:
                print(f"📈 {time_stamp} No trade. Price: ₹{price:.2f}, SMA20: ₹{sma20:.2f}")

        # Save to CSV after each loop
        history_df = pd.DataFrame(portfolio["history"])
        history_df.to_csv("trade_log.csv", index=False)

        time.sleep(60)  # wait for next minute

except KeyboardInterrupt:
    print("\n🛑 Trading stopped by user.")
    print("\n📊 Final Portfolio:")
    print(f"Cash: ₹{portfolio['cash']:.2f}")
    print(f"Holdings: {portfolio['holdings']} shares at avg ₹{portfolio['avg_buy_price']:.2f}")
    print("📄 Final trade history saved to trade_log.csv")
