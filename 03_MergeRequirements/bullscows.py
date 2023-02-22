import random
from datetime import datetime


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


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
	random.seed() #надо ли инициализировать временем? если нет, убрать импорт
	secret_word = words[random.randint(0, len(words))]
	print(secret_word)
	guess_word = ""
	tries = 0
	while(secret_word != guess_word):
		ask("Введите слово: ", words)
		inform("Быки: {}, Коровы: {}", b, c)
		tries += 1
	return 	tries

