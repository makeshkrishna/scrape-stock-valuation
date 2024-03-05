import pandas as pd
import os
# Load the CSV files
path = os.getcwd() 
valuation_df = pd.read_csv(f'{path}\stock_.csv')
market_cap_df = pd.read_csv(f'{path}\stock_scraper\stock_data_output.csv')

# Merge the dataframes based on the 'stock_symbol' column
combined_df = pd.merge(valuation_df, market_cap_df, left_on='stock_symbol', right_on='Symbol')

combined_df.shape

# Merge the dataframes based on the 'stock_symbol' column


