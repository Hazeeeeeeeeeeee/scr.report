import srcomapi, srcomapi.datatypes as dt
from itertools import product

api = srcomapi.SpeedrunCom(); api.debug = 1

def build_level_urls(level):
    level_id = level.id
    all_information = dt.Variable(api, data=api.get(f"levels/{level_id}/categories?embed=variables"))
    
    urls_dict = {}

    # Loop through each category (Solo, Duo, Fireteam)
    for category_info in all_information.data:
        category_name = category_info['name']
        category_id = category_info['id']

        # Check if the category has variables (subcategories)
        if 'variables' in category_info:
            subcategories = []
            
            for variable in category_info['variables']['data']:
                if variable['is-subcategory']:
                    subcategory_id = variable['id']
                    choices = variable['values']['values']
                    subcategories.append((subcategory_id, choices))

            # Generate combinations of choices across all subcategories
            for combination in product(*[choices.items() for _, choices in subcategories]):
                query_parts = []
                for (subcategory_id, _), (choice_id, choice_info) in zip(subcategories, combination):
                    query_parts.append(f"var-{subcategory_id}={choice_id}")
                query_string = "&".join(query_parts)
                descriptive_path = f"{category_name}_{'_'.join([choice['label'] for _, choice in combination])}"
                url = f"{level.id}/{category_id}?{query_string}"
                urls_dict[descriptive_path] = url

    return urls_dict


def get_levels_all_leaderboards(game_name, level_name):
    game = api.search(dt.Game, {"name": game_name})[0]
    for level in game.levels:
        if level.name == level_name:
            urls = build_level_urls(level)
            return urls
