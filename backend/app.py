from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import requests
import json
from raid_ids import raid_ids
#from mission_ids import mission_ids


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

player_cache = {}

@app.route('/raid/<raid_name>')
def raid(raid_name):
    print(f"raid name: {raid_name}")
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

@app.route('/mission/<mission_name>/<mission_type>')
def mission(mission_name, mission_type):
    mission = mission_ids.get(mission_name)
    print(f"mission name: {mission_name}")

    if not mission:
        return jsonify({'error': 'Invalid mission name'}), 400

    mission_id = mission.get(mission_type)
    if not mission_id:
        return jsonify({'error': 'Invalid mission type'}), 400
    ...

    response = requests.get(f'https://www.speedrun.com/api/v1/leaderboards/yd4or2x1/level/{mission_id}')

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

@app.route('/donjon/<name>')
def get_dungeon_or_mission(name):
    base_path = 'https://www.speedrun.com/api/v1/leaderboards/4d7y5zd7/level/'
    path = base_path + dungeon_strike_links[name]

    response = requests.get(path)
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
    duration = duration[2:]
    hours, minutes, seconds = 0, 0, 0
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
    if hours > 0:
        return f'{hours}:{minutes:02d}:{seconds:02d}'
    else:
        return f'{minutes:02d}:{seconds:02d}'
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

