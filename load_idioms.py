import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

# Read CSV
df = pd.read_csv("eng_mar_idioms_dataset_csv1.csv")

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client["cultural_translator"]
collection = db["idioms"]

data = df.to_dict(orient="records")

# Optional: clear old data
collection.delete_many({})

# Insert new data
collection.insert_many(data)

print("✅ Data inserted successfully!")
