from SmartApi import SmartConnect #or from SmartApi.smartConnect import SmartConnect
import pyotp
import pandas as pd
import pytz
from datetime import datetime, timedelta, time
import time as time_module  # Rename time module
import requests


symboltoken = [
    {"exchange": "NSE", "tradingsymbol": "LAURUSLABS-EQ", "symboltoken": "19234"},
    {"exchange": "NSE", "tradingsymbol": "CIPLA-EQ", "symboltoken": "694"},
    {"exchange": "NSE", "tradingsymbol": "ZYDUSLIFE-EQ", "symboltoken": "7929"},
    {"exchange": "NSE", "tradingsymbol": "ALKEM-EQ", "symboltoken": "11703"},
    {"exchange": "NSE", "tradingsymbol": "SUNPHARMA-EQ", "symboltoken": "3351"},
    {"exchange": "NSE", "tradingsymbol": "TORNTPHARM-EQ", "symboltoken": "3518"},
    {"exchange": "NSE", "tradingsymbol": "AUROPHARMA-EQ", "symboltoken": "275"},
    {"exchange": "NSE", "tradingsymbol": "LUPIN-EQ", "symboltoken": "10440"},
    {"exchange": "NSE", "tradingsymbol": "GLENMARK-EQ", "symboltoken": "7406"},
    {"exchange": "NSE", "tradingsymbol": "DRREDDY-EQ", "symboltoken": "881"},
    {"exchange": "NSE", "tradingsymbol": "DIVISLAB-EQ", "symboltoken": "10940"},
    {"exchange": "NSE", "tradingsymbol": "GRANULES-EQ", "symboltoken": "11872"},
    {"exchange": "NSE", "tradingsymbol": "BIOCON-EQ", "symboltoken": "11373"},
    {"exchange": "NSE", "tradingsymbol": "MANKIND-EQ", "symboltoken": "15380"},
    {"exchange": "NSE", "tradingsymbol": "DABUR-EQ", "symboltoken": "772"},
    {"exchange": "NSE", "tradingsymbol": "HINDUNILVR-EQ", "symboltoken": "1394"},
    {"exchange": "NSE", "tradingsymbol": "MARICO-EQ", "symboltoken": "4067"},
    {"exchange": "NSE", "tradingsymbol": "BRITANNIA-EQ", "symboltoken": "547"},
    {"exchange": "NSE", "tradingsymbol": "TATACONSUM-EQ", "symboltoken": "3432"},
    {"exchange": "NSE", "tradingsymbol": "ITC-EQ", "symboltoken": "1660"},
    {"exchange": "NSE", "tradingsymbol": "COLPAL-EQ", "symboltoken": "15141"},
    {"exchange": "NSE", "tradingsymbol": "GODREJCP-EQ", "symboltoken": "10099"},
    {"exchange": "NSE", "tradingsymbol": "NESTLEIND-EQ", "symboltoken": "17963"},
    {"exchange": "NSE", "tradingsymbol": "IGL-EQ", "symboltoken": "11262"},
    {"exchange": "NSE", "tradingsymbol": "PETRONET-EQ", "symboltoken": "11351"},
    {"exchange": "NSE", "tradingsymbol": "BPCL-EQ", "symboltoken": "526"},
    {"exchange": "NSE", "tradingsymbol": "RELIANCE-EQ", "symboltoken": "2885"},
    {"exchange": "NSE", "tradingsymbol": "IOC-EQ", "symboltoken": "1624"},
    {"exchange": "NSE", "tradingsymbol": "ATGL-EQ", "symboltoken": "6066"},
    {"exchange": "NSE", "tradingsymbol": "HINDPETRO-EQ", "symboltoken": "1406"},
    {"exchange": "NSE", "tradingsymbol": "MGL-EQ", "symboltoken": "17534"},
    {"exchange": "NSE", "tradingsymbol": "ONGC-EQ", "symboltoken": "2475"},
    {"exchange": "NSE", "tradingsymbol": "GAIL-EQ", "symboltoken": "4717"},
    {"exchange": "NSE", "tradingsymbol": "HEROMOTOCO-EQ", "symboltoken": "1348"},
    {"exchange": "NSE", "tradingsymbol": "MOTHERSON-EQ", "symboltoken": "4204"},
    {"exchange": "NSE", "tradingsymbol": "TVSMOTOR-EQ", "symboltoken": "8479"},
    {"exchange": "NSE", "tradingsymbol": "BAJAJ-AUTO-EQ", "symboltoken": "16669"},
    {"exchange": "NSE", "tradingsymbol": "TATAMOTORS-EQ", "symboltoken": "3456"},
    {"exchange": "NSE", "tradingsymbol": "MARUTI-EQ", "symboltoken": "10999"},
    {"exchange": "NSE", "tradingsymbol": "M&M-EQ", "symboltoken": "2031"},
    {"exchange": "NSE", "tradingsymbol": "BHARATFORG-EQ", "symboltoken": "422"},
    {"exchange": "NSE", "tradingsymbol": "SYNGENE-EQ", "symboltoken": "10243"},
    {"exchange": "NSE", "tradingsymbol": "FORTIS-EQ", "symboltoken": "14592"},
    {"exchange": "NSE", "tradingsymbol": "APOLLOHOSP-EQ", "symboltoken": "157"},
    {"exchange": "NSE", "tradingsymbol": "MAXHEALTH-EQ", "symboltoken": "22377"},
    {"exchange": "NSE", "tradingsymbol": "TATAPOWER-EQ", "symboltoken": "3426"},
    {"exchange": "NSE", "tradingsymbol": "JSWENERGY-EQ", "symboltoken": "17869"},
    {"exchange": "NSE", "tradingsymbol": "POWERGRID-EQ", "symboltoken": "14977"},
    {"exchange": "NSE", "tradingsymbol": "NTPC-EQ", "symboltoken": "11630"},
    {"exchange": "NSE", "tradingsymbol": "COALINDIA-EQ", "symboltoken": "20374"},
    {"exchange": "NSE", "tradingsymbol": "VBL-EQ", "symboltoken": "18921"},
    {"exchange": "NSE", "tradingsymbol": "ASIANPAINT-EQ", "symboltoken": "236"},
    {"exchange": "NSE", "tradingsymbol": "INDHOTEL-EQ", "symboltoken": "1512"},
    {"exchange": "NSE", "tradingsymbol": "TRENT-EQ", "symboltoken": "1964"},
    {"exchange": "NSE", "tradingsymbol": "HAVELLS-EQ", "symboltoken": "9819"},
    {"exchange": "NSE", "tradingsymbol": "DMART-EQ", "symboltoken": "19913"},
    {"exchange": "NSE", "tradingsymbol": "TITAN-EQ", "symboltoken": "3506"},
    {"exchange": "NSE", "tradingsymbol": "BHARTIARTL-EQ", "symboltoken": "10604"},
    {"exchange": "NSE", "tradingsymbol": "NAUKRI-EQ", "symboltoken": "13751"},
    {"exchange": "NSE", "tradingsymbol": "DLF-EQ", "symboltoken": "14732"},
    {"exchange": "NSE", "tradingsymbol": "SHRIRAMFIN-EQ", "symboltoken": "4306"},
    {"exchange": "NSE", "tradingsymbol": "SBILIFE-EQ", "symboltoken": "21808"},
    {"exchange": "NSE", "tradingsymbol": "HDFCAMC-EQ", "symboltoken": "4244"},
    {"exchange": "NSE", "tradingsymbol": "ICICIBANK-EQ", "symboltoken": "4963"},
    {"exchange": "NSE", "tradingsymbol": "HDFCBANK-EQ", "symboltoken": "1333"},
    {"exchange": "NSE", "tradingsymbol": "SBIN-EQ", "symboltoken": "3045"},
    {"exchange": "NSE", "tradingsymbol": "AXISBANK-EQ", "symboltoken": "5900"},
    {"exchange": "NSE", "tradingsymbol": "KOTAKBANK-EQ", "symboltoken": "5900"},
    {"exchange": "NSE", "tradingsymbol": "AMBER-EQ", "symboltoken": "1185"},
    {"exchange": "NSE", "tradingsymbol": "DIXON-EQ", "symboltoken": "21690"},
    {"exchange": "NSE", "tradingsymbol": "IDFCFIRSTB-EQ", "symboltoken": "11184"},
    {"exchange": "NSE", "tradingsymbol": "MPHASIS-EQ", "symboltoken": "4503"},
    {"exchange": "NSE", "tradingsymbol": "COFORGE-EQ", "symboltoken": "11543"},
    {"exchange": "NSE", "tradingsymbol": "INFY-EQ", "symboltoken": "1594"},
    {"exchange": "NSE", "tradingsymbol": "TCS-EQ", "symboltoken": "11536"},
    {"exchange": "NSE", "tradingsymbol": "JSWSTEEL-EQ", "symboltoken": "11723"},
    {"exchange": "NSE", "tradingsymbol": "HINDALCO-EQ", "symboltoken": "1363"},
    {"exchange": "NSE", "tradingsymbol": "TATASTEEL-EQ", "symboltoken": "3499"},
    {"exchange": "NSE", "tradingsymbol": "VEDL-EQ", "symboltoken": "3063"},
    {"exchange": "NSE", "tradingsymbol": "PHOENIXLTD-EQ", "symboltoken": "14552"},
    {"exchange": "NSE", "tradingsymbol": "PRESTIGE-EQ", "symboltoken": "20302"},
    {"exchange": "NSE", "tradingsymbol": "OBEROIRLTY-EQ", "symboltoken": "20242"},
    {"exchange": "NSE", "tradingsymbol": "GODREJPROP-EQ", "symboltoken": "17875"},
    {"exchange": "NSE", "tradingsymbol": "LODHA-EQ", "symboltoken": "3220"},
    {"exchange": "NSE", "tradingsymbol": "SJVN-EQ", "symboltoken": "18883"},
    {"exchange": "NSE", "tradingsymbol": "BHEL-EQ", "symboltoken": "438"},
    {"exchange": "NSE", "tradingsymbol": "ADANIENSOL-EQ", "symboltoken": "10217"},
    {"exchange": "NSE", "tradingsymbol": "ADANIGREEN-EQ", "symboltoken": "3563"},
    {"exchange": "NSE", "tradingsymbol": "INOXWIND-EQ", "symboltoken": "7852"},
    {"exchange": "NSE", "tradingsymbol": "ABB-EQ", "symboltoken": "13"},
    {"exchange": "NSE", "tradingsymbol": "NHPC-EQ", "symboltoken": "17400"},
    {"exchange": "NSE", "tradingsymbol": "SIEMENS-EQ", "symboltoken": "3150"},
    {"exchange": "NSE", "tradingsymbol": "CGPOWER-EQ", "symboltoken": "760"},
    {"exchange": "NSE", "tradingsymbol": "TORNTPOWER-EQ", "symboltoken": "13786"},
    {"exchange": "NSE", "tradingsymbol": "OIL-EQ", "symboltoken": "17438"},
    {"exchange": "NSE", "tradingsymbol": "NHPC-EQ", "symboltoken": "17400"},
{"exchange": "NSE", "tradingsymbol": "HINDZINC-EQ", "symboltoken": "1424"},
    {"exchange": "NSE", "tradingsymbol": "HINDCOPPER-EQ", "symboltoken": "17939"},
    {"exchange": "NSE", "tradingsymbol": "JSL-EQ", "symboltoken": "11236"},
    {"exchange": "NSE", "tradingsymbol": "NMDC-EQ", "symboltoken": "15332"},
    {"exchange": "NSE", "tradingsymbol": "NATIONALUM-EQ", "symboltoken": "6364"},
    {"exchange": "NSE", "tradingsymbol": "ADANIENT-EQ", "symboltoken": "25"},
    {"exchange": "NSE", "tradingsymbol": "JINDALSTEL-EQ", "symboltoken": "6733"},
    {"exchange": "NSE", "tradingsymbol": "APLAPOLLO-EQ", "symboltoken": "25780"},
    {"exchange": "NSE", "tradingsymbol": "SAIL-EQ", "symboltoken": "2963"},
    {"exchange": "NSE", "tradingsymbol": "BOSCHLTD-EQ", "symboltoken": "2181"},
    {"exchange": "NSE", "tradingsymbol": "EXIDEIND-EQ", "symboltoken": "676"},
    {"exchange": "NSE", "tradingsymbol": "TIINDIA-EQ", "symboltoken": "312"},
    {"exchange": "NSE", "tradingsymbol": "BALKRISIND-EQ", "symboltoken": "335"},
    {"exchange": "NSE", "tradingsymbol": "EICHERMOT-EQ", "symboltoken": "910"},
    {"exchange": "NSE", "tradingsymbol": "ASHOKLEY-EQ", "symboltoken": "212"},
    {"exchange": "NSE", "tradingsymbol": "UNITDSPR-EQ", "symboltoken": "10447"},
    {"exchange": "NSE", "tradingsymbol": "INDIGO-EQ", "symboltoken": "11195"},
    {"exchange": "NSE", "tradingsymbol": "ETERNAL-EQ", "symboltoken": "5097"},
    {"exchange": "NSE", "tradingsymbol": "PNB-EQ", "symboltoken": "10666"},
    {"exchange": "NSE", "tradingsymbol": "BANKBARODA-EQ", "symboltoken": "4668"},
    {"exchange": "NSE", "tradingsymbol": "INDIANB-EQ", "symboltoken": "14309"},
    {"exchange": "NSE", "tradingsymbol": "BANKINDIA-EQ", "symboltoken": "4745"},
    {"exchange": "NSE", "tradingsymbol": "CANBK-EQ", "symboltoken": "10794"},
    {"exchange": "NSE", "tradingsymbol": "UNIONBANK-EQ", "symboltoken": "10753"},
    {"exchange": "NSE", "tradingsymbol": "JIOFIN-EQ", "symboltoken": "18143"},
    {"exchange": "NSE", "tradingsymbol": "RECLTD-EQ", "symboltoken": "15355"},
    {"exchange": "NSE", "tradingsymbol": "LICHSGFIN-EQ", "symboltoken": "1997"},
    {"exchange": "NSE", "tradingsymbol": "PFC-EQ", "symboltoken": "14299"},
    {"exchange": "NSE", "tradingsymbol": "BAJFINANCE-EQ", "symboltoken": "317"},
    {"exchange": "NSE", "tradingsymbol": "ICICIPRULI-EQ", "symboltoken": "18652"},
    {"exchange": "NSE", "tradingsymbol": "BAJAJFINSV-EQ", "symboltoken": "16675"},
    {"exchange": "NSE", "tradingsymbol": "CHOLAFIN-EQ", "symboltoken": "685"},
    {"exchange": "NSE", "tradingsymbol": "HDFCLIFE-EQ", "symboltoken": "467"},
    {"exchange": "NSE", "tradingsymbol": "MUTHOOTFIN-EQ", "symboltoken": "23650"},
    {"exchange": "NSE", "tradingsymbol": "SBICARD-EQ", "symboltoken": "17971"},
    {"exchange": "NSE", "tradingsymbol": "ICICIGI-EQ", "symboltoken": "21770"},
    {"exchange": "NSE", "tradingsymbol": "PATANJALI-EQ", "symboltoken": "17029"},
    {"exchange": "NSE", "tradingsymbol": "PGEL-EQ", "symboltoken": "25358"},
    {"exchange": "NSE", "tradingsymbol": "KALYANKJIL-EQ", "symboltoken": "2955"},
    {"exchange": "NSE", "tradingsymbol": "VOLTAS-EQ", "symboltoken": "3718"},
    {"exchange": "NSE", "tradingsymbol": "BLUESTARCO-EQ", "symboltoken": "8311"},
    {"exchange": "NSE", "tradingsymbol": "CROMPTON-EQ", "symboltoken": "17094"},
    {"exchange": "NSE", "tradingsymbol": "AUBANK-EQ", "symboltoken": "21238"},
    {"exchange": "NSE", "tradingsymbol": "INDUSINDBK-EQ", "symboltoken": "5258"},
    {"exchange": "NSE", "tradingsymbol": "FEDERALBNK-EQ", "symboltoken": "1023"},
    {"exchange": "NSE", "tradingsymbol": "RBLBANK-EQ", "symboltoken": "18391"},
    {"exchange": "NSE", "tradingsymbol": "YESBANK-EQ", "symboltoken": "11915"},
    {"exchange": "NSE", "tradingsymbol": "BANDHANBNK-EQ", "symboltoken": "2263"},
    {"exchange": "NSE", "tradingsymbol": "WIPRO-EQ", "symboltoken": "3787"},
    {"exchange": "NSE", "tradingsymbol": "PERSISTENT-EQ", "symboltoken": "18365"},
    {"exchange": "NSE", "tradingsymbol": "HCLTECH-EQ", "symboltoken": "7229"},
    {"exchange": "NSE", "tradingsymbol": "TECHM-EQ", "symboltoken": "13538"},
    {"exchange": "NSE", "tradingsymbol": "OFSS-EQ", "symboltoken": "10738"},
    {"exchange": "NSE", "tradingsymbol": "BRIGADE-EQ", "symboltoken": "15184"},

]

