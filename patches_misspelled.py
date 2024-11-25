import string

def generate_edit_distance_two(word):
    """
    Generate all possible words with an edit distance of 2 from the given word.
    
    Args:
        word (str): The original word.
    
    Returns:
        set: A set of words with an edit distance of 2.
    """
    def edits_one(word):
        """Generate all words with an edit distance of 1."""
        letters = string.ascii_lowercase
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]  # Remove one character
        inserts = [L + c + R for L, R in splits for c in letters]  # Add one character
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]  # Replace one character
        return set(deletes + inserts + replaces)
    
    # Generate all edit distance 1 words
    edit_one = edits_one(word)
    # Generate all edit distance 2 words by applying edits_one again
    edit_two = set(e2 for e1 in edit_one for e2 in edits_one(e1))
    return edit_two

def save_to_file(words, file_path):
    """
    Save a set of words to a text file, one word per line.
    
    Args:
        words (set): The set of words to save.
        file_path (str): The path to the output file.
    """
    with open(file_path, 'w') as f:
        for word in sorted(words):  # Sort the words for easier reading
            f.write(f"{word}\n")
    print(f"Saved {len(words)} words to {file_path}")

if __name__ == "__main__":
    # The original word
    original_word = "patches"

    # Generate edit distance 2 words
    edit_distance_two_words = generate_edit_distance_two(original_word)

    # Output file path
    output_file = "possible_misspellings.txt"

    # Save the results to a file
    save_to_file(edit_distance_two_words, output_file)
