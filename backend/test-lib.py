import srcomapi, srcomapi.datatypes as dt

api = srcomapi.SpeedrunCom(); api.debug = 1

games = api.search(dt.Game, {"name": "Destiny 2 Story"})
game = games[0]

print(game.id)

id_run = "5923j3od/rkljm7nd?var-0nwop7kl=gq7evvr1&var-ylq6q5v8=5q8jn7rl"

response = api.get("leaderboards/yd4or2x1/level/{}".format (id_run))
print(response)


level_id = 'z98oorrd'
all_information = dt.Variable(api, data=api.get(f"levels/z98oorrd/categories?embed=variables"))

for all_informations in all_information.data:
    print(all_informations['name'])
    name_category = all_informations['name']
    id_category = all_informations['id']

    subcategories = all_informations['variables']['data']
    for subcategy in subcategories:
        if subcategy['is-subcategory'] == True:
            #print (subcategy)
            is_subcategory = subcategy
            id_subcategory = is_subcategory['id']
            name_subcategory = is_subcategory['name']
            print(id_subcategory)
            choices = is_subcategory['values']['values']
            print(choices)
            for id_choices, name_choices in choices.items():
                print(f"id_choices: {id_choices}")
                print(f"name_choices: {name_choices}")



##print(games)
##print(game)

#print (game)
game_categories = game.categories  # Selecting the third category
game_category = game.categories[5]  # Selecting the third category

##print(game_category)
##print(game_categories)

game_levels = game.levels
game_level = game.levels[0]

#print(game_levels)
#print(game_level)

game_id = game_level.id

#print(game_id)
#game_level_records = game_level.records

#game_category_records = game_category.records
# Loop through all the records and #print them
#for record in game_category_records:
    #for run in record.runs:
        ##print(run)

# #print levels
#print("Levels:")
#for level in game.levels:
    #print("Level Name:", level.name)
    #print("Level ID:", level.id)

# #print categories
#print("\nCategories:")
#for category in game.categories:
    #print("Category Name:", category.name)
    #print("Category ID:", category.id)




# Find the level "What Remains"
level_what_remains = None
for level in game.levels:
    if level.name == "What Remains":
        level_what_remains = level.endpoint
        #print(level_what_remains)
        break

# Identify the corresponding category (you may need to modify this part)
category_id = "What Remains"  # Replace with the correct category ID

# Retrieve the leaderboard for the level and category
#leaderboard = dt.Leaderboard(api, data=api.get("leaderboards/{}/level/{}/n2yjrq12?embed=variables".format(game.id, level_what_remains.id, category_id)))

# Extract the runs from the leaderboard
#



