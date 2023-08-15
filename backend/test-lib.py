import srcomapi, srcomapi.datatypes as dt

api = srcomapi.SpeedrunCom()

# Search for the game "Destiny 2"
games = api.search(dt.Game, {"name": "Destiny 2"})
game = games[0]

# Iterate through the levels of the game
for level in game.levels:
    print("Level Name:", level.name)
    print("Level ID:", level.id)

    # Get the categories for the level
    categories_url = f"https://www.speedrun.com/api/v1/levels/{level.id}/categories"
    categories_data = api.get(categories_url)

    print("Categories:")
    for category in categories_data['data']:
        print("  Category ID:", category['id'])
        print("  Category Name:", category['name'])
