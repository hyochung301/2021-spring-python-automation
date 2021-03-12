import os
import requests
import json

end_point = os.environ['alpaca_end_point']
api_key = os.environ['alpaca_api_key']
secret_key = os.environ['alpaca_secret_key']

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
    # TODO here
    # fetch information about the stock given as a parameter
    # return stock information in dictionary
    # example dictionary structure might be something like
    '''
    {
        "name": "google",
        "price": 2056,
        "date": "2021-03-09"
    }
    '''
    return {
        "name": stock,
        "price": 123,
        "date": "2021-03-09"
    }

def displayInformation(accountInfo, stockInfos):
    # display account information
    print("Account Information:")
    print("  Account Number: {}".format(accountInfo["account_number"]))
    print("  Cash Amt: {}".format(accountInfo["cash"]))
    print()

    # TODO: display stock information
    print("Stock Information:")
    print("  TODO: display stock information")
    


def main():
    accountInfo = getAccountInformation()
    stocks = ['Google', 'Apple', 'Facebook', 'Microsoft', 'Amazon']
    stockInfos = []
    for stock in stocks:
        stockInfo = getStockInformation(stock)
        stockInfos.append(stockInfo)
    displayInformation(accountInfo, stockInfos)

if __name__ == '__main__':
    main()