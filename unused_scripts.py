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