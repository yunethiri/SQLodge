import csv
import json

csv_file_path = 'C:/Users/Jeshuan/Desktop/database.csv'
json_file_path = 'C:/Users/Jeshuan/Desktop/sqldata.json'


# Open the CSV file and read its content
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    # Create a CSV reader object
    csv_reader = csv.reader(csvfile)

    # Get the header row
    header = next(csv_reader)

    # Create an empty list to hold the rows
    rows = []

    # Read each row of data from the CSV file and add it to the rows list
    for row in csv_reader:
        rows.append(row)

# Create an empty list to hold the JSON objects
json_objects = []

# Convert each row to a JSON object and add it to the json_objects list
for row in rows:
    json_objects.append(dict(zip(header, row)))

# Open the JSON file and write the JSON objects to it
with open(json_file_path, 'w') as jsonfile:
    json.dump(json_objects, jsonfile)