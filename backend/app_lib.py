from flask import Flask, jsonify
from flask_cors import CORS
from category.categories_all_leaderboards import get_category_all_leaderboards
from level.levels_all_leaderboards import get_levels_all_leaderboards
import requests

app = Flask(__name__)
CORS(app)

@app.route('/v2/<string:game_id>/all', methods=['GET'])
def get_all_runs(game_id):
    
    # Fetch levels using the provided endpoint
    print(f"Loading categories and levels for id: {game_id}")
    levels_response = requests.get(f"https://www.speedrun.com/api/v1/games/{game_id}/levels")
    print(f"Request to: https://www.speedrun.com/api/v1/games/{game_id}/levels")
    levels_data = levels_response.json()
    
    # Fetch categories using the provided endpoint
    categories_response = requests.get(f"https://www.speedrun.com/api/v1/games/{game_id}/categories")
    print(f"Request to: https://www.speedrun.com/api/v1/games/{game_id}/categories")
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
        # Fetching the variables for the category
        variables_url = f"https://www.speedrun.com/api/v1/categories/{ref_name}/variables"
        print("Fetching:", variables_url)
        variables_request = requests.get(variables_url)
        variables_data = variables_request.json()

        # Fetching the category details to get the category name
        category_details_url = f"https://www.speedrun.com/api/v1/categories/{ref_name}"
        category_details_request = requests.get(category_details_url)
        category_details_data = category_details_request.json()
        category_name = category_details_data['data']['name']

        # Constructing the URL with query parameters for each variable's default value
        query_parameters = []
        for variable in variables_data['data']:
            if variable['is-subcategory']:
                variable_id = variable['id']
                default_value = variable['values']['default']
                query_parameters.append(f"var-{variable_id}={default_value}")

        query_string = "&".join(query_parameters)
        leaderboard_url = f"https://www.speedrun.com/api/v1/leaderboards/{game_id}/category/{ref_name}?{query_string}"
        print("Fetching:", leaderboard_url)
        leaderboard_request = requests.get(leaderboard_url)
        leaderboard_data = leaderboard_request.json()

        # Combining the default leaderboard data with the variable details
        combined_data = {
            "default_leaderboard": leaderboard_data,
            "variable_details": variables_data['data'],
            "category_name": category_name
        }
        return jsonify(combined_data)



    elif group_type == "level":
        level_leaderboard_url = f"https://www.speedrun.com/api/v1/leaderboards/{game_id}/level/{ref_name}"
        print("Fetching:", level_leaderboard_url)
        leaderboard_request = requests.get(level_leaderboard_url)
        leaderboard_data = leaderboard_request.json()
        return jsonify(leaderboard_data)
    
    return jsonify({"error": "Invalid group type provided"}), 400



if __name__ == '__main__':
    app.run(debug=True)