import os
from flask import Flask, render_template, request, jsonify
from anagrams import find_anagrams
from mysql_connection import DatabaseConnection
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

total_requests = 0
host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_DATABASE")

# Establish database connection
connection = DatabaseConnection(host, database, user, db_password)


@app.route("/api/v1/similar", methods=["GET"])
def get_similar_words():
    global total_requests
    word = request.args.get("word")
    if word:
        total_requests += 1
        table_created = connection.create_table()
        # Only insert words if the table was created
        if table_created:
            print("Starting insert dataset to the table...")
            connection.insert_words_from_file("./words_dataset.txt")

        # Find anagrams
        print("Finding anagrams...")
        anagrams = find_anagrams(connection, word)

        # Return JSON response
        return jsonify({"similar": anagrams if anagrams else False})
    else:
        return jsonify({"error": "Word parameter is missing"}), 400


@app.route("/api/v1/add-word", methods=["POST"])
def add_word():
    try:
        # Get the word to add from the request body
        data = request.json
        word = data.get("word")

        # Check if the word is provided
        if not word:
            return jsonify({"error": "Word is missing in the request body"}), 400

        # Check if the word already exists in the database
        connection.execute("SELECT COUNT(*) FROM words WHERE word = %s", (word,))
        count = connection.fetchone()[0]
        if count > 0:
            return jsonify({"error": "Word already exists in the database"}), 400

        # Insert the word into the database
        connection.execute("INSERT INTO words (word) VALUES (%s)", (word,))
        connection.commit()

        return jsonify({"message": "Word added successfully"}), 200

    except Exception as e:
        print("Error adding word to database:", e)
        return jsonify({"error": "Failed to add word to database"}), 400


@app.route("/api/v1/stats", methods=["GET"])
def get_stats():
    global total_requests
    connection.execute("SELECT COUNT(*) FROM words")
    total_words = connection.fetchone()[0]
    stats = {
        "totalWords": total_words,
        "totalRequests": total_requests,
    }
    return jsonify(stats)


@app.route("/close-connection", methods=["POST", "GET"])
def close_connection():
    print("Closing database connection...")
    connection.close()
    return jsonify({"message": "Database connection closed"}), 200


if __name__ == "__main__":
    app.run(debug=True)  # Enable debug mode for development
