from datetime import datetime, timedelta
from account_management import end_point, end_point_for_data, api_key, secret_key
import requests  # needs to be installed separately using Pip3
import json
from json_functions import updateJson


def get_stock_info(stock):
    # get yesterday's date at 09:00 CST timez

    # yesterday = datetime.now() - timedelta(1) #Getting today's date, -1 day to get "yesterday"
    # yesterdayDate = datetime.strftime(yesterday, '%Y-%m-%d') #yesterday format
    calendar_date = datetime.strftime(datetime.now(), '%Y-%m-%d')
    target_start = '{}T14:00:01Z'.format(calendar_date)  # 14:00 UTC(Universal) is 09:00 CST(Chicago)
    target_end = '{}T14:10:00Z'.format(calendar_date)

    url = "{}/v2/stocks/{}/trades?start={}&end={}&limit=1".format(end_point_for_data, stock.upper(), target_start,
                                                                  target_end)
    headers = {
        "APCA-API-KEY-ID": api_key,
        "APCA-API-SECRET-KEY": secret_key
    }
    r = requests.get(url, headers=headers)
    res = json.loads(r.text)
    print(stock, "data:", res)
    return res


def decision(json_content, stocks):  # maybe include stock info to be now
    # this is the wrapper function to initiate updating stock information
    # iterate (make a for loop) over stocks
    # for each stock, get the most recent information from jsonContent
    # if there's no stock information in jsonContent, that means we don't own any of that stock
    # in that case, buy
    # if any information is present, get the current price for stock, compare with the previous price saved in jsonContent
    # do the business logic from there accordingly
    for stock in stocks:
        # get information from jsonContent here
        stock_price = json_content[stock]["price"]  # change this with information found from jsonContent
        current_price = stockInfo["trades"][0]["p"]  # this will the be the current price of the stock

        if stock_price is None:
            # we don't have any of this stock, please buy 5 shares (you can change the number of shares)
            # then update stock_price
            buy_stock_return_price(stock, current_price, 5)  # we now own the stock
        else:
            # we have some of this stock, get the current price and compare it with previous price
            # then print what actions have been taken here
            # use buyStockAndReturnPrice and sellStockAndReturnPrice if needed (business logic)
            current_price = get_stock_info(stock)  # getcurrentprice
            if current_price >= 1.05 * stock_price:
                # if the price has gone up 5% or more, sell
                sell_stock_return_price(stock, current_price, 5)
            elif current_price <= stock_price * 0.95:  # if gone down 5% or more, buy
                buy_stock_return_price(stock, current_price, 5)
            else:
                pass

        # now that the price is updated, save that info to json file


def buy_stock_return_price(stock, current_price, num_share=5) -> None:
    url = "{}/v2/orders".format(end_point)

    headers = {
        "APCA-API-KEY-ID": api_key,
        "APCA-API-SECRET-KEY": secret_key
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

    # get transaction time, price, share, stock and additional stock info that with string from history
    if res["status"] == "accepted":
        updated_price = current_price
        num_share = num_share
        time = None
        print(stock, "has been bought at $", updated_price, "@", time)

        updateJson(stock, updated_price, num_share, time)

    # we don't have any of this stock, please buy 5 shares (you can change the number of shares)
    # then update stockPrice
    # print how much of which stock we bought at which price here
    # return how much share we bought


def sell_stock_return_price(stock, current_price, num_share=5):
    url = "{}/v2/orders".format(end_point)

    headers = {
        "APCA-API-KEY-ID": api_key,
        "APCA-API-SECRET-KEY": secret_key
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
    # get transaction time, price, share, stock and additional stock info that with string from history
    if res["status"] == "accepted":
        updated_price = current_price
        num_share = num_share
        time = None
        print(stock, "has been sold at $", updated_price, "@", time)

        updateJson(stock, updated_price, num_share, time)

    else:
        print("transaction failed")
    # For simplicity, sell all the shares we have
    # we could improve this logic to sell partial shares of what we own, but let's do it later
    # print how much of which stock we sold at which price here and what the gain is
