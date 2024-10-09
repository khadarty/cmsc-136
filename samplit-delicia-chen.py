import argparse
import random

def random_samples(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            random_number = random.randint(1, 100)
            if random_number == 1:
                print(line, end='')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    random_samples(args.filename)