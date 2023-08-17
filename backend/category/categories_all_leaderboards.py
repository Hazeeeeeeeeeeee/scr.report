import srcomapi, srcomapi.datatypes as dt
from itertools import product

api = srcomapi.SpeedrunCom(); api.debug = 1

def get_subcategories_for_category(category_id):
    subcategories = {}
    variables_category = dt.Variable(api, data=api.get(f"categories/{category_id}/variables"))

    for variable in variables_category.data:
        if variable['is-subcategory']:
            subcategory_id = variable['id']
            subcategory_values = {details['label']: f"var-{subcategory_id}={value_id}" for value_id, details in variable['values']['values'].items()}
            subcategories[variable['name']] = subcategory_values
            print(subcategory_values)

    return subcategories

def build_category_urls(subcategories, game, category_id):
    subcategory_values = [list(values.items()) for values in subcategories.values()]
    urls_dict = {}
    for combination in product(*subcategory_values):
        query_string = "&".join([value_query for _, value_query in combination])
        descriptive_path = "_".join([name for name, _ in combination])
        url = f"{category_id}?{query_string}"
        urls_dict[descriptive_path] = url
    return urls_dict


def get_category_all_leaderboards(game_name, group_name):
    game = api.search(dt.Game, {"name": game_name})[0]
    for category in game.categories:
        if category.name == group_name:
            subcategories = get_subcategories_for_category(category.id)
            urls = build_category_urls(subcategories, game, category.id)
            return urls
