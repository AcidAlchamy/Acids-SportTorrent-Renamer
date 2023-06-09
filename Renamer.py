import csv
import os
import re

# Prepare regex to match date in filename
date_pattern = re.compile(r'\d{2}\.\d{2}\.\d{4}')

csv_dir = 'X://Acids-SportTorrent-Renamer/Data'  # path to directory with CSV files
video_dir = 'X://Acids-SportTorrent-Renamer/Files'  # path to directory with video files

# Create a set to store processed files
processed_files = set()

# Functions to handle team name matching and adjustment
def normalize_name(name):
    if isinstance(name, list):
        return [team.lower().strip() for team in name]
    else:
        return name.lower().strip()

def match_teams(filename_teams, csv_teams):
    for team in csv_teams:
        if any(normalize_name(team) in normalize_name(filename_team) or normalize_name(filename_team) in normalize_name(team) for filename_team in filename_teams):
            return True
    return False

def adjust_team_names(filename_teams, csv_teams):
    adjusted_teams = []
    for team in csv_teams:
        for filename_team in filename_teams:
            if normalize_name(team) in normalize_name(filename_team) or normalize_name(filename_team) in normalize_name(team):
                adjusted_teams.append(filename_team)
                break
    return adjusted_teams

# First scan: Match filenames to Column B
for video_filename in os.listdir(video_dir):
    date_match = date_pattern.search(video_filename)
    if date_match:
        video_date = date_match.group(0)
        video_event = video_filename.replace(video_date, '').strip('.mkv')
        video_teams = re.split(r' - | at | vs ', video_event)
        found_match = False  # flag to track if a match is found
        for csv_filename in os.listdir(csv_dir):
            with open(os.path.join(csv_dir, csv_filename), newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    event_date, event_column_b, event_column_c, event_column_d, event_column_e, _, _ = row
                    if event_date == video_date and (video_filename, event_column_c, event_column_d) not in processed_files:
                        print(f'Processing: {video_filename}')
                        print(f'Teams in Filename: {video_teams}')
                        print(f'Teams in CSV - Team 1: {event_column_c}, Team 2: {event_column_d}')
                        
                        # Normalize team names
                        normalized_filename_teams = normalize_name(video_teams)
                        normalized_csv_teams = [normalize_name(team) for team in [event_column_b, event_column_c, event_column_d] if team]
                        
                        # Check for a match using original team names
                        if match_teams(normalized_filename_teams, normalized_csv_teams):
                            print(f'Match found in file: {csv_filename}, date: {event_date}, mkv file: {video_filename}')
                            desired_filename = row[4]  # Extract desired filename from "Plex Name" column
                            print(f'Desired Filename: {desired_filename}')
                            try:
                                # Rename the video file to the desired filename
                                old_path = os.path.join(video_dir, video_filename)
                                new_path = os.path.join(video_dir, desired_filename)
                                os.rename(old_path, new_path)
                                print(f'Renamed file: {video_filename} to {desired_filename}')
                                processed_files.add((video_filename, event_column_c, event_column_d))
                                found_match = True
                                break  # we found a good match, no need to look further in this csv file
                            except Exception as e:
                                print(f'Error occurred while renaming file: {video_filename}')
                                print(f'Error message: {e}')
                        else:
                            # Adjust team names in the CSV file and retry matching
                            adjusted_csv_teams = adjust_team_names(normalized_filename_teams, normalized_csv_teams)
                            
                            if match_teams(normalized_filename_teams, adjusted_csv_teams):
                                print(f'Match found in file after adjusting CSV team names: {csv_filename}, date: {event_date}, mkv file: {video_filename}')
                                desired_filename = row[4]  # Extract desired filename from "Plex Name" column
                                print(f'Desired Filename: {desired_filename}')
                                try:
                                    # Rename the video file to the desired filename
                                    old_path = os.path.join(video_dir, video_filename)
                                    new_path = os.path.join(video_dir, desired_filename)
                                    os.rename(old_path, new_path)
                                    print(f'Renamed file: {video_filename} to {desired_filename}')
                                    processed_files.add((video_filename, event_column_c, event_column_d))
                                    found_match = True
                                    break  # we found a good match, no need to look further in this csv file
                                except Exception as e:
                                    print(f'Error occurred while renaming file: {video_filename}')
                                    print(f'Error message: {e}')
                if found_match:
                    break  # we found a match, no need to look further in other csv files

print("Processing completed.")

# Print the processed files
print("Processed Files:")
for file in processed_files:
    print(file)
