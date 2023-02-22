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

