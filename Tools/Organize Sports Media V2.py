import os
import shutil

destination_paths = {
    'BTCC': 'I:/Sports/BTCC/Season 2023',
    'Boxing': 'I:/Sports/Boxing/2023',
    'Formula 1': 'I:/Sports/Formula 1/2023',
    'Formula E': 'I:/Sports/Formula E/Season 2223',
    'MotoGP': 'I:/Sports/MotoGP/',
    'WRC': 'I:/Sports/WRC/Season 2023',
    'NASCAR Cup Series': 'I:/Sports/NASCAR Cup Series/2023',
    'Bundesliga': 'I:/Sports/Bundesliga/2223',
    'EuroLeague': 'I:/Sports/EuroLeague/2223',
    'XFL': 'I:/Sports/XFL/2223',
    'AFL': 'I:/Sports/AFL/2223',
    'NHL': 'I:/Sports/Ice Hockey/NHL/Season 2023',
    'NBA': 'I:/Sports/NBA/Season 2023',
    'NFL': 'I:/Sports/NFL/Season 2023',
    'MLB': 'I:/Sports/MLB/Season 2023',
    'MLS': 'I:/Sports/MLS/Season 2023',
    'WWE': 'I:/Sports/WWE/Season 2023',
    'UFC': 'I:/Sports/UFC/Season 2023',
    'English.Premier.League': 'I:/Sports/English.Premier.League/2223',
    'Argentinian.Primera.Division': 'I:/Sports/Argentinian Primera Division/2223',
    'Australian.National.Rugby.League': 'I:/Sports/Australian National Rugby League/2223',
}

def move_items(item_list, target_path):
    # Create the target directory if it doesn't exist
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    for item in item_list:
        print(f"Moving {item} to {target_path}")
        target_file_path = os.path.join(target_path, os.path.basename(item))
        if not os.path.exists(target_file_path):
            shutil.move(item, target_file_path)


def find_items(path, league_list):
    item_list = []
    for root, _, files in os.walk(path):
        for file in files:
            if any(league in file for league in league_list) and file.endswith('.mkv'):
                item_list.append(os.path.join(root, file))
    return item_list

# Update the league names
league_list = ['Australian.National.Rugby.League','Argentinian.Primera.Division','English.League.Championship','BTCC', 'Boxing', 'Formula 1', 'Formula E', 'MotoGP', 'WRC', 'NASCAR Cup Series', 'Bundesliga', 'EuroLeague', 'XFL', 'AFL', 'NHL', 'NBA', 'NFL', 'MLB', 'MLS', 'English Premier League', 'WWE', 'UFC']

items = find_items('.', league_list)

for league in league_list:
    matched_items = [item for item in items if league in item]
    print(f"{league} folders and .mkv files:", matched_items)
    move_items(matched_items, destination_paths[league])

input("Press Enter to exit...")
