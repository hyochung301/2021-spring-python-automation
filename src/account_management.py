import requests  # needs to be installed separately using Pip3
import json
from dotenv import load_dotenv
import os

load_dotenv()  # load environment variables from .env file

# Get the values of the required environment variables
API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
ENDPOINT = os.getenv("ENDPOINT")
END_POINT_FOR_DATA = os.getenv("END_POINT_FOR_DATA")


def get_account_info():
    # return account information in dictionary
    # example dictionary structure might be something like

    url = "{}/v2/account".format(ENDPOINT)
    headers = {
        "APCA-API-KEY-ID": API_KEY,
        "APCA-API-SECRET-KEY": SECRET_KEY
    }
    r = requests.get(url, headers=headers)
    res = json.loads(r.text)
    return res


def display_information(account_info, stock_infos) -> None:
    # display account information
    print("Account Information:")
    print("  Account Number: {}".format(account_info["account_number"]))
    print("  Cash Amt: {}".format(account_info["cash"]))
    print()

    print("Stock Information:")
    for info in stock_infos:
        print(" {}:".format(info["symbol"]))  # getting information of that symbol
        print(" prices:${}".format(info["trades"][0]["p"]))  # actually printing out the stocks' prices
