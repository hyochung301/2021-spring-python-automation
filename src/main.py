# import requests #needs to be installed separately using Pip3
from stock_trading import decision
from json_functions import create_json_file


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
