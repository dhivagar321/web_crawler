import yfinance as yf

print("whether the stock is good time to buy or not")

def predict_stock_recommendation(stock_symbol):
    # Create a Ticker object for the specified stock symbol
    stock = yf.Ticker(stock_symbol)

    # Get real-time data
    real_time_data = stock.info

    # Extract relevant data for analysis
    current_price = real_time_data.get('currentPrice', None)
    previous_close = real_time_data.get('previousClose', None)
    fifty_day_avg = real_time_data.get('fiftyDayAverage', None)
    two_hundred_day_avg = real_time_data.get('twoHundredDayAverage', None)
    print("current price",current_price)
    print("previous close", previous_close)
    print("fifty day average", fifty_day_avg)
    print("two hundred day average", two_hundred_day_avg)
    
    # Perform analysis to predict recommendation
    if current_price is not None and previous_close is not None:
        price_change = current_price - previous_close
        if price_change > 0 and current_price > fifty_day_avg and current_price > two_hundred_day_avg:
            return "Good time to buy"
        elif price_change < 0:
            return "Price is dropping, wait for a better opportunity"
        else:
            return "Neutral"
    else:
        return "Insufficient data"

def main():
    # Get user input for the stock symbol
    stock_symbol = input("Enter the stock symbol: ")

    # Predict the recommendation
    recommendation = predict_stock_recommendation(stock_symbol.upper())

    # Print the recommendation
    print(f"Recommendation for {stock_symbol.upper()}: {recommendation}")

if __name__ == "__main__":
    main() 



'''
import requests
import yfinance as yf
from bs4 import BeautifulSoup
from pymongo import MongoClient
from tabulate import tabulate

def fetch_sp500_companies():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to load page {url}")

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'wikitable sortable'})
    companies = []

    for row in table.findAll('tr')[1:]:
        cells = row.findAll('td')
        ticker = cells[0].text.strip()
        company_name = cells[1].text.strip()
        companies.append((ticker, company_name))
    
    return companies

def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker.replace('.', '-'))
        
        # Try to fetch daily data first
        hist = stock.history(period="1d")
        if hist.empty:
            # If no daily data, try fetching monthly data
            hist = stock.history(period="1mo")
            if hist.empty:
                return None
        
        data = {
            'Ticker': ticker,
            'Date': hist.index[0].strftime('%Y-%m-%d'),
            'Open': hist['Open'].iloc[0],
            'Close': hist['Close'].iloc[0],
            'High': hist['High'].iloc[0],
            'Low': hist['Low'].iloc[0]
        }
        
        if data['Close'] < data['Open']:
            data['Suggestion'] = "Good time to buy"
        else:
            data['Suggestion'] = "Not a good time to buy"
        
        return data
    except Exception as e:
        print(f"Failed to fetch data for {ticker}: {e}")
        return None

def fetch_quarterly_report(ticker):
    try:
        stock = yf.Ticker(ticker.replace('.', '-'))
        quarterly_financials = stock.quarterly_financials

        if quarterly_financials.empty:
            return None

        quarterly_data = quarterly_financials.T.to_dict('records')
        
        return quarterly_data
    except Exception as e:
        print(f"Failed to fetch quarterly report for {ticker}: {e}")
        return None

def store_data_to_mongodb(data, db_name='stock_data', collection_name='sp500'):
    # Connect to MongoDB
    client = MongoClient('localhost', 27017)  # Adjust the host and port as necessary
    db = client[db_name]
    collection = db[collection_name]
    # Insert the stock data into the collection
    collection.update_one(
        {'Ticker': data['Ticker']},
        {'$set': data},
        upsert=True
    )

def print_all_companies_and_store_stock_data(companies):
    print("All Companies in the S&P 500 with Stock Data:")
    for ticker, company_name in companies:
        print(f"{ticker}: {company_name}")
        stock_data = fetch_stock_data(ticker)
        if stock_data:
            stock_table = [
                ['Date', 'Open', 'Close', 'High', 'Low', 'Suggestion'],
                [stock_data['Date'], stock_data['Open'], stock_data['Close'], stock_data['High'], stock_data['Low'], stock_data['Suggestion']]
            ]
            print(tabulate(stock_table, headers='firstrow', tablefmt='grid'))
            store_data_to_mongodb(stock_data)
            
            # Fetch and print quarterly report
            quarterly_report = fetch_quarterly_report(ticker)
            if quarterly_report:
                print("  Quarterly Report:")
                for report in quarterly_report:
                    report_table = [['Attribute', 'Value']] + [[key, value] for key, value in report.items()]
                    print(tabulate(report_table, headers='firstrow', tablefmt='grid'))
                store_data_to_mongodb({"Ticker": ticker, "Quarterly Report": quarterly_report})
            else:
                print("  No quarterly report available")
        else:
            print("  No stock data available")
        print()

if _name_ == "_main_":
    companies = fetch_sp500_companies()
    print_all_companies_and_store_stock_data(companies)
    print(f"\nTotal number of companies: {len(companies)}")
'''
