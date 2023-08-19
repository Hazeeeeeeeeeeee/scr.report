from itertools import product
import requests

def get_levels_all_leaderboards(level_id):
    print(f"Loading level leaderboard for id: {level_id}")
    level_request = requests.get(f"https://www.speedrun.com/api/v1/levels/{level_id}/categories?embed=variables")
    print(f"Request to: https://www.speedrun.com/api/v1/levels/{level_id}/categories?embed=variables")
    level_data = level_request.json()['data']

    urls_dict = {}
    for level_type in level_data:
        category_id = level_type['id']
        level_category_name = level_type['name']
        subcategories = []
        if 'variables' in level_type:
            for variable in level_type['variables']['data']:
                if variable['is-subcategory']:
                    subcategory_id = variable['id']
                    subcategories.append((subcategory_id, variable['values']['values']))

            for combination in product(*[choices.items() for _, choices in subcategories]):
                            query_parts = []
                            for (subcategory_id, _), (choice_id, choice_info) in zip(subcategories, combination):
                                query_parts.append(f"var-{subcategory_id}={choice_id}")
                            query_string = "&".join(query_parts)
                            descriptive_path = f"{level_category_name}_{'_'.join([choice['label'] for _, choice in combination])}"
                            url = f"{level_id}/{category_id}?{query_string}"
                            urls_dict[descriptive_path] = url
    return urls_dict