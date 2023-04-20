from datetime import datetime
import requests  # needs to be installed separately using Pip3
import json
from json_functions import update_json
from dotenv import load_dotenv
import os

load_dotenv()  # load environment variables from .env file

# Get the values of the required environment variables
API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
ENDPOINT = os.getenv("ENDPOINT")
END_POINT_FOR_DATA = os.getenv("END_POINT_FOR_DATA")

def get_stock_info(stock):
    # get yesterday's date at 09:00 CST timez

    # yesterday = datetime.now() - timedelta(1) #Getting today's date, -1 day to get "yesterday"
    # yesterdayDate = datetime.strftime(yesterday, '%Y-%m-%d') #yesterday format
    calendar_date = datetime.strftime(datetime.now(), '%Y-%m-%d')
    target_start = '{}T14:00:01Z'.format(calendar_date)  # 14:00 UTC(Universal) is 09:00 CST(Chicago)
    target_end = '{}T14:10:00Z'.format(calendar_date)

    url = "{}/v2/stocks/{}/trades?start={}&end={}&limit=1".format(END_POINT_FOR_DATA, stock.upper(), target_start,
                                                                  target_end)
    headers = {
        "APCA-API-KEY-ID": API_KEY,
        "APCA-API-SECRET-KEY": SECRET_KEY
    }
    r = requests.get(url, headers=headers)
    res = json.loads(r.text)
    print(stock, "data:", res)
    return res


def decision(json_content, stocks):  # maybe include stock info to be now
    # this is the wrapper function to initiate updating stock information iterate (make a for loop) over stocks for
    # each stock, get the most recent information from jsonContent if there's no stock information in jsonContent,
    # that means we don't own any of that stock in that case, buy if any information is present, get the current
    # price for stock, compare with the previous price saved in jsonContent do the business logic from there accordingly
    for stock in stocks:
        # get information from jsonContent here
        num_share = 0
        stock_price = json_content[stock]["price"]  # change this with information found from jsonContent
        stock_info = get_stock_info(stock)
        current_price = stock_info["trades"][0]["p"]  # this will be the current price of the stock

        if stock_price is None:
            # we don't have any of this stock, please buy 5 shares (you can change the number of shares)
            # then update stock_price
            num_share = buy_stock_return_price(stock, current_price, 5)  # we now own the stock
        else:
            # we have some of this stock, get the current price and compare it with previous price
            # then print what actions have been taken here
            # use buyStockAndReturnPrice and sellStockAndReturnPrice if needed (business logic)
            current_price = get_stock_info(stock)  # get current price
            if current_price >= 1.05 * stock_price:
                # if the price has gone up 5% or more, sell
                num_share -= sell_stock_return_price(stock, current_price, 5)
            elif current_price <= stock_price * 0.95:
                # if gone down 5% or more, buy
                num_share += buy_stock_return_price(stock, current_price, 5)
            else:
                pass

        # now that the price is updated, save that info to json file
        update_json(stock, current_price, num_share)


def buy_stock_return_price(stock, current_price, num_share=5) -> int:
    url = "{}/v2/orders".format(ENDPOINT)

    headers = {
        "APCA-API-KEY-ID": API_KEY,
        "APCA-API-SECRET-KEY": SECRET_KEY
    }

    body = {
        "symbol": stock,
        "qty": "{}".format(num_share),
        "side": "buy",
        "type": "market",
        "time_in_force": "day",
    }

    r = requests.post(url, headers=headers, data=body)

    res = json.loads(r.text)
    num_share_bought = 0
    # get transaction time, price, share, stock and additional stock info that with string from history
    if res["status"] == "accepted":
        updated_price = current_price
        num_share_bought = num_share
        time = datetime.fromisoformat(res["submitted_at"][:-1])
        print(stock, "has been bought at $", updated_price, "@", time.strftime("%Y-%m-%d %H:%M:%S"))

        # update_json(stock, updated_price, num_share, time)
    elif r.status_code == 403:
        print(f"Forbidden to purchase {stock}. Buying power or shares is not sufficient to purchase.")
    elif r.status_code == 422:
        print(f"purchase {stock} unprocessable. Input parameters are not recognized.")
    # we don't have any of this stock, please buy 5 shares (you can change the number of shares)
    # then update stockPrice
    # print how much of which stock we bought at which price here
    return num_share_bought  # return how much share we bought


def sell_stock_return_price(stock, current_price, num_share=5) -> int:
    url = "{}/v2/orders".format(ENDPOINT)

    headers = {
        "APCA-API-KEY-ID": API_KEY,
        "APCA-API-SECRET-KEY": SECRET_KEY
    }

    body = {
        "symbol": stock,
        "qty": "{}".format(num_share),
        "side": "sell",
        "type": "market",
        "time_in_force": "day",
    }

    r = requests.post(url, headers=headers, data=body)
    res = json.loads(r.text)
    num_share_sold = 0
    # get transaction time, price, share, stock and additional stock info that with string from history
    if res["status"] == "accepted":
        updated_price = current_price
        num_share_sold = num_share
        time = datetime.fromisoformat(res["submitted_at"][:-1])
        print(stock, "has been sold at $", updated_price, "@", time.strftime("%Y-%m-%d %H:%M:%S"))

        # update_json(stock, updated_price, num_share, time)
    else:
        print("transaction failed")
        if r.status_code == 403:
            print(f"Forbidden to sell {stock}. Possibly shares is not sufficient to sell.")
        elif r.status_code == 422:
            print(f"Selling {stock} unprocessable. Input parameters are not recognized.")

    # For simplicity, sell all the shares we have
    # we could improve this logic to sell partial shares of what we own, but let's do it later
    # print how much of which stock we sold at which price here and what the gain is
    return num_share_sold
