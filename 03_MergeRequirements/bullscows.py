import random
from typing import List
import argparse
import sys
import urllib.request
import urllib.error
import cowsay
from io import StringIO


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
	secret_word = words[random.randint(0, len(words) - 1)]
	guess_word = ""
	tries = 0
	while(secret_word != guess_word):
		guess_word = ask("Введите слово: ", words)
		b, c = bullscows(guess_word, secret_word)
		inform("Быки: {}, Коровы: {}", b, c)
		tries += 1
	return 	tries


def ask(prompt: str, valid: List[str] = None) -> str:
	print(cowsay.cowsay(
            prompt,
            cowfile=cow_for_print
    	  )
	)
	printed_word = input()
	while (valid != None and printed_word not in valid):
		print(cowsay.cowsay(
        		prompt,
            	cowfile=cow_for_print
    		  )
		)
		printed_word = input()
	return printed_word

def inform(format_string: str, bulls: int, cows: int) -> None:
	print(cowsay.cowsay(
            format_string.format(bulls, cows),
            cowfile=cow_for_print
    	  )
	)

parser = argparse.ArgumentParser(
    description="Bulls and Cows",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

parser.add_argument(
    "dictionary", action="store", help="Dictionary file or URL"
)

parser.add_argument(
    "len", action="store", default="5", help="Lenght of secret words", nargs="?", type=int
)

cow_for_print = cowsay.read_dot_cow(StringIO("""
$the_cow = <<EOC;
         $thoughts
          $thoughts
           $thoughts
             .--.
            |o_o |
            |:_/ |
             .  .      _______
             |  |     |  _____|
             |  |     |  |   ()
             |  |_____|  |   **
             (           |
             (___________|
EOC
"""))


if __name__ == "__main__":
	args = parser.parse_args(sys.argv[1:])
	my_dict = list()
	try:
		with urllib.request.urlopen(args.dictionary) as f:
			my_dict = f.read().decode('utf-8').split()
	except Exception as e1:
		try:
			with open(args.dictionary, "r") as f:
				my_dict = f.read().split()
		except Exception as e2:
			print("Error as URL:\n",  e1)
			print("Error as file:\n", e2)
	my_dict = list(filter(lambda x: len(x) == args.len, my_dict))
	print("Number of attempts:", gameplay(ask, inform, my_dict))