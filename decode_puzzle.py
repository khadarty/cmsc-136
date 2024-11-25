import hashlib

def load_words(file_paths):
    """
    Load words from multiple text files and combine them into a single list.
    """
    words = set()  # Use a set to avoid duplicates
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            for line in f:
                words.add(line.strip())
    return list(words)

def load_hashes(file_path):
    """Load hashes from PUZZLE.txt into a list (to preserve order)."""
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def md5_hash(input_str):
    """Compute the MD5 hash of a given string."""
    return hashlib.md5(input_str.encode()).hexdigest()

def decode_message(number, words, hashes):
    """
    Decode the message by finding the word that matches each hash in PUZZLE.txt.
    """
    decoded_message = []

    # Iterate over each hash in the puzzle
    for puzzle_hash in hashes:
        for word in words:
            candidate = f"{number}{word}"  # Combine number and word
            candidate_hash = md5_hash(candidate)  # Compute hash
            if candidate_hash == puzzle_hash:
                decoded_message.append(word)  # Add the matching word to the message
                break
        else:
            # If no match is found for a hash, add a placeholder
            decoded_message.append("[UNKNOWN]")

    return decoded_message

if __name__ == "__main__":
    # File paths for word lists (add as many files as needed)
    word_files = [
        "freq.txt",
        "crosswd.txt",  # Replace with the actual file paths
        'single.txt',
        'words_to_try.txt',
        'acronyms.txt',
        'possible_misspellings.txt'
    ]
    hashes_file = "PUZZLE.txt"  # Path to PUZZLE.txt

    # The 9-digit number you found
    number = "294644421"

    # Load data
    words = load_words(word_files)  # Pass the list of word files
    hashes = load_hashes(hashes_file)

    # Decode the message
    message = decode_message(number, words, hashes)

    # Print the decoded message
    print("Decoded Message:")
    print(" ".join(message))
