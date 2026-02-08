import pandas as pd
from pymongo import MongoClient

df = pd.read_csv("eng_mar_idioms_dataset_csv1.csv")

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

client = MongoClient("mongodb+srv://dishaparte_db_user:NhyeJcvixvsK4pnw@nlp.qlaxdo4.mongodb.net/?appName=NLP")
db = client["cultural_translator"]
collection = db["idioms"]

data = df.to_dict(orient="records")

collection.delete_many({})  # Optional: clears old data
collection.insert_many(data)

print("✅ Data inserted successfully!")
