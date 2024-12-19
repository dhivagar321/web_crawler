import requests
from tabulate import tabulate
import json

# Function to fetch stock time series data for a symbol
def fetch_stock_data(symbol):
    url = "https://twelve-data1.p.rapidapi.com/time_series"
    querystring = {
        "symbol": symbol,
        "interval": "1day",
        "outputsize": "1",
        "format": "json"
    }
    headers = {
        "x-rapidapi-key": "709ec67693msh579df1437015176p131167jsn0cabe74a07de",
        "x-rapidapi-host": "twelve-data1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

# Function to fetch stock overview data for a symbol
def fetch_stock_overview(symbol):
    url = "https://twelve-data1.p.rapidapi.com/quote"
    querystring = {"symbol": symbol}
    headers = {
        "x-rapidapi-key": "709ec67693msh579df1437015176p131167jsn0cabe74a07de",
        "x-rapidapi-host": "twelve-data1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

# List of top 17 Indian stocks
indian_stocks = [
    "INFY", "TCS", "HDFC", "HDFCBANK", "RELIANCE", 
    "ICICIBANK", "ITC", "AXISBANK", "SBIN", "KOTAKBANK", 
    "ONGC", "LT", "IOC", "HINDUNILVR", "NTPC", "SUNPHARMA", "BAJFINANCE"
]

# Fetch and store data for each stock
for symbol in indian_stocks:
    print(f"\nFetching data for {symbol}...")
    stock_data = fetch_stock_data(symbol)
    stock_overview = fetch_stock_overview(symbol)

    # Check if data is fetched successfully
    if "values" in stock_data:
        latest_data = stock_data["values"][0]
        stock_data_table = [
            ["Date", latest_data["datetime"]],
            ["Open Price", f"{latest_data['open']} USD"],
            ["Close Price", f"{latest_data['close']} USD"],
            ["High Price", f"{latest_data['high']} USD"],
            ["Low Price", f"{latest_data['low']} USD"]
        ]

        # Store data in a JSON file for each symbol
        filename = f"{symbol}_stock_data.json"
        with open(filename, 'w') as file:
            json.dump(stock_data_table, file, indent=4)

        print(f"Stock Time Series Data for {symbol} stored in {filename}")
    else:
        print(f"Error fetching stock time series data for {symbol}")
        print(stock_data)

# Print a summary table for all stocks
summary_table = []
for symbol in indian_stocks:
    filename = f"{symbol}_stock_data.json"
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            summary_table.append([symbol, data[0][1], data[1][1], data[2][1], data[3][1]])
    except FileNotFoundError:
        print(f"File {filename} not found. Skipping summary entry.")

print("\nSummary of Stock Time Series Data:")
print(tabulate(summary_table, headers=["Symbol", "Date", "Open Price", "Close Price", "High Price"], tablefmt="fancy_grid"))
