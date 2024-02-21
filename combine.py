import pandas as pd

# Load the CSV files
valuation_df = pd.read_csv(r'C:\sha3uncle\Dad\stock_.csv')
market_cap_df = pd.read_csv(r'C:\sha3uncle\Dad\stock_scraper\stock_data_output.csv')

# Merge the dataframes based on the 'stock_symbol' column
combined_df = pd.merge(valuation_df, market_cap_df, left_on='stock_symbol', right_on='Symbol')

combined_df.shape

# Merge the dataframes based on the 'stock_symbol' column


