from flask import Flask, jsonify
from flask_cors import CORS
import srcomapi, srcomapi.datatypes as dt
from category.categories_all_leaderboards import get_category_all_leaderboards
from level.levels_all_leaderboards import get_levels_all_leaderboards
import requests

app = Flask(__name__)
CORS(app)

@app.route('/v2/<string:game_id>/all', methods=['GET'])
def get_all_runs(game_id):
    print(game_id)
    
    # Fetch levels using the provided endpoint
    levels_response = requests.get(f"https://www.speedrun.com/api/v1/games/{game_id}/levels")
    levels_data = levels_response.json()
    
    # Fetch categories using the provided endpoint
    categories_response = requests.get(f"https://www.speedrun.com/api/v1/games/{game_id}/categories")
    categories_data = categories_response.json()
    
    if 'data' in levels_data and 'data' in categories_data:
        levels = [
            {
                "Level Name": level['name'], 
                "Level ID": level['id']
            } 
            for level in levels_data['data'] 
            if any(link['rel'] == 'leaderboard' for link in level.get('links', []))
        ]
        
        categories = [
            {
                "Category Name": category['name'], 
                "Category ID": category['id']
            } 
            for category in categories_data['data'] 
            if any(link['rel'] == 'leaderboard' for link in category.get('links', []))
        ]

        response_data = {
            "Levels": levels,
            "Categories": categories
        }

        print(response_data)
        return jsonify(response_data)
    return jsonify({"error": "Data not found"}), 404      


@app.route('/v2/<string:game_id>/all_leaderboards/<string:group_type>/<string:group_id>', methods=['GET'])
def get_all_leaderboard(game_id, group_type, group_id):
    
    if group_type.lower() == "category":
        # Handle category logic
        print("hi")
        ref_names = get_category_all_leaderboards(group_id)
        return jsonify(ref_names)
    elif group_type.lower() == "level":
        ref_names = get_levels_all_leaderboards(group_id)
        return jsonify(ref_names)
    else:
        return jsonify({"error": "Invalid group type provided"}), 400


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


if __name__ == '__main__':
    app.run(debug=True)
