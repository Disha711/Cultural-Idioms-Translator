import os
import re
from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- Load Environment Variables ----------------
load_dotenv()

# ---------------- Flask Setup ----------------
app = Flask(__name__)

# ---------------- MongoDB Connection ----------------
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI is not set in environment variables")

client = MongoClient(MONGO_URI)

db = client["cultural_translator"]
collection = db["idioms"]

# ---------------- Text Preprocessing ----------------
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^\u0900-\u097F\w\s]", "", text)  # Keeps Marathi + English
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ---------------- NLP Matching ----------------
def find_best_match(user_input, docs):

    phrases = [preprocess_text(doc["phrase"]) for doc in docs]

    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    vectors = vectorizer.fit_transform([user_input] + phrases)

    similarity_scores = cosine_similarity(vectors[0:1], vectors[1:])[0]

    best_index = similarity_scores.argmax()
    best_score = similarity_scores[best_index]

    if best_score >= 0.4:
        return docs[best_index], best_score

    return None, None

# ---------------- API Route ----------------
@app.route("/translate", methods=["POST"])
def translate():

    data = request.get_json()
    user_input = data.get("text")

    if not user_input:
        return jsonify({"error": "No input text provided"}), 400

    user_input_clean = preprocess_text(user_input)

    docs = list(collection.find())

    if not docs:
        return jsonify({"message": "Dataset empty"})

    result, score = find_best_match(user_input_clean, docs)

    if result is None:
        return jsonify({"message": "Phrase not found in dataset"})

    return jsonify({
        "input_text": user_input,
        "language": result.get("language"),
        "similarity_score": round(score, 2),
        "literal_translation": result.get("literal_translation"),
        "actual_meaning": result.get("actual_meaning"),
        "cultural_translation": result.get("cultural_translation")
    })

# ---------------- Run Server ----------------
if __name__ == "__main__":
    app.run(debug=True)
