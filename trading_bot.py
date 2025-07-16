import yfinance as yf
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta, time as dt_time
import pytz
import requests


# -------------------------------
# Configuration
# -------------------------------
india_tz = pytz.timezone('Asia/Kolkata')
starting_cash = 250000
quantity_per_trade = 70
trend_cooldown = 6
volume_lookback = 78
top_n_stocks = 5

symbols = []
holding_symbols=[]
positive_trading= True

# -------------------------------
# Indicator Functions
# -------------------------------
def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    avg_gain = avg_gain.copy()
    avg_loss = avg_loss.copy()

    for i in range(period, len(avg_gain)):
        avg_gain.iloc[i] = (avg_gain.iloc[i - 1] * (period - 1) + gain.iloc[i]) / period
        avg_loss.iloc[i] = (avg_loss.iloc[i - 1] * (period - 1) + loss.iloc[i]) / period

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def calculate_indicators(df):
    df['RSI'] = calculate_rsi(df['Close'])
    df['Volume_MA'] = df['Volume'].rolling(window=volume_lookback).mean()
    return df


def check_rsi_signal(prev_rows, current_row, positive_trading):

    if positive_trading:
        if prev_rows.iloc[4]['RSI'] < 30 and current_row['RSI'] >= 30:
            return 'BUY'

        return None
    else:
        if prev_rows.iloc[4]['RSI'] > 70 and current_row['RSI'] <= 70:
            return 'SELL'

        return None

def check_rsi_signal_for_squar_off(prev_rows, current_row, positive_trading):

    if positive_trading:

        if (prev_rows['RSI'] > 70).any() and current_row['RSI'] <= 70 or current_row['RSI'] > 70:
            return 'SELL'
        return None
    else:
        if (prev_rows['RSI'] <30 ).any() and current_row['RSI'] >= 30 or current_row['RSI'] < 30:
            return 'BUY'
        return None




# -------------------------------
# Live Trading Functions
# -------------------------------
def initialize_portfolio():
    return {
        "cash": starting_cash,
        "holdings": {symbol: 0 for symbol in symbols},
        "positions": {symbol: [] for symbol in symbols},
        "history": [],
        "last_trade": {symbol: datetime.min for symbol in symbols}
    }


def fetch_live_data(symbols):
    end_time = datetime.now(india_tz)
    start_time = end_time - timedelta(minutes=volume_lookback * 2)

    data = yf.download(
        tickers=symbols,
        start=start_time,
        end=end_time,
        interval="1m",
        group_by='ticker',
        auto_adjust=True,
        threads=True
    )

    processed_data = {}
    for symbol in symbols:
        try:
            df = data.xs(symbol, axis=1, level=0).copy()
            df = calculate_indicators(df)
            processed_data[symbol] = df
        except:
            continue
    return processed_data


def execute_trade(portfolio, action, symbol, price, quantity, timestamp, positive_trading):

    if positive_trading == True:
        if action == "BUY":
            portfolio["cash"] -= price * quantity
            if symbol not in portfolio["holdings"]:
                portfolio["holdings"][symbol] = 0

            portfolio["holdings"][symbol] += quantity
            if symbol not in portfolio["positions"]:
                portfolio["positions"][symbol] = []
            portfolio["positions"][symbol].append({
                "price": price,
                "quantity": quantity,
                "time": timestamp
            })
            holding_symbols.append(symbol)
            if symbol not in portfolio["last_trade"]:
                portfolio["last_trade"][symbol] = datetime.min
            portfolio["last_trade"][symbol] = timestamp
            print(f"{timestamp} - BUY {quantity} shares of {symbol} @ ₹{price:.2f}")

        elif action == "SELL":
            portfolio["cash"] += price * quantity
            portfolio["holdings"][symbol] -= quantity

            # Calculate profit from first position
            profit = 0
            if portfolio["positions"][symbol]:
                buy_trade = portfolio["positions"][symbol][0]
                profit = (price - buy_trade["price"]) * quantity
                portfolio["positions"][symbol].pop(0)
            holding_symbols.remove(symbol)
            portfolio["last_trade"][symbol] = timestamp
            reason = "RSI SELL"
            if price >= 1.015 * buy_trade["price"]:
                reason = "Take Profit"
            elif price <= 0.995 * buy_trade["price"]:
                reason = "Stop Loss"

            print(f"{timestamp} - SELL {quantity} shares of {symbol} @ ₹{price:.2f} | Profit: ₹{profit:.2f} | {reason}")

    elif positive_trading == False:
        if action == "SELL":
            portfolio["cash"] -= price * quantity
            if symbol not in portfolio["holdings"]:
                portfolio["holdings"][symbol] = 0

            portfolio["holdings"][symbol] -= quantity
            if symbol not in portfolio["positions"]:
                portfolio["positions"][symbol] = []
            portfolio["positions"][symbol].append({
                "price": price,
                "quantity": quantity,
                "trade_type": "Nagative",
                "time": timestamp
            })
            holding_symbols.append(symbol)
            if symbol not in portfolio["last_trade"]:
                portfolio["last_trade"][symbol] = datetime.min
            portfolio["last_trade"][symbol] = timestamp
            print(f"{timestamp} - SELL {quantity} shares of {symbol} @ ₹{price:.2f}")

        elif action == "BUY":
            portfolio["cash"] += price * quantity
            portfolio["holdings"][symbol] += quantity

            # Calculate profit from first position
            profit = 0
            if portfolio["positions"][symbol]:
                buy_trade = portfolio["positions"][symbol][0]
                profit = ( buy_trade["price"] - price ) * quantity
                portfolio["positions"][symbol].pop(0)
            holding_symbols.remove(symbol)
            portfolio["last_trade"][symbol] = timestamp
            reason = "RSI SELL"
            if price <= 0.990 * buy_trade["price"]:
                reason = "Take Profit"
            elif price >= 1.005 * buy_trade["price"]:
                reason = "Stop Loss"

            print(f"{timestamp} - Buy {quantity} shares of {symbol} @ ₹{price:.2f} | Profit: ₹{profit:.2f} | {reason}")

    portfolio["history"].append({
        "type": action,
        "symbol": symbol,
        "price": price,
        "quantity": quantity,
        "time": timestamp,
        "profit": profit if action == "SELL" else 0
    })


