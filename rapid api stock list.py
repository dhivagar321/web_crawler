import requests
from pymongo import MongoClient

# Your Twelve Data API key
API_KEY = '739e405083604c21967dc03d85875f02'

# API endpoint for stock list from NSE or BSE
BASE_URL = 'https://api.twelvedata.com/stocks'

# MongoDB connection URI
MONGO_URI = 'mongodb://localhost:27017/'

def get_stock_list(exchange):
    params = {
        'exchange': exchange,
        'apikey': API_KEY
    }
    
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        stock_data = response.json()
        return stock_data
    else:
        print(f"Error: Unable to fetch data (Status code: {response.status_code})")
        return None

def save_to_mongodb(collection, stock_data, exchange):
    if stock_data and 'data' in stock_data:
        for stock in stock_data['data']:
            stock['exchange'] = exchange
        collection.insert_many(stock_data['data'])

def main():
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client['indian_stock_list']
    
    # Get stock list for NSE
    nse_stocks = get_stock_list('NSE')
    if nse_stocks:
        print("Saving NSE Stock List to MongoDB...")
        nse_collection = db['nse_stocks']
        save_to_mongodb(nse_collection, nse_stocks, 'NSE')
        print("NSE Stock List saved.")
    
    # Get stock list for BSE
    bse_stocks = get_stock_list('BSE')
    if bse_stocks:
        print("Saving BSE Stock List to MongoDB...")
        bse_collection = db['bse_stocks']
        save_to_mongodb(bse_collection, bse_stocks, 'BSE')
        print("BSE Stock List saved.")

    # Close MongoDB connection
    client.close()

if __name__ == '__main__':
    main()
