from flask import Flask, jsonify
from flask_cors import CORS
import srcomapi, srcomapi.datatypes as dt
from category.categories_all_leaderboards import get_category_all_leaderboards
from level.levels_all_leaderboards import get_levels_all_leaderboards


app = Flask(__name__)
CORS(app)
api = srcomapi.SpeedrunCom()

SUPPORTED_GAMES = ["Destiny 2", "Destiny 2 Story", "Destiny 2 Lost Sectors"]

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
        
        # Filter out categories without leaderboards
        categories = []
        for category in game.categories:
            if category.weblink != game.weblink:
                categories.append({
                    "Category Name": category.name,
                    "Category ID": category.id
                })

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
      

@app.route('/v2/<string:game_name>/all_leaderboards/<string:group_name>', methods=['GET'])
def get_all_leaderboard(game_name, group_name):
    game = api.search(dt.Game, {"name": game_name})[0]
    
    if is_category(game, group_name):
        # Handle category logic
        ref_names = get_category_all_leaderboards(game_name, group_name)
        return jsonify(ref_names)
    else:
        ref_names = get_levels_all_leaderboards(game_name, group_name)
        return jsonify(ref_names)

@app.route('/v2/<string:game_name>/leaderboard/<string:group_name>/ref/<string:ref_name>', methods=['GET'])
def get_leaderboard(game_name, group_name, ref_name):
    game =  api.search(dt.Game, {"name": game_name})[0]
    game_id = api.search(dt.Game, {"name": game_name})[0].id

    # Determine if it's a category or level
    if is_category(game, group_name):
        ref_names = get_category_all_leaderboards(game_name, group_name)
    else:
        ref_names = get_levels_all_leaderboards(game_name, group_name)

    # Use the ref_name to look up the corresponding URL
    constructed_url = ref_names.get(ref_name)
    if not constructed_url:
        return jsonify({"error": "Invalid ref_name provided"}), 400

    # Fetch the leaderboard based on whether it's a level or category
    if is_category(game, group_name):
        response = api.get(f"leaderboards/{game_id}/category/{constructed_url}")
    else:
        response = api.get(f"leaderboards/{game_id}/level/{constructed_url}")
    
    return response




if __name__ == "__main__":
    app.run(debug=True)
