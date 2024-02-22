from pymongo import MongoClient
import pandas as pd

# Specify your MongoDB URI, database, and collection
mongodb_uri = 'mongodb+srv://sha3uncle:MSRYGViZjAxyY2g3@daddb.3rb4meq.mongodb.net/'
mongodb_database = 'stock_db'
mongodb_collection = 'stock_valuation'

def export_mongodb_to_csv(uri, database, collection, csv_filename):
    # Connect to MongoDB
    client = MongoClient(uri)
    db = client[database]
    collection = db[collection]

    # Retrieve data from MongoDB collection
    data = list(collection.find())

    # Convert data to DataFrame
    df = pd.DataFrame(data)

    # Write DataFrame to CSV file
    df.to_csv(csv_filename, index=False)

    print(f'Data exported to {csv_filename}')

# Specify the desired CSV filename
csv_filename = 'stock_data_output_3.csv'

# Export MongoDB data to CSV
export_mongodb_to_csv(mongodb_uri, mongodb_database, mongodb_collection, csv_filename)
