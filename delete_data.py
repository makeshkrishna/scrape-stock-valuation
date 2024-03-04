import pymongo
import os

# Example usage:
path = os.getcwd() 
csv_path = f'{path}\Dad\stock_.csv'
mongodb_uri = 'mongodb+srv://sha3uncle:MSRYGViZjAxyY2g3@daddb.3rb4meq.mongodb.net/'  # Replace with your MongoDB URI
mongodb_database = 'stock_db'
mongodb_collection = 'stock_valuation'

# Connect to MongoDB
client = pymongo.MongoClient(mongodb_uri)

# Access the specified database and collection
db = client[mongodb_database]
collection = db[mongodb_collection]

# Remove all documents from the collection
collection.delete_many({})

# Close the MongoDB connection
client.close()
