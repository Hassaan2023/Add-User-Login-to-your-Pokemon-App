import requests as r

def get_pokemon(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}/"
    response = r.get(url)
    
    if response.ok:
        data = response.json()
        pokemon_name = data['name']
        ability_name = data['abilities'][0]['ability']['name']
        base_experience = data['base_experience']
        front_shiny = data['sprites']['front_shiny']

        output = {
            'pokemon_name': pokemon_name,
            'ability_name': ability_name,
            'base_experience': base_experience,
            'front_shiny' : front_shiny
        } 
        
        return output
    else:
        return None