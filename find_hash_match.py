import hashlib
from itertools import product

def load_words(file_path):
    """Load words from freq.txt into a list."""
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def load_hashes(file_path):
    """Load hashes from PUZZLE.txt into a set for quick lookup."""
    with open(file_path, 'r') as f:
        return {line.strip() for line in f if line.strip()}

def md5_hash(input_str):
    """Compute the MD5 hash of a given string."""
    return hashlib.md5(input_str.encode()).hexdigest()

def find_combination(words, puzzle_hashes):
    """
    Brute-force all 9-digit numbers with words to find matches in puzzle_hashes.
    """
    for word in words:
        # Iterate over all possible 9-digit numbers
        for num in range(100000000, 1000000000):  # 9-digit numbers
            candidate = f"{num}{word}"  # Concatenate number and word
            candidate_hash = md5_hash(candidate)  # Compute hash
            if candidate_hash in puzzle_hashes:
                print(f"Match found: Number = {num}, Word = {word}, Hash = {candidate_hash}")
                return  # Stop after finding the first match
    print("No match found.")

if __name__ == "__main__":
    # File paths
    words_file = "freq.txt"  # Path to freq.txt
    hashes_file = "PUZZLE.txt"  # Path to PUZZLE.txt

    # Load data
    words = load_words(words_file)
    puzzle_hashes = load_hashes(hashes_file)

    # Find the combination
    find_combination(words, puzzle_hashes)
