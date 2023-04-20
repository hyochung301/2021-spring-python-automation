import json
import os  # accessing environment variable.
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env file


def create_json_file():
    if not os.path.isfile("wallet.json"):
        with open("wallet.json", "w") as file:  # check if wallet.json exists #if not  #create a wallet.json file
            json.dump({}, file)
        return {}  # if the file has been just created, it will return an empty dict {}     python file write
    else:
        with open("wallet.json") as file:
            filedata = json.load(file)  # parse json data from file string using json.load()
        return filedata
        # once the file is created above (if not already existed), parse the file and return a dict of all the
        # information


def update_json(stock, updated_price, num_share):
    # this function updates json files
    # get transaction details directly from buy/sell function to avoid working with multiple return values
    # 2 things need to happen
    # if numShare is 0, then we don't own any of this stock, remove any information about them in json file
    # else update the information
    with open("wallet.json") as file:
        json_content = json.load(file)  # call json file into a dictionary

    if num_share > 0:
        json_content[stock] = {"price": updated_price, "num_shares": num_share}
        # we bought some stock, update the json file
        print(stock, "has been added to the wallet")
    else:
        # we sold all the stock, delete any information about the stock from json file
        del json_content[stock]
        print(stock, "has been removed from the wallet")
    with open("wallet.json", "w") as file:
        json.dump(json_content, file)
