from itertools import permutations


def find_anagrams(db_connection, word):
    # Generate all permutations of the characters in the word
    word_permutations = [''.join(p) for p in permutations(word)]

    # Create the SQL query dynamically
    query = "SELECT word FROM words WHERE word IN (%s)" % ','.join(['%s'] * len(word_permutations))

    # Exclude the input word from the query
    query += " AND word != %s"

    # Execute the query with the permutations as parameters
    db_connection.execute(query, tuple(word_permutations + [word]))

    # Fetch the matching words
    anagrams = [row[0] for row in db_connection.fetchall()]
    print("Found anagrams:", anagrams)
    return anagrams

