import json
from pymongo import MongoClient
from urllib.parse import quote_plus
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://sharmojj:Sharmover%40100@cluster0.1snfcdx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))



# Test the connection
try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB Atlas!")
except Exception as e:
    print("Connection failed:", e)
    exit()

# Select database and collection
db = client["amtronics"]  # You can change this to your preferred database name
collection = db["products"]  # You can change this to your preferred collection name

# Load JSON data from file
json_file_path = "products.json"  # Make sure the file is in the same directory or provide full path

# Since the file contains multiple JSON objects (one per line), we need to process it line by line
products = []
with open(json_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        if line.strip():  # Skip empty lines
            try:
                product = json.loads(line)
                products.append(product)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON line: {e}")
                print("Problematic line:", line)

# Insert data into MongoDB
if products:
    try:
        # Insert many documents at once
        result = collection.insert_many(products)
        print(f"Successfully inserted {len(result.inserted_ids)} documents")
        
        # Create indexes for better query performance
        collection.create_index([("sku", 1)])  # Index on SKU field
        collection.create_index([("en_category", 1)])  # Index on category field
        collection.create_index([("price", 1)])  # Index on price field
        print("Created indexes on sku, en_category, and price fields")
        
    except Exception as e:
        print("Error inserting documents:", e)
else:
    print("No valid products found to insert")

# Close the connection
client.close()