def square_off_positions(portfolio, symbol_data):
    now = datetime.now(india_tz)
    for symbol in symbols:
        if portfolio["holdings"][symbol] > 0:
            price = symbol_data[symbol]['Close'].iloc[-1]
            execute_trade(portfolio, "SELL", symbol, price, portfolio["holdings"][symbol], now)

def sector_data_fetching():
    """Fetch sector performance data from API and map keywords to datasets"""
    try:
        response = requests.get(
            "https://intradayscreener.com/api/indices/sectorData/1",
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            # Create dictionary mapping keywords to datasets
            maped_data= dict(zip(data['keywords'], data['datasets']))
            first_key = next(iter(maped_data))
            first_value = maped_data[first_key]

            last_key = next(reversed(maped_data))
            last_value = maped_data[last_key]
            global positive_trading
            if(first_value>= abs(last_value)):
                positive_trading=True
                response1 = requests.get(
                    url=f"https://intradayscreener.com/api/indices/index-constituents/{first_key}/1?filter=cash",
                timeout=10
                )
                data1=response1.json()
                first_4_stocks = data1["indexConstituents"][:4]
                print(first_4_stocks)
                for stock in first_4_stocks:
                    symbol_name = stock["symbol"] + ".NS"  # append .NS for NSE if using yfinance
                    symbols.append(symbol_name)
            else:
                positive_trading = False
                response2 = requests.get(
                    url=f"https://intradayscreener.com/api/indices/index-constituents/{last_key}/1?filter=fno",
                    timeout=10
                )
                data2=response2.json()
                last_4_stocks = data2["indexConstituents"][-4:]
                print(last_4_stocks)
                for stock in last_4_stocks:
                    symbol_name = stock["symbol"] + ".NS"
                    symbols.append(symbol_name)




        else:
            print(f"⚠️ Sector API Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ Sector API Exception: {e}")
        return None

# -------------------------------
# Main Trading Loop
# -------------------------------
def run_live_trading():
    portfolio = initialize_portfolio()
    print("Starting live paper trading...")
    print(f"Initial Portfolio Value: ₹{starting_cash:,.2f}")

    while True:
        now = datetime.now(india_tz)
        current_time = now.time()

        sector_data_fetching()

        # Check if within market hours (9:15 AM to 3:30 PM IST)
        # if current_time < dt_time(9, 15) or current_time > dt_time(15, 30):
        #     if current_time > dt_time(15, 30):
        #         print("Market closed. Stopping trading.")
        #         continue
        #     next_open = now.replace(hour=9, minute=15, second=0, microsecond=0) + timedelta(days=1)
        #     sleep_seconds = (next_open - now).total_seconds()
        #     print(f"Market closed. Sleeping for {sleep_seconds / 3600:.2f} hours...")
        #     time.sleep(sleep_seconds)
        #     continue

        # Fetch and process data
        try:
            symbol_data = fetch_live_data(symbols)
            symbol_data_for_holdings=fetch_live_data(holding_symbols)
        except Exception as e:
            print(f"Error fetching data: {e}")
            # time.sleep(60)
            # continue

        # Trading logic
        try:
            # 1. Check for exit conditions on existing positions
            holding_any_stock = any(qty > 0 or 0 > qty for qty in portfolio["holdings"].values())
            for symbol in holding_symbols:
                if portfolio["holdings"][symbol] > 0:

                    df = symbol_data_for_holdings[symbol]
                    # Skip if not enough data or in cooldown
                    if len(df) < 7:
                        continue

                    # Get signal from previous completed candle
                    prev_rows = df.iloc[-7:-2]
                    current_row = df.iloc[-2]
                    signal = check_rsi_signal_for_squar_off(prev_rows, current_row,True)
                    current_price = current_row['Close']
                    buy_price = portfolio["positions"][symbol][0]["price"]
                    # Check take profit/stop loss
                    if signal=='SELL' or (current_price <= 0.990 * buy_price or current_price >= 1.005 * buy_price):
                        execute_trade(
                            portfolio, "SELL", symbol,
                            current_price, portfolio["holdings"][symbol], now,True
                        )

                elif portfolio["holdings"][symbol]< 0:
                    df = symbol_data_for_holdings[symbol]
                    # Skip if not enough data or in cooldown
                    if len(df) < 7:
                        continue

                    # Get signal from previous completed candle
                    prev_rows = df.iloc[-7:-2]
                    current_row = df.iloc[-2]
                    signal = check_rsi_signal(prev_rows, current_row, False)
                    current_price = current_row['Close']
                    buy_price = portfolio["positions"][symbol][0]["price"]
                    # Check take profit/stop loss
                    if signal == 'SELL' or (current_price >= 1.015 * buy_price or current_price <= 0.995 * buy_price):
                        execute_trade(
                            portfolio, "SELL", symbol,
                            current_price, portfolio["holdings"][symbol], now
                        )



            # 2. Find top volume stocks
            volume_ranking = []
            for symbol in symbols:
                try:
                    df = symbol_data[symbol]
                    current_vol = df['Volume'].iloc[-2]  # Previous completed candle
                    vol_ma = df['Volume_MA'].iloc[-2]
                    if not np.isnan(vol_ma) and vol_ma > 0:
                        volume_ratio = current_vol / vol_ma
                        volume_ranking.append((symbol, volume_ratio))
                except:
                    continue

            volume_ranking.sort(key=lambda x: x[1], reverse=True)
            top_symbols = [sym for sym, _ in volume_ranking[:top_n_stocks]]

            # 3. Check RSI signals for top symbols
            for symbol in symbols:
                try:
                    df = symbol_data[symbol]
                    # Skip if not enough data or in cooldown
                    if len(df) < 7 :
                        continue

                    # Get signal from previous completed candle
                    prev_rows = df.iloc[-7:-2]
                    current_row = df.iloc[-2]

                    signal = check_rsi_signal(prev_rows, current_row,positive_trading)
                    current_price = current_row['Close']

                    if signal == 'BUY' and not holding_any_stock and current_time <= dt_time(23, 30):
                        max_qty = int((portfolio["cash"]) // current_price)

                        if max_qty > 0:
                            execute_trade(
                                portfolio, "BUY", symbol,
                                current_price, max_qty, now,positive_trading
                            )
                            holding_any_stock = True

                    elif signal == 'SELL' and not holding_any_stock and current_time <= dt_time(23, 30):
                        max_qty = int((portfolio["cash"]) // current_price)
                        if max_qty > 0:
                            execute_trade(
                                portfolio, "SELL", symbol,
                                current_price, max_qty, now, False
                            )
                            holding_any_stock = True
                except Exception as e:
                    print(f"Error processing {symbol}: {e}")

            # 4. Square off positions near market close
            if current_time >= dt_time(15, 25):
                square_off_positions(portfolio, symbol_data)
                print("Squared off all positions before market close")

            # Calculate portfolio value
            holdings_value = 0
            for symbol in symbols:
                holdings_value += symbol_data[symbol]['Close'].iloc[-1] * portfolio["holdings"][symbol]
            portfolio_value = portfolio["cash"] + holdings_value

            print(
                f"{now} | Portfolio Value: ₹{portfolio_value:,.2f} | Cash: ₹{portfolio['cash']:,.2f} | Holdings Value: ₹{holdings_value:,.2f}")

        except Exception as e:
            print(f"Trading error: {e}")

        # Sleep until next minute
        next_run = now + timedelta(minutes=1)
        next_run = next_run.replace(second=0, microsecond=0)
        sleep_seconds = (next_run - datetime.now(india_tz)).total_seconds()
        if sleep_seconds > 0:
            time.sleep(sleep_seconds)


# -------------------------------
# Run Live Trading
# -------------------------------
if __name__ == "__main__":
    run_live_trading()
