import srcomapi, srcomapi.datatypes as dt
from itertools import product

api = srcomapi.SpeedrunCom(); api.debug = 1

def get_subcategories(level):
    subcategories = {}
    level_id = level.id
    variables_level = dt.Variable(api, data=api.get(f"levels/{level_id}/variables"))

    for variable in variables_level.data:
        if variable['is-subcategory']:
            subcategory_id = variable['id']
            subcategory_values = {details['label']: f"var-{subcategory_id}={value_id}" for value_id, details in variable['values']['values'].items()}
            subcategories[variable['name']] = subcategory_values
            print(subcategory_values)

    return subcategories

def get_categories(level):
    level_id = level.id
    categories_level = dt.Category(api, data=api.get(f"levels/{level_id}/categories"))
    print(categories_level)
    return [(category['name'], category['id']) for category in categories_level.data]

def build_level_urls(subcategories, categories, game, level):
    subcategory_values = [list(values.items()) for values in subcategories.values()]
    urls_dict = {}
    for combination in product(*subcategory_values):
        query_parts = [f"{name}({value_query})" for name, value_query in combination]
        query_string = "&".join([value_query for _, value_query in combination])
        descriptive_path = "_".join([name for name, _ in combination])
        for category_name, category_id in categories:
            url = f"{level.id}/{category_id}?{query_string}"
            urls_dict[f"{category_name}_{descriptive_path}"] = url
    return urls_dict



def get_levels_all_leaderboards(game_name, level_name):
    game = api.search(dt.Game, {"name": game_name})[0]
    for level in game.levels:
        if level.name == level_name:
            subcategories = get_subcategories(level)
            categories = get_categories(level)
            urls = build_level_urls(subcategories, categories, game, level)
            return urls
