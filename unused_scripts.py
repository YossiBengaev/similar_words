"""
from pygtrie import StringTrie
from collections import Counter
import time

app = Flask(__name__)

dictionary = set()  # This will store all the words added to the dictionary
request_counter = 0  # To count the number of requests made to /api/v1/similar
total_processing_time = 0  # To calculate the average processing time

trie = StringTrie()
with open("./words_dataset.txt", "r") as file:
    for word in file:
        trie[word] = True

@app.route("/api/v1/similar", methods=["GET"])
def sim():
    global request_counter
    global total_processing_time

    start_time = time.time()
"""

"""
with open('./words_dataset.txt', 'r') as file:
    words = file.readlines()
    for word in words:
        word = word.strip()  # Remove newline character
        # Insert word into the table
        cursor.execute("INSERT INTO words (word) VALUES (%s)", (word,))

"""
"""
@app.route("/", methods=["GET", "POST"])
def check_similarity():

    # Handles both GET and POST requests for the similarity check endpoint.
    # 
    # Returns:
    #     - A rendered template (GET request) with an empty form for user input.
    #     - A rendered template (POST request) displaying the similarity result and a form with pre-filled values.


    word1 = ""
    word2 = ""
    result = None  # Initialize result to avoid potential errors

    if request.method == "POST":
        # Extract user input from the POST request form
        word1 = request.form.get("word1")
        word2 = request.form.get("word2")

        if word1 and word2:  # Validate user input
            similar = Similarity()
            result = similar.are_similar(word1, word2)

    return render_template("index.html", word1=word1, word2=word2, result=result)
"""
"""
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    db_password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE")
)

cursor = db.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS words (id INT AUTO_INCREMENT PRIMARY KEY, word VARCHAR(255))")

with open("./words_dataset.txt", "r") as file:
    for line in file:
        word = line.strip()
        sorted_word = "".join(sorted(word))
        query = "INSERT INTO words (word, sorted_word) VALUES (%s, %s)"
        cursor.execute(query, (word, sorted_word))

db.commit()
cursor.close()
db.close()

print("Words inserted into the database successfully.")

import mysql.connector
"""

"""
!!!!!!!!!!!!!!!!!!!!!!! THIS IS WORKING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
import os
from flask import Flask, render_template, request, jsonify
from anagrams import find_anagrams
from mysql_connection import DatabaseConnection
from singleton_mysql_connection import MySQLConnection
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
mysql_connection = MySQLConnection()


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


@app.route("/home")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)  # Enable debug mode for development

"""