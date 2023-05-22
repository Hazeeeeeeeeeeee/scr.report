import requests
import json

url = "https://www.speedrun.com/api/v1/games/yd4or2x1/levels?embed=categories.variables.variables"
url_donjon_strike = "https://www.speedrun.com/api/v1/games/4d7y5zd7/levels?embed=categories.variables.variables"

response = requests.get(url)
data = response.json()

output_dict = {}

for mission in data['data']:
    mission_name = mission['name'].replace(' ', '_')
    mission_id = mission['id']

    output_dict[mission_name] = {}

    for category in mission['categories']['data']:
        category_name = category['name'].replace(' ', '_')
        category_id = category['id']

        category_dict = {}

        if 'variables' in category and category['variables']['data']:
            for variable in category['variables']['data']:
                if variable['is-subcategory']:
                    for value_id, value_data in variable['values']['values'].items():
                        variable_name = variable['name'].replace(' ', '_')
                        variable_id = variable['id']
                        value_label = value_data['label'].replace(' ', '_')

                        url_value = f'{mission_id}/{category_id}?id-{variable_id}={value_id}'
                        category_dict[f'{variable_name}_{value_label}'] = url_value
                        
                else:
                    category_dict = {"Default": f'{mission_id}/{category_id}'}

            if not category_dict:
                category_dict = {"Default": f'{mission_id}/{category_id}'}

        output_dict[mission_name][category_name] = category_dict

with open("output_1.txt", "w") as file:
    file.write("mission_ids = {\n")
    for mission_name, categories in output_dict.items():
        file.write(f"  '{mission_name}': {{\n")
        for category, variables in categories.items():
            file.write(f"    '{category}': {{\n")
            variable_entries = [f"      '{variable}': '{variable_url}'," for variable, variable_url in variables.items()]
            file.write('\n'.join(variable_entries))
            file.write("\n    },\n")
        file.write("  },\n")
    file.write("}\n")
