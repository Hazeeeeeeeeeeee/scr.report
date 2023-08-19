from flask import Flask, jsonify
from flask_cors import CORS
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
        ref_names = get_category_all_leaderboards(group_id)
        return jsonify(ref_names)
    elif group_type.lower() == "level":
        ref_names = get_levels_all_leaderboards(group_id)
        return jsonify(ref_names)
    else:
        return jsonify({"error": "Invalid group type provided"}), 400


@app.route('/v2/<string:game_id>/leaderboard/<string:group_type>/<string:ref_name>', methods=['GET'])
def get_leaderboard(game_id, group_type, ref_name):
    if group_type == "category":
        leaderboard_request = requests.get(f"https://www.speedrun.com/api/v1/leaderboards/{game_id}/category/{ref_name}")
        leaderboard_data = leaderboard_request.json()
        return leaderboard_data
    elif group_type == "level":
        leaderboard_request = requests.get(f"https://www.speedrun.com/api/v1/leaderboards/{game_id}/level/{ref_name}")
        leaderboard_data = leaderboard_request.json()
        return leaderboard_data
    
    return jsonify({"error": "Invalid group type provided"}), 400


if __name__ == '__main__':
    app.run(debug=True)