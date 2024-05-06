import os
from flask import Flask, render_template, request, jsonify
from anagrams import find_anagrams
from mysql_connection import DatabaseConnection
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_DATABASE")

# Establish database connection
db_connection = DatabaseConnection(host, database, user, db_password)


@app.route("/api/v1/similar", methods=["GET"])
def get_similar_words():
    word = request.args.get("word")
    table_created = db_connection.create_table()

    # Only insert words if the table was created
    if table_created:
        print("Starting insert dataset to the table...")
        db_connection.insert_words_from_file("./words_dataset.txt")

    # Find anagrams
    print("Finding anagrams...")
    anagrams = find_anagrams(db_connection, word)

    # Close connection
    print("Closing database connection...")
    db_connection.close()

    # Return JSON response
    return jsonify({"similar": anagrams if anagrams else False})


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
        db_connection.execute("SELECT COUNT(*) FROM words WHERE word = %s", (word,))
        count = db_connection.fetchone()[0]
        if count > 0:
            return jsonify({"error": "Word already exists in the database"}), 400

        # Insert the word into the database
        db_connection.execute("INSERT INTO words (word) VALUES (%s)", (word,))
        db_connection.commit()

        return jsonify({"message": "Word added successfully"}), 200

    except Exception as e:
        print("Error adding word to database:", e)
        return jsonify({"error": "Failed to add word to database"}), 400


if __name__ == "__main__":
    app.run(debug=True)  # Enable debug mode for development
