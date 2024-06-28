import requests
from bs4 import BeautifulSoup

# Alpha Vantage API Key
api_key = '3MP1UIT4AZ5NS4QP'

# Function to fetch stock data from Alpha Vantage
def fetch_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    return data

# Example usage of Alpha Vantage API
symbol = 'AAPL'  # Apple Inc.
stock_data = fetch_stock_data(symbol)
print(stock_data)

# Web crawling example function
def crawl_website(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

# Example usage of web crawler
url = 'https://www.example.com'
soup = crawl_website(url)

# If the soup object is not None, we can start parsing it
if soup:
    # Find all hyperlinks in the page
    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        text = link.get_text()
        print(f'Text: {text}, Href: {href}')
