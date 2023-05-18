from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import requests
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

player_cache = {}

raid_ids = {
    'Leviathan': 'jdzvzqvk',
    'Eater_of_Worlds': '824r4ygd',
    'Spire_of_Stars': '9d8g973k',
    'Last_Wish': '02qlzqpk?var-8107wkol=1',
    'Scourge_of_the_Past': 'mkernrnd',
    'Crown_of_Sorrow': '8241elw2',
    'Garden_of_Salvation': '7dgng872',
    'Deep_Stone_Crypt': 'zd3oymnd',
    'Vault_of_Glass': 'q25x58vk',
    'Vow_of_the_Disciple':' 7kj909n2',
    'Kings_Fall': '9kvlp902',
    'Root_of_Nightmares': '9d88x6ld'
}

@app.route('/raid/<raid_name>')
@cross_origin()
def raid(raid_name):
    raid_id = raid_ids.get(raid_name)
    if not raid_id:
        return jsonify({'error': 'Invalid raid name'}), 400

    response = requests.get(f'https://www.speedrun.com/api/v1/leaderboards/4d7y5zd7/category/{raid_id}')

    data = json.loads(response.text)

    leaderboard = []
    for i, run in enumerate(data['data']['runs'], start=1):
        player_names = [get_player_name(player) for player in run['run']['players']]

        run_time = format_duration(run['run']['times']['primary'])

        leaderboard.append({
            'rank': i,
            'players': player_names,
            'time': run_time
        })


    return jsonify(leaderboard)

def get_player_name(player):
    if player['rel'] == 'user':
        player_id = player['id']
        if player_id in player_cache:
            return player_cache[player_id]

        response = requests.get(f'https://www.speedrun.com/api/v1/users/{player_id}')

        data = json.loads(response.text)

        if 'data' not in data or 'names' not in data['data'] or 'international' not in data['data']['names']:
            print(f"Error: Unable to get player name for player_id: {player_id}")
            return "Unknown Player"

        player_name = data['data']['names']['international']

        player_cache[player_id] = player_name

        return player_name
    elif player['rel'] == 'guest':
        return player['name']



def format_duration(duration):
    # Remove the 'PT' prefix
    duration = duration[2:]

    hours, minutes, seconds = 0, 0, 0

    # Split the duration into its components
    time_parts = duration.split('H')
    if len(time_parts) > 1:
        hours = int(time_parts[0])
        duration = time_parts[1]

    time_parts = duration.split('M')
    if len(time_parts) > 1:
        minutes = int(time_parts[0])
        duration = time_parts[1]

    time_parts = duration.split('S')
    if len(time_parts) > 1:
        seconds = int(time_parts[0])

    # Format the duration as a string
    if hours > 0:
        return f'{hours}:{minutes:02d}:{seconds:02d}'
    else:
        return f'{minutes:02d}:{seconds:02d}'


if __name__ == '__main__':
    app.run(port=5000)
