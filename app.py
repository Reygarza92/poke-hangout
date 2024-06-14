from flask import Flask, render_template, request, redirect, url_for
import requests
import random

app = Flask(__name__, static_folder='static')

# Función para obtener una palabra aleatoria de la PokeAPI
def get_random_pokemon_name():
    response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1000")
    pokemon_data = response.json()
    random_pokemon = random.choice(pokemon_data["results"])
    return random_pokemon["name"]

# Inicialización de variables
word_to_guess = get_random_pokemon_name()
guessed_word = ["_"] * len(word_to_guess)
attempts_left = 6  # Número de intentos permitidos

# Ruta principal para el juego del ahorcado
@app.route('/')
def hangman():
    return render_template('hangman.html', guessed_word=guessed_word, attempts_left=attempts_left)

# Ruta para manejar las letras adivinadas
@app.route('/guess', methods=['POST'])
def guess():
    global word_to_guess, guessed_word, attempts_left
    if request.method == 'POST':
        letter = request.form['letter'].lower()

        if letter.isalpha() and letter not in guessed_word:
            if letter in word_to_guess:
                for i in range(len(word_to_guess)):
                    if word_to_guess[i] == letter:
                        guessed_word[i] = letter
            else:
                attempts_left -= 1
                
        # Verificar si se ha adivinado la palabra o si se han agotado los intentos
        if "_" not in guessed_word or attempts_left == 0:
            return redirect(url_for('game_over'))

        # Obtener la pista del Pokémon
        pokemon_data = get_pokemon_data(word_to_guess)
        return render_template('hangman.html', guessed_word=guessed_word, attempts_left=attempts_left, pokemon_data=pokemon_data)

    return redirect(url_for('hangman'))

# Ruta para reiniciar el juego
@app.route('/reset')
def reset_game():
    global word_to_guess, guessed_word, attempts_left
    word_to_guess = get_random_pokemon_name()
    guessed_word = ["_"] * len(word_to_guess)
    attempts_left = 6
    return redirect(url_for('hangman'))

# Ruta para la pantalla de game over
@app.route('/game-over')
def game_over():
    global word_to_guess, guessed_word, attempts_left
    if guessed_word == list(word_to_guess):
        return redirect(f'https://www.wikidex.net/wiki/{word_to_guess.lower()}')
    else:
        return render_template('game_over.html', word_to_guess=word_to_guess, guessed_word=guessed_word)

# Ruta para obtener los datos de un Pokémon para la pista
@app.route('/hint', methods=['POST'])
def get_hint():
    global word_to_guess, guessed_word, attempts_left
    pokemon_data = get_pokemon_data(word_to_guess)
    if pokemon_data:
        attempts_left-=3
        return render_template('hangman.html', guessed_word=guessed_word, attempts_left=attempts_left, pokemon_data=pokemon_data)
    else:
        return "No se pudo encontrar información del Pokémon."

def get_pokemon_data(word_to_guess):
    url = f'https://pokeapi.co/api/v2/pokemon/{word_to_guess.lower()}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        pokemon_data = {
            'name': data['name'],
            'id': data['id'],
            'height': data['height'],
            'weight': data['weight'],
            'types': [t['type']['name'] for t in data['types']],
            'image': data['sprites']['front_default']
        }
        return pokemon_data
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)

