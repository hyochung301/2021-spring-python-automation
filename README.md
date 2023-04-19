# Python Stock Trading Automation Project
This project provides a set of Python scripts for automating stock trading using the Alpaca trading API
(All the code examples are to be executed in the root directory)

## Getting Started
### Prerequisites
Before running the scripts, you need to set up a few things:
* Create an account on [Alpaca](https://alpaca.markets/)
* Obtain API credentials (API key and secret key) from Alpaca and store them in a .env file in the root directory of the project, using the following format:
```APCA_API_KEY_ID=<your_api_key>
APCA_API_SECRET_KEY=<your_secret_key>
```
* Install the required Python packages by running 
```pip install -r requirements.txt```




## How to Run the App
To run the main application, execute the following command in the root directory of the project:
```python3 src/main.py```

## How to Run Unit Tests
To run the unit tests, execute the following command in the root directory of the project:
```python3 -m unittest```


# API Reference
The Alpaca trading API reference is available at:

https://alpaca.markets/docs/api-references/trading-api/
