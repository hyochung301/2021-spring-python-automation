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

    #yesterday = datetime.now() - timedelta(1) #Getting today's date, -1 day to get "yesterday"
    #yesterdayDate = datetime.strftime(yesterday, '%Y-%m-%d') #yesterday format
    calendarDate = datetime.strftime(datetime.now(), '%Y-%m-%d')
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

def createJsonFile():
    if not os.path.isfile("wallet.json"):
        with open("wallet.json", "w") as file:  #check if wallet.json exists #if not  #create a wallet.json file
            file.write( {} )
        return {}         # if the file has been just created, it will return an empty dict {}     pytjhon file write               
    else:
        with open("wallet.json") as file:
            filedata = json.load(file) #parse json data from file string using json.load()
        return filedata
            # once the file is created above (if not already existed), parse the file and return a dict of all the information

def decision(jsonContent, stocks): #maybe include stock info to be now
    # this is the wrapper function to initiate updating stock information
    # iterate (make a for loop) over stocks
    # for each stock, get the most recent information from jsonContent
    # if there's no stock information in jsonContent, that means we don't own any of that stock
    # in that case, buy
    # if any information is present, get the current price for stock, compare with the previous price saved in jsonContent
    # do the business logic from there accordingly
    for stock in stocks:
        # get information from jsonContent here
        stockPrice = jsonContent[stock]["price"] # change this with information found from jsonContent
        currentPrice = stockInfo["trades"][0]["p"] # this will the be the current price of the stock

        if stockPrice is None:
            # we don't have any of this stock, please buy 5 shares (you can change the number of shares)
            # then update stockPrice
            buyStockAndReturnPrice(stock,5,currentPrice) # we now own the stock
        else:
            # we have some of this stock, get the current price and compare it with previous price
            # then print what actions have been taken here
            # use buyStockAndReturnPrice and sellStockAndReturnPrice if needed (business logic)
            currentPrice = getStockInformation(stock) #getcurrentprice
            if currentPrice >= 1.05*stockPrice:
                 #if the price has gone up 5% or more, sell
                sellStockAndReturnPrice(stock,5,currentPrice)
            elif currentPrice <= stockPrice*0.95: #if gone down 5% or more, buy
                buyStockAndReturnPrice(stock,5,currentPrice)
            else: 
               pass

        # now that the price is updated, save that info to json file

def buyStockAndReturnPrice(stock ,numShare=5, currentPrice):
    url = "{}/v2/orders".format(end_point)
    
    headers = {
    "APCA-API-KEY-ID": api_key,
    "APCA-API-SECRET-KEY": secret_key  
    }
    
    body = {
        "symbol": stock,
        "qty": "{}".format(numShare),
        "side": "buy",
        "type": "market",
        "time_in_force": "day",
    }

    r = requests.post(url, headers=headers, data=body)

    res = json.loads(r.text)

    #get transaction time, price, share, stock and additional stock info that with string from history
    if res["status"] == "accepted":
        updatedPrice = currentPrice
        numShare = numShare
        time = None
        print(stock, "has been bought at $", updatedPrice, "@", time)
        
        updateJson(stock, updatedPrice, numShare, time)

    # we don't have any of this stock, please buy 5 shares (you can change the number of shares)
    # then update stockPrice
    # print how much of which stock we bought at which price here
    # return how much share we bought    
    
def sellStockAndReturnPrice(stock, numShare=5, currentPrice):
    url = "{}/v2/orders".format(end_point)

    headers = {
    "APCA-API-KEY-ID": api_key,
    "APCA-API-SECRET-KEY": secret_key  
    }

    body = {
     "symbol": stock,
        "qty": "{}".format(numShare),
        "side": "sell",
        "type": "market",
        "time_in_force": "day",
    }

    r = requests.post(url, headers=headers, data=body)
    res = json.loads(r.text)
    #get transaction time, price, share, stock and additional stock info that with string from history
    if res["status"] == "accepted":
        updatedPrice = currentPrice
        numShare = numShare
        time = None
        print(stock, "has been sold at $", updatedPrice, "@", time)
        
        updateJson(stock, updatedPrice, numShare, time)

    else:
         print("transaction failed")
    # For simplicity, sell all the shares we have
    # we could improve this logic to sell partial shares of what we own, but let's do it later
    # print how much of which stock we sold at which price here and what the gain is


def updateJson(stock, updatedPrice, numShare, time):
    # complete this function to update json file]
    # get transaction details directly from buy/sell function to avoid working with multiple return values
    # 2 things need to happen
    # if numShare is 0, then we don't own any of this stock, remove any information about them in json file
    # else update the information
    jsonContent = json.load("wallet.json") #call json file into a dictionary
    if numShare > 0:
        jsonContent[stock] = {}
        jsonContent[stock]["price"] = updatedPrice
        jsonContent[stock]["numShare"] = numShare  
        # we bought some of the stock, update the json file
        with open('wallet.json', 'w') as file:
            json.dump(jsonContent, file)
        print(stock, "has been added to the wallet")
    else:
        # we sold all the stock, delete any information about the stock from json file
         with open('wallet.json', 'w') as file:
            del  jsonContent[stock]
         print(stock, "has been removed from the wallet")

def main():
    stocks = ['GOOGL', 'AAPL', 'LYFT', 'ABNB', 'AMZN'] #symbols of stocks used in the program
    jsonContent = createJsonFile()
    decision(jsonContent, stocks)  
    print("program end")
    # all the logs will be generated inside getSotkcInformationFromJson function for now
    # accountInfo = getAccountInformation()
    # displayInformation(accountInfo, stockInfos) 




if __name__ == '__main__':
    main()
