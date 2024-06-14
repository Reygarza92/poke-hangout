from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/hint', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pokemon_name = request.form['pokemon_name']
        pokemon_data = get_pokemon_data(pokemon_name)
        if pokemon_data:
            return render_template('index.html', pokemon=pokemon_data, show_result=True)
        else:
            return render_template('index.html', pokemon_name=pokemon_name, not_found=True)
    return render_template('index.html')

def get_pokemon_data(pokemon_name):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}'
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

