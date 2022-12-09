import ta
from utilities.perp_bitget import PerpBitget
from utilities.custom_indicators import get_n_columns
from datetime import datetime
import telegram_send


file = open("history.txt", "a")
messages=""

now = datetime.now()
current_time = now.strftime("%d/%m/%Y %H:%M:%S")
print("--- Start Execution Time :", current_time, "---")


account_to_select = "bitget_exemple"
production = True

pair = "BTC/USDT:USDT"
timeframe = "1h"
leverage = 1

type = ["long", "short"]

# Here we have default values for the bollinger band indicator 

bol_window = 100
bol_std = 2.25
min_bol_spread = 0
long_ma_window = 500

def open_long(row):
    if (
        row['n1_close'] < row['n1_higher_band'] 
        and (row['close'] > row['higher_band']) 
        and ((row['n1_higher_band'] - row['n1_lower_band']) / row['n1_lower_band'] > min_bol_spread)
        (row['close'] > row['long_ma'])
    ):
        return True
    else:
        return False

def close_long(row):
    if (row['close'] < row['ma_band']):
        return True
    else:
        return False

def open_short(row):
    if (
        row['n1_close'] > row['n1_lower_band'] 
        and (row['close'] < row['lower_band']) 
        and ((row['n1_higher_band'] - row['n1_lower_band']) / row['n1_lower_band'] > min_bol_spread)
        and (row['close'] < row['long_ma'])        
    ):
        return True
    else:
        return False

def close_short(row):
    if (row['close'] > row['ma_band']):
        return True
    else:
        return False

bitget = PerpBitget(
    
    #get your apikey on your bitget account
    
   # apiKey=secret[account_to_select]["apiKey"]
   # secret=secret[account_to_select]["secret"],
   # password=secret[account_to_select]["password"],
)

# Get data
df = bitget.get_more_last_historical_async(pair, timeframe, 1000)

# Populate indicator
df.drop(columns=df.columns.difference(['open','high','low','close','volume']), inplace=True)
bol_band = ta.volatility.BollingerBands(close=df["close"], window=bol_window, window_dev=bol_std)
df["lower_band"] = bol_band.bollinger_lband()
df["higher_band"] = bol_band.bollinger_hband()
df["ma_band"] = bol_band.bollinger_mavg()

df['long_ma'] = ta.trend.sma_indicator(close=df['close'], window=long_ma_window)

df = get_n_columns(df, ["ma_band", "lower_band", "higher_band", "close"], 1)


# verify if our wallet status

usd_balance = float(bitget.get_usdt_equity())
print("USD balance :", round(usd_balance, 2), "$")
file.write("USD balance :", round(usd_balance, 2), "$")
messages="USD balance :" + round(usd_balance, 2)+ "$"
# check if we have positions or not 

positions_data = bitget.get_open_position()
position = [
    {"side": d["side"], "size": d["contractSize"], "market_price":d["info"]["marketPrice"], "usd_size": float(d["contractSize"]) * float(d["info"]["marketPrice"]), "open_price": d["entryPrice"]}
    for d in positions_data if d["symbol"] == pair]

row = df.iloc[-2]

# If we have position we check if we have to close our position 

if len(position) > 0:
    position = position[0]
    print(f"Current position : {position}")
    file.write(f"Current position : {position}")
    messages="Current position : "+ position +"ATM"
    if position["side"] == "long" and close_long(row):
        close_long_market_price = float(df.iloc[-1]["close"])
        close_long_quantity = float(bitget.convert_amount_to_precision(pair, position["size"]))
        exchange_close_long_quantity = close_long_quantity * close_long_market_price
        print(f"Place Close Long Market Order: {close_long_quantity} {pair[:-5]} at the price of {close_long_market_price}$ ~{round(exchange_close_long_quantity, 2)}$")
        messages="close long"+pair+"at"+round(exchange_close_long_quantity)+"$"
        if production:
            bitget.place_market_order(pair, "sell", close_long_quantity, reduce=True)

    elif position["side"] == "short" and close_short(row):
        close_short_market_price = float(df.iloc[-1]["close"])
        close_short_quantity = float(bitget.convert_amount_to_precision(pair, position["size"]))
        exchange_close_short_quantity = close_short_quantity * close_short_market_price
        print(f"Place Close Short Market Order: {close_short_quantity} {pair[:-5]} at the price of {close_short_market_price}$ ~{round(exchange_close_short_quantity, 2)}$")
        file.write( f"Place Close Short Market Order: {close_short_quantity} {pair[:-5]} at the price of {close_short_market_price}$ ~{round(exchange_close_short_quantity, 2)}$")
        messages="Close short"+pair+"at"+round(exchange_close_long_quantity)+"$"
        if production:
            bitget.place_market_order(pair, "buy", close_short_quantity, reduce=True)

# If we don't have position we check if we can take position and we take it if it's possible 

else:
    print("No active position")
    if open_long(row) and "long" in type:
        long_market_price = float(df.iloc[-1]["close"])
        long_quantity_in_usd = usd_balance * leverage
        long_quantity = float(bitget.convert_amount_to_precision(pair, float(
            bitget.convert_amount_to_precision(pair, long_quantity_in_usd / long_market_price)
        )))
        exchange_long_quantity = long_quantity * long_market_price
        print(f"Place Open Long Market Order: {long_quantity} {pair[:-5]} at the price of {long_market_price}$ ~{round(exchange_long_quantity, 2)}$")
        file.write(f"Place Open Long Market Order: {long_quantity} {pair[:-5]} at the price of {long_market_price}$ ~{round(exchange_long_quantity, 2)}$")
        messages="long"+pair+"at"+round(exchange_close_long_quantity)+"$"
        if production:
            bitget.place_market_order(pair, "buy", long_quantity, reduce=False)

    elif open_short(row) and "short" in type:
        short_market_price = float(df.iloc[-1]["close"])
        short_quantity_in_usd = usd_balance * leverage
        short_quantity = float(bitget.convert_amount_to_precision(pair, float(
            bitget.convert_amount_to_precision(pair, short_quantity_in_usd / short_market_price)
        )))
        exchange_short_quantity = short_quantity * short_market_price
        print(f"Place Open Short Market Order: {short_quantity} {pair[:-5]} at the price of {short_market_price}$ ~{round(exchange_short_quantity, 2)}$")
        file.write(f"Place Open Short Market Order: {short_quantity} {pair[:-5]} at the price of {short_market_price}$ ~{round(exchange_short_quantity, 2)}$")
        messages="short"+pair+"at"+round(exchange_close_long_quantity)+"$"
        if production:
            bitget.place_market_order(pair, "sell", short_quantity, reduce=False)

now = datetime.now()
current_time = now.strftime("%d/%m/%Y %H:%M:%S")
print("--- End Execution Time :", current_time, "---")
file.write("--- End Execution Time :", current_time, "---")
telegram_send.send(messages=[messages])
file.close()