token_map = {entry["tradingsymbol"]: entry["symboltoken"] for entry in symboltoken}

symbols = []  # Final output list
holding_symbols=[]
positive_trading= True

# === YOUR CREDENTIALS ===
API_KEY = "49Azo42v"
CLIENT_CODE = "R63242776"
PASSWORD = "2005"
TOTP_SECRET = "VG2FMTOYFLDFCVNII7KUIGAE7I"

# Initialize SmartConnect
smart_api = SmartConnect(api_key=API_KEY)

# Generate TOTP
totp = pyotp.TOTP(TOTP_SECRET).now()

# Login
try:
    session = smart_api.generateSession(CLIENT_CODE, PASSWORD, totp)
    print("✅ Login successful")
    refresh_token = session['data']['refreshToken']
except Exception as e:
    print("❌ Login failed:", e)
    exit()

# Define Indian timezone
india_tz = pytz.timezone('Asia/Kolkata')

# ======== Strategy Parameters ========
starting_cash = 250000
trend_cooldown = 6  # minutes
volume_lookback = 15
top_n_stocks = 5
quantity_per_trade = 70


# ======== Portfolio State ========
capital = starting_cash
positions = {}
last_trade_time = {}
symbol_data_dict = {}
trade_history = []


# ======== Utility Functions ========
def calculate_rsi(series, period=14):
    print("Candles available for RSI:", len(series))

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
    df['RSI'] = calculate_rsi(df['close'])
    df['Volume_MA'] = df['volume'].rolling(window=volume_lookback).mean()
    return df


