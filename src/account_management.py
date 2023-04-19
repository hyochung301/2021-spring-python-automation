import requests #needs to be installed speratley using Pip3
import json
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


def displayInformation(accountInfo, stockInfos) -> None:
    # display account information
    print("Account Information:")
    print("  Account Number: {}".format(accountInfo["account_number"]))
    print("  Cash Amt: {}".format(accountInfo["cash"]))
    print()

    print("Stock Information:")
    for info in stockInfos:
        print(" {}:".format(info["symbol"]))                   #getting information of that symbol
        print(" prices:${}".format(info["trades"][0]["p"]))  #actually printing out the stocks' prices
