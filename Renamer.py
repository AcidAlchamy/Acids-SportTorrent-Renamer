import csv
import os
import re
import datetime
import unicodedata
from openpyxl import Workbook

# Prepare regex to match date in filename
date_pattern = re.compile(r'\d{2}\.\d{2}\.\d{4}')

csv_dir = 'C:/Users/UserName/'  # path to directory with CSV files
video_dir = 'C:/Users/UserName/'  # path to directory with video files

# Create a set to store processed files
processed_files = set()

# Create log file
log_file = open('matching_log.txt', 'w', encoding='utf-8')

# Create CSV file
csv_file = open('matching_results.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Timestamp', 'Filename', 'Strings Matched', 'New Filename', 'Matched'])

# Create Excel file
workbook = Workbook()
sheet = workbook.active
sheet.append(['Timestamp', 'Filename', 'Strings Matched', 'New Filename', 'Matched'])
excel_filename = 'matching_results.xlsx'

# Functions to handle team name matching and adjustment
def normalize_name(name):
    if isinstance(name, list):
        return [unicodedata.normalize('NFKD', team.lower().strip()) for team in name]
    else:
        return unicodedata.normalize('NFKD', name.lower().strip())

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

# Functions for logging and writing to CSV and Excel
def log_event(message):
    print(message)
    log_file.write(message + '\n')

def write_to_csv(timestamp, filename, strings_matched, new_filename, matched):
    csv_writer.writerow([timestamp, filename, strings_matched, new_filename, matched])

def write_to_excel(timestamp, filename, strings_matched, new_filename, matched):
    sheet.append([timestamp, filename, strings_matched, new_filename, matched])

# First scan: Match filenames to Column B
for video_filename in os.listdir(video_dir):
    date_match = date_pattern.search(video_filename)
    if date_match:
        video_date = date_match.group(0)
        video_event = video_filename.replace(video_date, '').strip('.mkv')
        video_teams = re.split(r' - | at | vs ', video_event)
        found_match = False  # flag to track if a match is found
        unmatched_reason = ''  # reason for the unmatched file
        for csv_filename in os.listdir(csv_dir):
            with open(os.path.join(csv_dir, csv_filename), newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    event_date, event_column_b, event_column_c, event_column_d, event_column_e, _, _ = row
                    if event_date == video_date and (video_filename, event_column_c, event_column_d) not in processed_files:
                        log_event(f'Processing: {video_filename}')
                        log_event(f'Teams in Filename: {video_teams}')
                        log_event(f'Teams in CSV - Team 1: {event_column_c}, Team 2: {event_column_d}')
                        
                        # Normalize team names
                        normalized_filename_teams = normalize_name(video_teams)
                        normalized_csv_teams = [normalize_name(team) for team in [event_column_b, event_column_c, event_column_d] if team]
                        
                        # Check for a match using original team names
                        if match_teams(normalized_filename_teams, normalized_csv_teams):
                            log_event(f'Match found in file: {csv_filename}, date: {event_date}, mkv file: {video_filename}')
                            desired_filename = row[4]  # Extract desired filename from "Plex Name" column
                            log_event(f'Desired Filename: {desired_filename}')
                            try:
                                # Rename the video file to the desired filename
                                old_path = os.path.join(video_dir, video_filename)
                                new_path = os.path.join(video_dir, desired_filename)
                                os.rename(old_path, new_path)
                                log_event(f'Renamed file: {video_filename} to {desired_filename}')
                                processed_files.add((video_filename, event_column_c, event_column_d))
                                found_match = True
                                write_to_csv(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), video_filename, ','.join(video_teams), desired_filename, 'Yes')
                                write_to_excel(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), video_filename, ','.join(video_teams), desired_filename, 'Yes')
                                break  # we found a good match, no need to look further in this csv file
                            except Exception as e:
                                log_event(f'Error occurred while renaming file: {video_filename}')
                                log_event(f'Error message: {e}')
                        else:
                            # Adjust team names in the CSV file and retry matching
                            adjusted_csv_teams = adjust_team_names(normalized_filename_teams, normalized_csv_teams)
                            
                            if match_teams(normalized_filename_teams, adjusted_csv_teams):
                                log_event(f'Match found in file after adjusting CSV team names: {csv_filename}, date: {event_date}, mkv file: {video_filename}')
                                desired_filename = row[4]  # Extract desired filename from "Plex Name" column
                                log_event(f'Desired Filename: {desired_filename}')
                                try:
                                    # Rename the video file to the desired filename
                                    old_path = os.path.join(video_dir, video_filename)
                                    new_path = os.path.join(video_dir, desired_filename)
                                    os.rename(old_path, new_path)
                                    log_event(f'Renamed file: {video_filename} to {desired_filename}')
                                    processed_files.add((video_filename, event_column_c, event_column_d))
                                    found_match = True
                                    write_to_csv(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), video_filename, ','.join(video_teams), desired_filename, 'Yes')
                                    write_to_excel(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), video_filename, ','.join(video_teams), desired_filename, 'Yes')
                                    break  # we found a good match, no need to look further in this csv file
                                except Exception as e:
                                    log_event(f'Error occurred while renaming file: {video_filename}')
                                    log_event(f'Error message: {e}')
                    elif event_date != video_date:
                        unmatched_reason = 'Mismatched date'
                if found_match:
                    break  # we found a match, no need to look further in other csv files

            if unmatched_reason:
                log_event(f'No match found for file: {video_filename}. Reason: {unmatched_reason}')
                write_to_csv(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), video_filename, ','.join(video_teams), '', 'No')
                write_to_excel(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), video_filename, ','.join(video_teams), '', 'No')