def check_rsi_signal(df):
    if len(df) < 6:
        return None

    current_row = df.iloc[-1]
    prev_rows = df.iloc[-6:-1]
    prev_rsi = prev_rows['RSI'].iloc[-1]  # immediate previous RSI

    # Buy signal: RSI crosses above 30
    if positive_trading:
        if prev_rsi >= 30 and current_row['RSI'] <= 60 or current_row['RSI']<=30:
            return 'BUY'
    else:
        # Sell signal: RSI crosses below 70
        if prev_rsi <= 70 and current_row['RSI'] >= 40 or current_row['RSI']>=70:
            return 'SELL'

    return None



def fetch_historical_data(symbol, minutes=15):
    try:
        now = datetime.now(india_tz)
        # now = datetime.now(india_tz).replace(hour=9, minute=20, second=0, microsecond=0)

        today = now.date()

        market_open_time = datetime.combine(today, datetime.min.time()).replace(
            hour=9, minute=15, tzinfo=india_tz)
        market_close_time = datetime.combine(today, datetime.min.time()).replace(
            hour=15, minute=30, tzinfo=india_tz)

        full_df = pd.DataFrame()

        if now < market_open_time:
            # Before market open → use yesterday's full final minutes
            to_date = datetime.combine(today - timedelta(days=1), datetime.min.time()).replace(
                hour=15, minute=30, tzinfo=india_tz)
            from_date = to_date - timedelta(minutes=minutes)

            # Fetch only from yesterday
            historicParam = {
                "exchange": symbol["exchange"],
                "symboltoken": symbol["symboltoken"],
                "interval": "ONE_MINUTE",
                "fromdate": from_date.strftime("%Y-%m-%d %H:%M"),
                "todate": to_date.strftime("%Y-%m-%d %H:%M")
            }

            response = smart_api.getCandleData(historicParam)
            if response['status'] and response['data']:
                full_df = pd.DataFrame(response['data'], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

        elif now < market_open_time + timedelta(minutes=minutes):
            # Market just opened → mix of today + yesterday

            # 1️⃣ Today's data from 9:15 to now
            today_from = market_open_time
            today_to = now
            today_minutes = int((today_to - today_from).total_seconds() / 60)

            if today_minutes > 0:
                historicParam_today = {
                    "exchange": symbol["exchange"],
                    "symboltoken": symbol["symboltoken"],
                    "interval": "ONE_MINUTE",
                    "fromdate": today_from.strftime("%Y-%m-%d %H:%M"),
                    "todate": today_to.strftime("%Y-%m-%d %H:%M")
                }

                response_today = smart_api.getCandleData(historicParam_today)
                if response_today['status'] and response_today['data']:
                    today_df = pd.DataFrame(response_today['data'], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                    full_df = pd.concat([full_df, today_df], ignore_index=True)

            # 2️⃣ Yesterday's data to fill the remaining
            remaining_minutes = minutes - today_minutes
            if remaining_minutes > 0:
                yest_to = datetime.combine(today - timedelta(days=1), datetime.min.time()).replace(
                    hour=15, minute=30, tzinfo=india_tz)
                yest_from = yest_to - timedelta(minutes=remaining_minutes)

                historicParam_yesterday = {
                    "exchange": symbol["exchange"],
                    "symboltoken": symbol["symboltoken"],
                    "interval": "ONE_MINUTE",
                    "fromdate": yest_from.strftime("%Y-%m-%d %H:%M"),
                    "todate": yest_to.strftime("%Y-%m-%d %H:%M")
                }

                response_yest = smart_api.getCandleData(historicParam_yesterday)
                if response_yest['status'] and response_yest['data']:
                    yest_df = pd.DataFrame(response_yest['data'], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                    full_df = pd.concat([yest_df, full_df])
                    full_df = full_df.sort_values(by='timestamp')


        else:
            # Normal hours → fetch last `minutes` from today
            to_date = min(now, market_close_time)
            from_date = to_date - timedelta(minutes=minutes)

            historicParam = {
                "exchange": symbol["exchange"],
                "symboltoken": symbol["symboltoken"],
                "interval": "ONE_MINUTE",
                "fromdate": from_date.strftime("%Y-%m-%d %H:%M"),
                "todate": to_date.strftime("%Y-%m-%d %H:%M")
            }

            response = smart_api.getCandleData(historicParam)
            if response['status'] and response['data']:
                full_df = pd.DataFrame(response['data'], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

        # Final processing
        if not full_df.empty:
            full_df['timestamp'] = pd.to_datetime(full_df['timestamp'], format='ISO8601')
            full_df['timestamp'] = full_df['timestamp'].dt.tz_convert(india_tz)
            return full_df.set_index('timestamp')

    except Exception as e:
        print(f"❌ Error fetching historical data for {symbol['tradingsymbol']}: {e}")

    return pd.DataFrame()


def fetch_ltp(symbol):
    try:
        ltp_data = smart_api.ltpData(
            exchange=symbol["exchange"],
            tradingsymbol=symbol["tradingsymbol"],
            symboltoken=symbol["symboltoken"])
        return ltp_data['data']['ltp']
    except Exception as e:
        print(f"Error fetching LTP for {symbol['tradingsymbol']}: {e}")
        return None


def place_order(symbol, transaction_type, quantity):
    try:
        # order_params = {
        #     "variety": "NORMAL",
        #     "tradingsymbol": symbol["tradingsymbol"],
        #     "symboltoken": symbol["symboltoken"],
        #     "transactiontype": transaction_type,
        #     "exchange": symbol["exchange"],
        #     "ordertype": "MARKET",
        #     "producttype": "INTRADAY",
        #     "duration": "DAY",
        #     "price": "0",
        #     "quantity": quantity
        # }
        # order = smart_api.placeOrder(order_params)
        # return order['message'] == 'SUCCESS' if 'message' in order else False
        if transaction_type=="BUY":
            print("order executed",symbol, transaction_type, quantity)
            holding_symbols.append(symbol)
            return True
        elif transaction_type=="SELL":
            print("order executed", symbol, transaction_type, quantity)
            holding_symbols.append(symbol)
            return True
    except Exception as e:
        print(f"Order placement error: {e}")
        return False

symbols = []

def sector_data_fetching():
    """Fetch sector performance data and map to Angel One symbol objects"""
    global symbols
    symbols=[]
    try:
        response = requests.get(
            "https://intradayscreener.com/api/indices/sectorData/1",
            timeout=10
        )

        if response.status_code != 200:
            print(f"⚠️ Sector API Error: {response.status_code}")
            return

        data = response.json()
        mapped_data = dict(zip(data['keywords'], data['datasets']))
        first_key = next(iter(mapped_data))
        last_key = next(reversed(mapped_data))

        global positive_trading

        # Decide top or bottom sector based on performance
        if mapped_data[first_key] >= abs(mapped_data[last_key]):
            positive_trading = True
            sector_response = requests.get(
                f"https://intradayscreener.com/api/indices/index-constituents/{first_key}/1?filter=fno",
                timeout=10
            )
            stocks = sector_response.json().get("indexConstituents", [])[-4:]
        else:
            positive_trading = False
            sector_response = requests.get(
                f"https://intradayscreener.com/api/indices/index-constituents/{last_key}/1?filter=cash",
                timeout=10
            )
            stocks = sector_response.json().get("indexConstituents", [])[-4:]

        for stock in stocks:
            try:
                name = stock["symbol"].strip().upper()
                tradingsymbol = name + "-EQ"

                print(f"🔍 Looking up token for: {tradingsymbol}")

                token = token_map.get(tradingsymbol)

                if token:
                    symbols.append({
                        "exchange": "NSE",
                        "tradingsymbol": tradingsymbol,
                        "symboltoken": token
                    })
                    print(f"✅ Added: {tradingsymbol}")
                else:
                    print(f"❌ Token not found for {tradingsymbol}")

            except Exception as e:
                print(f"❌ Error processing {stock}: {e}")

    except Exception as e:
        print(f"⚠️ Sector API Exception: {e}")

def run_live_trading():

    # ======== Main Trading Loop ========
    print("\n🚀 Starting RSI Trading Strategy")
    print(f"⏰ Trading Hours: 9:15 AM to 3:30 PM IST")
    print(f"💰 Starting Capital: ₹{starting_cash:,}")

    try:
        while True:
            global capital
            current_time = datetime.now(india_tz)
            current_minute = current_time.replace(second=0, microsecond=0)

            # Skip outside market hours
            # if current_time.time() < time(9, 15) or current_time.time() > time(15, 30):
            #     if current_time.time() > time(15, 30):
            #         print("🛑 Market closed. Stopping strategy")
            #         break
            #     time_module.sleep(30)
            #     continue

            print(f"\n⏱️ {current_time.strftime('%H:%M:%S')} - Processing...")
            sector_data_fetching()

            # Update historical data every minute
     # Update at start of minute
            for symbol in symbols:
                symbol_key = symbol["tradingsymbol"]
                df = fetch_historical_data(symbol, volume_lookback + 14)
                if not df.empty:
                    df = calculate_indicators(df)
                    symbol_data_dict[symbol_key] = df
                    last_close = df['close'].iloc[-1] if len(df) > 0 else 0
                    print(
                        f"📊 {symbol_key}: ₹{last_close:.2f} | RSI: {df['RSI'].iloc[-1]:.1f} | Vol Ratio: {(df['volume'].iloc[-1] / df['Volume_MA'].iloc[-1]):.2f}")
                    time_module.sleep(0.3)

            # Volume-based stock selection
            volume_ranking = []
            for symbol in symbols:
                symbol_key = symbol["tradingsymbol"]
                if symbol_key in symbol_data_dict and not symbol_data_dict[symbol_key].empty:
                    df = symbol_data_dict[symbol_key]
                    if 'Volume_MA' in df.columns and len(df) > volume_lookback:
                        last_row = df.iloc[-1]
                        volume_ratio = last_row['volume'] / last_row['Volume_MA']
                        volume_ranking.append((symbol, volume_ratio, last_row))

            volume_ranking.sort(key=lambda x: x[1], reverse=True)
            top_symbols = volume_ranking[:top_n_stocks]

            # Process top volume symbols
            for symbol_data in top_symbols:
                symbol, volume_ratio, last_row = symbol_data
                symbol_key = symbol["tradingsymbol"]
                df = symbol_data_dict[symbol_key]

                # Check trade cooldown
                last_trade = last_trade_time.get(symbol_key, datetime.min.replace(tzinfo=india_tz))
                if (current_time - last_trade).total_seconds() < trend_cooldown * 60:
                    continue

                # Check RSI signal
                signal = check_rsi_signal(df)
                holding_any = len(positions) > 0

                # BUY signal - Only if no existing positions
                if signal == 'BUY' and not holding_any and current_time.hour <= 20:
                    max_qty =  int(capital // last_row['close'])
                    if max_qty > 0 and place_order(symbol, "BUY", max_qty):
                        positions[symbol_key] = {
                            'qty': max_qty,
                            'buy_price': last_row['close'],
                            'buy_time': current_time
                        }
                        capital -= max_qty * last_row['close']
                        last_trade_time[symbol_key] = current_time
                        trade_history.append({
                            'time': current_time, 'symbol': symbol_key,
                            'type': 'BUY', 'qty': max_qty,
                            'price': last_row['close']
                        })
                        print(f"✅ BUY {symbol_key} {max_qty} @ ₹{last_row['close']:.2f}")

                elif signal == 'SELL' and not holding_any and current_time.hour <= 20:
                    max_qty =  int(capital // last_row['close'])
                    if max_qty > 0 and place_order(symbol, "SELL", max_qty):
                        positions[symbol_key] = {
                            'qty': max_qty,
                            'sell_price': last_row['close'],
                            'Sell_time': current_time
                        }
                        capital -= max_qty * last_row['close']
                        last_trade_time[symbol_key] = current_time
                        trade_history.append({
                            'time': current_time, 'symbol': symbol_key,
                            'type': 'BUY', 'qty': max_qty,
                            'price': last_row['close']
                        })
                        print(f"✅ SELL {symbol_key} {max_qty} @ ₹{last_row['close']:.2f}")
                # SELL signal - For owned stocks
                elif symbol_key in positions:
                    pos = positions[symbol_key]
                    sell_reason = ""

                    # RSI-based sell
                    if signal == 'SELL':
                        sell_reason = "RSI"
                    # Profit target (1.5%)
                    elif last_row['close'] >= 1.015 * pos['buy_price']:
                        sell_reason = "PROFIT"
                    # Stop loss (0.5%)
                    elif last_row['close'] <= 0.995 * pos['buy_price']:
                        sell_reason = "STOP LOSS"

                    if sell_reason:
                        if place_order(symbol, "SELL", pos['qty']):
                            profit = (last_row['close'] - pos['buy_price']) * pos['qty']
                            capital += pos['qty'] * last_row['close']
                            trade_history.append({
                                'time': current_time, 'symbol': symbol_key,
                                'type': 'SELL', 'qty': pos['qty'],
                                'price': last_row['close'], 'profit': profit
                            })
                            del positions[symbol_key]
                            last_trade_time[symbol_key] = current_time
                            print(
                                f"💰 SELL {symbol_key} {pos['qty']} @ ₹{last_row['close']:.2f} | P/L: ₹{profit:.2f} ({sell_reason})")

            # End-of-day closing (3:25 PM)
            # if current_time.time() >= time(15, 25):
            #     for symbol_key, pos in list(positions.items()):
            #         symbol = next((s for s in symbols if s["tradingsymbol"] == symbol_key), None)
            #         if symbol:
            #             current_price = fetch_ltp(symbol)
            #             if current_price and place_order(symbol, "SELL", pos['qty']):
            #                 profit = (current_price - pos['buy_price']) * pos['qty']
            #                 capital += pos['qty'] * current_price
            #                 trade_history.append({
            #                     'time': current_time, 'symbol': symbol_key,
            #                     'type': 'SELL', 'qty': pos['qty'],
            #                     'price': current_price, 'profit': profit
            #                 })
            #                 del positions[symbol_key]
            #                 print(f"⏰ EOD SELL {symbol_key} {pos['qty']} @ ₹{current_price:.2f} | P/L: ₹{profit:.2f}")

            # Portfolio summary
            holdings_value = 0
            for symbol in symbols:
                symbol_key = symbol["tradingsymbol"]
                if symbol_key in positions:
                    current_price = fetch_ltp(symbol)
                    if current_price:
                        holdings_value += positions[symbol_key]['qty'] * current_price

            print(f"💼 Cash: ₹{capital:,.2f} | Holdings: ₹{holdings_value:,.2f} | Total: ₹{(capital + holdings_value):,.2f}")

            time_module.sleep(7)

    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")

    # Close all positions on exit
    print("\n🔚 Closing all positions...")
    for symbol_key, pos in list(positions.items()):
        symbol = next((s for s in symbols if s["tradingsymbol"] == symbol_key), None)
        if symbol:
            current_price = fetch_ltp(symbol)
            if current_price and place_order(symbol, "SELL", pos['qty']):
                profit = (current_price - pos['buy_price']) * pos['qty']
                capital += pos['qty'] * current_price
                print(f"🔚 Sold {symbol_key} {pos['qty']} @ ₹{current_price:.2f} | P/L: ₹{profit:.2f}")

    # Final report
    final_value = capital
    roi = ((final_value - starting_cash) / starting_cash) * 100
    print(f"\n📊 Final Portfolio Value: ₹{final_value:,.2f}")
    print(f"📈 ROI: {roi:.2f}%")
    print(f"🔢 Total Trades: {len(trade_history)}")


def start():
    run_live_trading()
# -------------------------------
# Run Live Trading
# -------------------------------
if __name__ == "__main__":
    start()
