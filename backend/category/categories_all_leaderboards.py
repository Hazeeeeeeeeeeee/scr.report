from itertools import product
import requests

def get_category_all_leaderboards(category_id):
    print(f"Loading category leaderboard for id: {category_id}")
    category_request = requests.get(f"https://www.speedrun.com/api/v1/categories/{category_id}/variables")
    print(f"Request to: https://www.speedrun.com/api/v1/categories/{category_id}/variables")
    category_data = category_request.json()['data']

    subcategories = {}
    for category_type in category_data:
        if category_type['is-subcategory']:
            subcategory_id = category_type['id']
            categories_inType = {value['label']: f"var-{subcategory_id}={id}" for id, value in category_type['values']['values'].items()}
            subcategories[category_type['name']] = categories_inType

    subcategory_values = [list(values.items()) for values in subcategories.values()]
    urls_dict = {}
    for combination in product(*subcategory_values):
        query_string = "&".join([value_query for _, value_query in combination])
        descriptive_path = "_".join([name for name, _ in combination])
        url = f"{category_id}?{query_string}"
        urls_dict[descriptive_path] = url

    return urls_dict