# Second scan: Match filenames to Column B with date + 1
for video_filename in os.listdir(video_dir):
    date_match = date_pattern.search(video_filename)
    if date_match:
        video_date = date_match.group(0)
        video_date_adjusted = (datetime.datetime.strptime(video_date, '%d.%m.%Y') + datetime.timedelta(days=1)).strftime('%d.%m.%Y')
        if video_date_adjusted != video_date:
            video_event = video_filename.replace(video_date, '').strip('.mkv')
            video_teams = re.split(r' - | at | vs ', video_event)
            found_match = False  # flag to track if a match is found
            unmatched_reason = ''  # reason for the unmatched file
            for csv_filename in os.listdir(csv_dir):
                with open(os.path.join(csv_dir, csv_filename), newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        event_date, event_column_b, event_column_c, event_column_d, event_column_e, _, _ = row
                        if event_date == video_date_adjusted and (video_filename, event_column_c, event_column_d) not in processed_files:
                            log_event(f'Processing with adjusted date: {video_filename}')
                            log_event(f'Teams in Filename: {video_teams}')
                            log_event(f'Teams in CSV - Team 1: {event_column_c}, Team 2: {event_column_d}')
                            
                            # Normalize team names
                            normalized_filename_teams = normalize_name(video_teams)
                            normalized_csv_teams = [normalize_name(team) for team in [event_column_b, event_column_c, event_column_d] if team]
                            
                            # Check for a match using original team names
                            if match_teams(normalized_filename_teams, normalized_csv_teams):
                                log_event(f'Match found in file with adjusted date: {csv_filename}, date: {event_date}, mkv file: {video_filename}')
                                desired_filename = row[4]  # Extract desired filename from "Plex Name" column
                                log_event(f'Desired Filename: {desired_filename}')
                                try:
                                    # Rename the video file to the desired filename
                                    old_path = os.path.join(video_dir, video_filename)
                                    new_path = os.path.join(video_dir, desired_filename)
                                    os.rename(old_path, new_path)
                                    log_event(f'Renamed file: {video_filename} to {desired_filename}')
                                    processed_files.add((video_filename, event_column_c, event_column_d))
                                    found_match = True
                                    write_to_csv(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), video_filename, ','.join(video_teams), desired_filename, 'Yes')
                                    write_to_excel(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), video_filename, ','.join(video_teams), desired_filename, 'Yes')
                                    break  # we found a good match, no need to look further in this csv file
                                except Exception as e:
                                    log_event(f'Error occurred while renaming file: {video_filename}')
                                    log_event(f'Error message: {e}')
                                    unmatched_reason = 'Error renaming file'
                        elif event_date != video_date_adjusted:
                            unmatched_reason = 'Mismatched date'

                        if found_match:
                            break  # we found a match, no need to look further in other csv files

                    if unmatched_reason:
                        log_event(f'No match found for file with adjusted date: {video_filename}. Reason: {unmatched_reason}')
                        write_to_csv(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), video_filename, ','.join(video_teams), '', 'No')
                        write_to_excel(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), video_filename, ','.join(video_teams), '', 'No')



# Close log file
log_file.close()

# Save and close CSV file
csv_file.close()

# Save Excel file
workbook.save(excel_filename)
workbook.close()

print("Processing completed.")

# Print the processed files
print("Processed Files:")
for file in processed_files:
    print(file)
