import os
import requests #needs to be installed speratley using Pip3
import json
from datetime import datetime, timedelta

end_point = "https://paper-api.alpaca.markets"  #url of Alpaca making trades
end_point_for_data = "https://data.alpaca.markets" #url for getting real time data
api_key = "PK6PH05TCS88DVTPEN86" #ID
secret_key = "8BYckAsBk6E8esFJErSKyJflrFMulVzr6COK2W8q" #password

def getAccountInformation():
    # return account information in dictionary
    # example dictionary structure might be something like
    url = "{}/v2/account".format(end_point)
    headers = {
        "APCA-API-KEY-ID": api_key,
        "APCA-API-SECRET-KEY": secret_key
    }
    r = requests.get(url, headers=headers)
    res = json.loads(r.text)
    return res
    

def getStockInformation(stock):
    # get yesterday's date at 09:00 CST timez
    yesterday = datetime.now() - timedelta(1) #Getting today's date, -1 day to get "yesterday"
    calendarDate = datetime.strftime(yesterday, '%Y-%m-%d')
    targetStart = '{}T14:00:01Z'.format(calendarDate) # 14:00 UTC(Universal) is 09:00 CST(Chicago)
    targetEnd = '{}T14:10:00Z'.format(calendarDate)

    url = "{}/v2/stocks/{}/trades?start={}&end={}&limit=1".format(end_point_for_data, stock.upper(), targetStart, targetEnd)
    headers = {
    "APCA-API-KEY-ID": api_key,
    "APCA-API-SECRET-KEY": secret_key  
    }
    r = requests.get(url, headers=headers)
    res = json.loads(r.text)
    print(stock, "data:", res)
    return res

def displayInformation(accountInfo, stockInfos):
    # display account information
    print("Account Information:")
    print("  Account Number: {}".format(accountInfo["account_number"]))
    print("  Cash Amt: {}".format(accountInfo["cash"]))
    print()

       print("Stock Information:")
    for info in stockInfos:
        print(" {}:".format(info["symbol"]))                   #getting information of that symbol
        print(" prices:${}".format(info["trades"][0]["p"]))  #actually printing out the stocks' prices  


def main():
     accountInfo = getAccountInformation()
    stocks = ['GOOGL', 'AAPL', 'LYFT', 'ABNB', 'AMZN'] #symbols of stocks used in the program
    stockInfos = []
    for stock in stocks:
        stockInfo = getStockInformation(stock)
        stockInfos.append(stockInfo)
    displayInformation(accountInfo, stockInfos)

if __name__ == '__main__':
    main()
