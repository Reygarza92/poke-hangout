import requests
import random

def get_pokemon():
    response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=1000')
    pokemon = random.choice(response.json()['results'])
    return pokemon['name']

def hangman(word):
    word = list(word)
    guessed_letters = ['_' for _ in word]
    attempts = 6

    while attempts > 0 and '_' in guessed_letters:
        print(' '.join(guessed_letters))
        print(f'Attempts left: {attempts}')

        guess = input('Guess a letter: ').lower()

        if guess in word:
            for i, letter in enumerate(word):
                if letter == guess:
                    guessed_letters[i] = guess
        else:
            attempts -= 1

    if '_' not in guessed_letters:
        print('Felicidades!!! ' + ''.join(word))
    else:
        print('Perdiste, el pokemon era ' + ''.join(word))

def main():
    pokemon = get_pokemon()
    hangman(pokemon)

if __name__ == "__main__":
    main()
