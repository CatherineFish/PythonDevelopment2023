import random
from datetime import datetime
from typing import List
import argparse
import sys

def bullscows(guess: str, secret: str) -> (int, int):
	cow = 0
	bull = 0
	for i in range(min(len(guess), len(secret))):
		if guess[i] == secret[i]:
			bull += 1
		elif secret.find(guess[i]) != -1:
			cow += 1
	i += 1
	for j in range(i, len(guess)):
		if secret.find(guess[j]):
			cow += 1
	return (bull, cow)


def gameplay(ask: callable, inform: callable, words: List[str]) -> int:
	random.seed() #надо ли инициализировать временем? если нет, убрать импорт
	secret_word = words[random.randint(0, len(words))]
	print(secret_word)
	guess_word = ""
	tries = 0
	while(secret_word != guess_word):
		guess_word = ask("Введите слово: ", words)
		b, c = bullscows(guess_word, secret_word)
		inform("Быки: {}, Коровы: {}", b, c)
		tries += 1
	return 	tries


def ask(prompt: str, valid: List[str] = None) -> str:
	print(str)
	printed_word = input()
	if (valid != None and printed_word not in valid):
		pritn(str)
	return printed_word

def inform(format_string: str, bulls: int, cows: int) -> None:
	print(format_string.format(bulls, cows))

parser = argparse.ArgumentParser(
    description="Bulls and Cows",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

parser.add_argument(
    "dictionary", action="store", help="Dictionary file or URL"
)

parser.add_argument(
    "len_of_word", action="store", default="5", help="Lenght of secret words", nargs="?", type=int
)



if __name__ == "__main__":
	args = parser.parse_args(sys.argv[1:])
	print(args)

