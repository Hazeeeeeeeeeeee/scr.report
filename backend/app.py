from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import requests
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

player_cache = {}

raid_ids = {
    'Leviathan_Normal': 'jdzvzqvk?var-68kmerkl=4qy4j26q',
    'Leviathan_Prestige': 'jdzvzqvk?var-68kmerkl=mln3zvoq',
    'Eater_of_Worlds': '824r4ygd',
    'Spire_of_Stars': '9d8g973k',
    'Last_Wish_All_Encounters': '02qlzqpk?var-j84km3wn=8107wkol',
    'Last_Wish_Any%':'02qlzqpk?var-j84km3wn=9qjdxk7q',
    'Last_Wish_Trio_All_Encounters':'02qlzqpk?var-j84km3wn=810292jq',
    'Scourge_of_the_Past_No_Major_Glitches': 'mkernrnd?var-5ly7jpgl=mln32enq',
    'Scourge_of_the_Past_Any%': 'mkernrnd?var-5ly7jpgl=4qy467dq',
    'Crown_of_Sorrow': '8241elw2',
    'Garden_of_Salvation_Any%': '7dgng872?var-wl3d3gy8=4lxn3041',
    'Garden_of_Salvation_Trio': '7dgng872?var-wl3d3gy8=814z3kvl',
    'Deep_Stone_Crypt_Any%': 'zd3oymnd?var-789dj59n=zqo4dmx1',
    'Deep_Stone_Crypt_Trio':'zd3oymnd?var-789dj59n=013g3wxl',
    'Vault_of_Glass_Any%': 'q25x58vk?var-e8mqrmwn=jqzj7eml',
    'Vault_of_Glass_Trio': 'q25x58vk?var-e8mqrmwn=klrgw42q',
    'Vow_of_the_Disciple_Any%':'7kj909n2?var-gnx2yo48=q75vror1',
    'Vow_of_the_Disciple_Trio':'7kj909n2?var-gnx2yo48=1gnw26ol',
    'Kings_Fall': '9kvlp902?var-9l75odz8=192joekq',
    'Kings_Fall': '9kvlp902?var-9l75odz8=12v6yjkq',
    'Root_of_Nightmares_Any%': '9d88x6ld?var-jlzxvz78=lx5v72r1',
    'Root_of_Nightmares_Trio': '9d88x6ld?var-jlzxvz78=14o50mjq'
}

