from flask import Flask, jsonify
import srcomapi, srcomapi.datatypes as dt
from category.categories_all_leaderboards import get_category_all_leaderboards
from level.levels_all_leaderboards import get_levels_all_leaderboards


app = Flask(__name__)
api = srcomapi.SpeedrunCom()

SUPPORTED_GAMES = ["Destiny 2", "Destiny 2 Story", "Destiny 2 Lost Sectors", "Destiny 2 Content Vault"]

def normalize_game_name(game_name):
    return game_name.replace(" ", "").lower()

def get_supported_game(game_name):
    normalized_game_name = normalize_game_name(game_name)
    for supported_game in SUPPORTED_GAMES:
        if normalize_game_name(supported_game) == normalized_game_name:
            games = api.search(dt.Game, {"name": supported_game})
            if games:
                return games[0]
    return None

@app.route('/v2/<string:game_name>', methods=['GET'])
def get_game(game_name):
    game = get_supported_game(game_name)
    if game:
        return jsonify({
            "name": game.name,
            "id": game.id,
            "categories": [category.name for category in game.categories]
        })
    return jsonify({"error": "Game not supported"}), 404


@app.route('/v2/<string:game_name>/all', methods=['GET'])
def get_all_runs(game_name):
    game = get_supported_game(game_name)
    if game:
        levels = [{"Level Name": level.name, "Level ID": level.id} for level in game.levels]
        categories = [{"Category Name": category.name, "Category ID": category.id} for category in game.categories]

        response = {
            "Levels": levels,
            "Categories": categories
        }

        return jsonify(response)
    return jsonify({"error": "Game not supported"}), 404


api = srcomapi.SpeedrunCom(); api.debug = 1
def is_category(game, group_name):
    for category in game.categories:
        if category.name == group_name:
            return True
    return False
      

@app.route('/v2/<string:game_name>/leaderboards_all/<string:group_name>', methods=['GET'])
def get_all_leaderboard(game_name, group_name):
    game = api.search(dt.Game, {"name": game_name})[0]
    
    if is_category(game, group_name):
        # Handle category logic
        urls = get_category_all_leaderboards(game_name, group_name)
        return jsonify(urls)
    else:
        urls = get_levels_all_leaderboards(game_name, group_name)
        return jsonify(urls)

@app.route('/v2/<string:game_name>/leaderboard/<string:group_name>/ref/<string:ref_name>', methods=['GET'])
def get_precise_leaderboard(game_name, group_name, ref_name):
    game = api.search(dt.Game, {"name": game_name})[0]

    if is_category(game, group_name):

        urls = get_category_all_leaderboards(game_name, group_name)
        print (jsonify(urls))
        leaderboard_url_part = urls.get(ref_name)
       # if leaderboard_url_part:
       #     full_url = f"leaderboards/{game.id}/category/{leaderboard_url_part}"
       #     leaderboard_data = dt.Leaderboard(api, data=api.get(full_url))
       #     return jsonify({"leaderboard": leaderboard_data})
       # else:
       #     return jsonify({"error": "Leaderboard not found"}), 404
    else:
        urls = get_levels_all_leaderboards(game_name, group_name)
        leaderboard_url_part = urls.get(ref_name)
        if leaderboard_url_part:
            full_url = f"leaderboards/{game.id}/level/{leaderboard_url_part}"
            leaderboard_data = dt.Leaderboard(api, data=api.get(full_url))
            return jsonify({"leaderboard": leaderboard_data})
        else:
            return jsonify({"error": "Leaderboard not found"}), 404












if __name__ == '__main__':
    app.run(debug=True)



['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_api', '_repr', '_retrieved', 'data', 'embeds', 'endpoint', 'id', 'links', 'miscellaneous', 'name', 'players', 'records', 'rules', 'type', 'variables', 'weblink']   
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_api', '_repr', '_retrieved', 'data', 'embeds', 'endpoint', 'id', 'links', 'name', 'rules', 'weblink']