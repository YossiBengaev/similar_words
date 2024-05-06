"""
Good for 2 words not for all the words in the dataset
"""


class Similarity:

    #  This class provides a method to check if two words are similar (letter permutations).
  def are_similar(self, word1, word2):
    """
    This function checks if two words are similar, meaning they are letter permutations of each other.

    Args:
        word1: The first word to compare.
        word2: The second word to compare.

    Returns:
        True if the words are similar, False otherwise.
    """
    if len(word1) != len(word2):
        return False
    # Create a dictionary to store the frequency of each character in word1
    char_count = {}
    for char in word1:
        char_count[char] = char_count.get(char, 0) + 1

    # Iterate through word2 and check if each character exists in the dictionary with a non-zero count
    for char in word2:
      if char not in char_count or char_count[char] == 0:
        return False
      char_count[char] -= 1

    return True