dungeon_strike_links = {'What Remains solo': 'kwj2rl09/n2yjrq12', 'What Remains duo': 'kwj2rl09/7kjzlvzd', 'What Remains fireteam': 'kwj2rl09/xk9j50gd', '//NODE.OVRD.AVALON// solo': 'y9mnzqzd/n2yjrq12', '//NODE.OVRD.AVALON// duo': 'y9mnzqzd/7kjzlvzd', '//NODE.OVRD.AVALON// fireteam': 'y9mnzqzd/xk9j50gd', 'The Shattered Throne (Dungeon) solo': '5wkpxnvd/n2yjrq12', 'The Shattered Throne (Dungeon) duo': '5wkpxnvd/7kjzlvzd', 'The Shattered Throne (Dungeon) fireteam': '5wkpxnvd/xk9j50gd', 'Pit of Heresy solo Current Patch': 'xd023px9/n2yjrq12?var-38dp43e8=5lmp96yl', 'Pit of Heresy duo Current Patch': 'xd023px9/7kjzlvzd?var-38dp43e8=5lmp96yl', 'Pit of Heresy fireteamCurrent Patch': 'xd023px9/xk9j50gd?var-38dp43e8=5lmp96yl', 'Pit of Heresy solo Pre 3.2.0': 'xd023px9/n2yjrq12?var-38dp43e8=81w9ko9l', 'Pit of Heresy duo Pre 3.2.0': 'xd023px9/7kjzlvzd?var-38dp43e8=81w9ko9l', 'Pit of Heresy fireteamPre 3.2.0': 'xd023px9/xk9j50gd?var-38dp43e8=81w9ko9l', 'Prophecy (Dungeon) solo': 'y9m13yz9/n2yjrq12', 'Prophecy (Dungeon) duo': 'y9m13yz9/7kjzlvzd', 'Prophecy (Dungeon) fireteam': 'y9m13yz9/xk9j50gd', 'Grasp of Avarice FT fireteam Any%': 'z98oorrd/xk9j50gd?var-68k51rz8=814mr7w1', 'Grasp of Avarice FT fireteam Shield Servitor Skip (PATCHED)': 'z98oorrd/xk9j50gd?var-68k51rz8=p12jg4vq', 'Grasp of Avarice Solo solo Post 6.3.0': 'z98oorrd/n2yjrq12?var-j84gjxy8=81w03zol', 'Grasp of Avarice Solo solo Pre 6.3.0': 'z98oorrd/n2yjrq12?var-j84gjxy8=z19e0djq', 'Grasp of Avarice Solo solo Shield Servitor Skip (PATCHED)': 'z98oorrd/n2yjrq12?var-j84gjxy8=81pkr6el', 'Grasp of Avarice Duo duo Post 6.3.0': 'z98oorrd/7kjzlvzd?var-wl39jxyl=zqovdkp1', 'Grasp of Avarice Duo duo Pre 6.3.0': 'z98oorrd/7kjzlvzd?var-wl39jxyl=81pk9ekl', 'Grasp of Avarice Duo duo Shield Servitor Skip (PATCHED)': 'z98oorrd/7kjzlvzd?var-wl39jxyl=xqkwvoyq', 'Duality Fireteam fireteam Post 6.3.0': '69z0546d/xk9j50gd?var-p855o008=jq6egjol', 'Duality duo': '69z0546d/7kjzlvzd', 'Duality solo': '69z0546d/n2yjrq12', 'Duality Fireteam fireteam Pre 6.3.0': '69z0546d/xk9j50gd?var-p855o008=9qj8e5o1', 'Spire of the Watcher (Dungeon) solo': '592yv57w/n2yjrq12', 'Spire of the Watcher (Dungeon) duo': '592yv57w/7kjzlvzd', 'Spire of the Watcher (Dungeon) fireteam': '592yv57w/xk9j50gd', 'The Arms Dealer Normal/GM fireteam Normal': 'ldyyjypd/xk9j50gd?var-wle97m48=gq7m3opq', 'The Arms Dealer Normal/GM fireteam GM': 'ldyyjypd/xk9j50gd?var-wle97m48=21gz066l', 'Arms Dealer Normal/GM solo Normal': 'ldyyjypd/n2yjrq12?var-ylpqyq68=klrr5rml', 'Arms Dealer Normal/GM solo GM': 'ldyyjypd/n2yjrq12?var-ylpqyq68=21dm2m51', 'The Arms Dealer 7.0.0.1 solo Pre 7.0.0.1': 'ldyyjypd/n2yjrq12?var-j84d4o28=qyzv95d1', 'The Arms Dealer 7.0.0.1 duo Pre 7.0.0.1': 'ldyyjypd/7kjzlvzd?var-j84d4o28=qyzv95d1', 'The Arms Dealer 7.0.0.1 fireteamPre 7.0.0.1': 'ldyyjypd/xk9j50gd?var-j84d4o28=qyzv95d1', 'The Arms Dealer 7.0.0.1 solo Post 7.0.0.1': 'ldyyjypd/n2yjrq12?var-j84d4o28=ln849dnl', 'The Arms Dealer 7.0.0.1 duo Post 7.0.0.1': 'ldyyjypd/7kjzlvzd?var-j84d4o28=ln849dnl', 'The Arms Dealer 7.0.0.1 fireteamPost 7.0.0.1': 'ldyyjypd/xk9j50gd?var-j84d4o28=ln849dnl', 'Lake of Shadows Patch FT fireteam Pre 7.0.0.1': 'nwllnlow/xk9j50gd?var-ylpqjz68=814w3ejl', 'Lake of Shadows Patch FT fireteam Post 7.0.0.1': 'nwllnlow/xk9j50gd?var-ylpqjz68=4lx63wrl', 'Lake of Shadows FT Normal/GM fireteam Normal': 'nwllnlow/xk9j50gd?var-jlzrmzq8=81pzvdnl', 'Lake of Shadows FT Normal/GM fireteam GM': 'nwllnlow/xk9j50g3od/xk9j50gd', 'Normal/Heroic solo Normal': '5wk8445w/n2yjrq12?var-dlo396dl=81p0kkeq', 'Normal/Heroic duo Normal': '5wk8445w/7kjzlvzd?var-dlo396dl=81p0kkeq', 'Normal/Heroic fireteamNormal': '5wk8445w/xk9j50gd?var-dlo396dl=81p0kkeq', 'Normal/Heroic solo Heroic': '5wk8445w/n2yjrq12?var-dlo396dl=xqk4ww9l', 'Normal/Heroic duo Heroic': '5wk8445w/7kjzlvzd?var-dlo396dl=xqk4ww9l', 'Normal/Heroic fireteamHeroic': '5wk8445w/xk9j50gd?var-dlo396dl=xqk4ww9l', "Savathun's Song (Strike, Unavailable) solo": 'gdregee9/n2yjrq12', "Savathun's Song (Strike, Unavailable) duo": 'gdregee9/7kjzlvzd', "Savathun's Song (Strike, Unavailable) fireteam": 'gdregee9/xk9j50gd', 'The Pyramidion (Strike, Unavailable) solo': 'z986e6rd/n2yjrq12', 'The Pyramidion (Strike, Unavailable) duo': 'z986e6rd/7kjzlvzd', 'The Pyramidion (Strike, Unavailable) fireteam': 'z986e6rd/xk9j50gd', 'A Garden World (Strike, Unavailable) solo': '29v3pmlw/n2yjrq12', 'A Garden World (Strike, Unavailable) duo': '29v3pmlw/7kjzlvzd', 'A Garden World (Strike, Unavailable) fireteam': '29v3pmlw/xk9j50gd', 'Tree of Probabilities (Strike, Unavailable) solo': '592zp039/n2yjrq12', 'Tree of Probabilities (Strike, Unavailable) duo': '592zp039/7kjzlvzd', 'Tree of Probabilities (Strike, Unavailable) fireteam': '592zp039/xk9j50gd', 'Strange Terrain (Strike, Unavailable) solo': 'rdq7v719/n2yjrq12', 'Strange Terrain (Strike, Unavailable) duo': 'rdq7v719/7kjzlvzd', 'Strange Terrain (Strike, Unavailable) fireteam': 'rdq7v719/xk9j50gd', 'Will of the Thousands (Strike, Unavailable) solo': '495505j9/n2yjrq12', 'Will of the Thousands (Strike, Unavailable) duo': '495505j9/7kjzlvzd', 'Will of the Thousands (Strike, Unavailable) fireteam': '495505j9/xk9j50gd', 'The Festering Core (Strike, Unavailable) solo': 'ldy5jppw/n2yjrq12', 'The Festering Core (Strike, Unavailable) duo': 'ldy5jppw/7kjzlvzd', 'The Festering Core (Strike, Unavailable) fireteam': 'ldy5jppw/xk9j50gd', 'The Hollowed Lair Normal/GM fireteam Normal': 'r9gx765w/xk9j50gd?var-dlo7qkd8=814687kq', 'The Hollowed Lair Normal/GM fireteam GM': 'r9gx765w/xk9j50gd?var-dlo7qkd8=p12krx21', 'Broodhold (Strike, Unavailable) solo': 'rdnlrp5w/n2yjrq12', 'Broodhold (Strike, Unavailable) duo': 'rdnlrp5w/7kjzlvzd', 'Broodhold (Strike, Unavailable) fireteam': 'rdnlrp5w/xk9j50gd'}

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
    app.run(port=5000)