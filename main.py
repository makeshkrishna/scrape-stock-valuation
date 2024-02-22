import pandas as pd
import os
from tqdm import tqdm
from datetime import datetime, timezone
from pymongo import MongoClient
from scraper import scrape_stock_data 


# Function to read the last processed stock symbol from the CSV file
def get_last_processed_stock(csv_path):
    try:
        df = pd.read_csv(csv_path)
        return df['Symbol'].tolist()
    except FileNotFoundError:
        return []

# Function to write the processed stock symbols to the CSV file
def write_processed_stock(csv_path, processed_stocks):
    df = pd.DataFrame({'Symbol': processed_stocks})
    df.to_csv(csv_path, index=False)

# Example usage:
    # C:\sha3uncle\Dad\stock_.csv
path = os.getcwd() 
csv_path = f'{path}\stock_.csv'
log_csv_path = f'{path}\processed_stocks_log_.csv'  # New CSV for logging processed stocks
mongodb_uri = 'mongodb+srv://sha3uncle:MSRYGViZjAxyY2g3@daddb.3rb4meq.mongodb.net/'  # Replace with your MongoDB URI
mongodb_database = 'stock_db'
mongodb_collection = 'stock_valuation'

client = MongoClient(mongodb_uri)
db = client[mongodb_database]
collection = db[mongodb_collection]

# Load stock symbols from CSV
df = pd.read_csv(csv_path)
stock_symbols = df['Symbol'].tolist()
# print(type(stock_symbols[1]))

# Load already processed stock symbols
processed_stocks = get_last_processed_stock(log_csv_path)

# Remove already processed stocks from the list
stock_symbols_to_process = [symbol for symbol in stock_symbols if symbol not in processed_stocks]

# Iterate through stock symbols
for stock_symbol in tqdm(stock_symbols_to_process, desc="Processing stocks"):
    # Call the scrape_stock_data function
    result = scrape_stock_data(stock_symbol)

    if result:
        # Unpack the result
        valuation_data, relative_valuation_data, dcf_valuation_data, dcf_currency_data, price , price_ = result
        
        # Remove space between digits
        price_str = str(price).replace(" ", "")
        price_ = str(price_).replace(" ", "")
        dcf_valuation_data = str(dcf_valuation_data).replace(" ", "")
        valuation_data_str = str(valuation_data).replace(" ","")
        relative_valuation_data_str = " ".join(valuation_data_str.strip().split())
        dcf_valuation_data_str = " ".join(dcf_valuation_data.strip().split())

        # Print the results with reduced space
        print('---------------------------------------------------------')
        print(f" Stock Name: {stock_symbol}")
        print(f"Price of stock: {price_str}")
        print(f"Price of stock_2: {price_}")
        print(f"Relative Valuation Price: {relative_valuation_data_str}")
        print(f"Relative valuation : {relative_valuation_data}")
        print(f"DCF Valuation: {dcf_currency_data}")
        print(f"DCF Valuation Price: {dcf_valuation_data_str}")
        print('---------------------------------------------------------')


        # Create a document to insert into MongoDB
        document = {
            'timestamp': datetime.now(timezone.utc),
            'stock_symbol': stock_symbol,
            'Price_of_stock': price_str,
            'Price_of_stock_' : price_,
            'Relative_Valuation_Price': relative_valuation_data_str,
            'Relative_valuation': relative_valuation_data,  # Replace with your calculation
            'DCF_Valuation_Price': dcf_valuation_data_str,
            'DCF_Valuation': dcf_currency_data,  # Replace with your calculation
        }

        # Insert the document into MongoDB
        collection.insert_one(document)

        # # Update the list of processed stocks
        processed_stocks.append(stock_symbol)

        # Write the updated list to the log CSV file
        write_processed_stock(log_csv_path, processed_stocks)

