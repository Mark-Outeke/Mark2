import requests
import csv
import json

# DHIS2 instance details
base_url = 'http://localhost:8080/dhis2-stable-40.4.1'
username = 'admin'
password = 'district'
program_id = 'wfd9K4dQVDR'
org_unit_id = 'GuJvMV22ihs'

# API endpoint to fetch tracked entity instances
endpoint = f'{base_url}/api/trackedEntityInstances.json?pageSize=20000&program={program_id}&ou={org_unit_id}&fields=trackedEntityInstance,attributes'

# Make the API request
response = requests.get(endpoint, auth=(username, password))

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
   
    # Extract tracked entity instances and their attributes
    tracked_entities = data['trackedEntityInstances']
    
    # Print the tracked entity instance IDs and attributes
    print("Tracked Entity Instances and Attributes:")
    for tei in tracked_entities:
        tei_id = tei['trackedEntityInstance']
        attributes = tei.get('attributes', [])
        print(f"TEI ID: {tei_id}")
        for attr in attributes:
            print(f" - {attr['attribute']}: {attr['value']}")
    
    # Write the tracked entity instance IDs and attributes to a CSV file
    with open('tracked_entity_instances_with_attributes.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write the header
        csvwriter.writerow(['Tracked Entity Instance ID', 'Attribute', 'Value'])
        for tei in tracked_entities:
            tei_id = tei['trackedEntityInstance']
            for attr in tei.get('attributes', []):
                csvwriter.writerow([tei_id, attr['attribute'], attr['value'].encode('utf-8')])
    
    print("Tracked entity instances and attributes have been written to 'tracked_entity_instances_with_attributes.csv'")
else:
    print(f"Error: Unable to fetch data (Status Code: {response.status_code})")
    print("Response content:", response.content.decode('utf-8'))  # Log the response content for debugging
