import hashlib
from itertools import permutations


with open("PUZZLE", "r") as f:
    puzzle_hashes = [line.strip() for line in f]


with open("/usr/share/dict/words", "r") as f:
    words = [word.strip() for word in f]

nine_digit_numbers = [str(i).zfill(9) for i in range(10**9)]


def md5_hash(input_str):
    return hashlib.md5(input_str.encode()).hexdigest()

# Iterate through numbers and word combinations
for num in nine_digit_numbers:
    for word_combo in permutations(words, 3):  # Adjust number of words based on puzzle.py
        candidate = num + "".join(word_combo)
        hash_result = md5_hash(candidate)
        if hash_result in puzzle_hashes:
            print(f"Match found: {candidate}")
            break
