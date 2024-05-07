def find_permutation(db_connection, word):
    # Generate the sorted version of the input word
    sorted_word = ''.join(sorted(word))
    # Selected the words by it is sorted word.
    query = "SELECT word FROM words WHERE sorted_word = %s AND word != %s"

    # Execute the query with the sorted_word and the input word as parameters
    db_connection.execute(query, (sorted_word, word))

    # Fetch the matching words
    permutation = [row[0] for row in db_connection.fetchall()]
    print("Found permutation:", permutation)
    return permutation

