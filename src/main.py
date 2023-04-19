# import requests #needs to be installed separately using Pip3
from stock_trading import get_stock_info, decision, buy_stock_return_price, sell_stock_return_price
from json_functions import create_json_file, update_json


def main():
    stocks = ['GOOGL', 'AAPL', 'LYFT', 'ABNB', 'AMZN']  # symbols of stocks used in the program
    json_content = create_json_file()
    decision(json_content, stocks)
    # all the logs will be generated inside getStockInformationFromJson function for now
    # accountInfo = getAccountInformation()
    # displayInformation(accountInfo, stockInfos)
    print("program end")


if __name__ == '__main__':
    main()
