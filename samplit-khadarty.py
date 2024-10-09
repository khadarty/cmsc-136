import random
import argparse

#random returns a random number between 0 and 1
def samplit(filename):
	with open(filename, 'r', encoding = 'utf-8') as file:
		for line in file:
			if random.randint(1,100) == 1 :
				print(line, end = '')

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('filename')
	args = parser.parse_args()

samplit(args.filename)
