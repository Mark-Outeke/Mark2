import requests
import csv
import json

# DHIS2 instance details
base_url = 'http://localhost:8080/dhis2-stable-40.4.1'
username = 'admin'
password = 'district'
org_unit_id = 'GuJvMV22ihs'  # Organization unit ID

# API endpoint to fetch enrollments
endpoint = f'{base_url}/api/trackedEntityInstances.json?fields*&enrollment&trackedEntityType=MCPQUTHX1Ze&ou=GuJvMV22ihs'

# Make the API request
response = requests.get(endpoint, auth=(username, password))

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    
    # Extract the first enrollment's orgUnitName for the file name
    #org_unit_name = data['enrollments'][0]['orgUnitName'] if data['enrollments'] else 'UnknownOrgUnit'

    # Extract enrollment details
    trackedEntityInstances = [
        (
            trackedEntityInstances['attributes'],
            trackedEntityInstances['trackedEntityInstance'], 
            trackedEntityInstances['incidentDate'],
            trackedEntityInstances['enrollmentDate'],
            trackedEntityInstances['program'],
            trackedEntityInstances['orgUnit'],
            trackedEntityInstances['orgUnitName']
           
        )
        for trackedEntityInstances in data['trackedEntityInstances']
    ]
    
    # Print the enrollment details
    print("Enrollment Details (Enrollment ID, Tracked Entity Instance ID, Incident Date, Enrollment Date, Program, Org Unit, Org Unit Name):")
    for trackedEntityInstances_attribute in trackedEntityInstances:
        print(trackedEntityInstances_attribute)
    
    # Write the enrollment details to a CSV file
    csv_filename = f'enrollment_details_{org_unit_name}.csv'
    with open(csv_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Enrollment ID', 'Tracked Entity Instance ID', 'Incident Date', 'Enrollment Date', 'Program', 'Org Unit', 'Org Unit Name'])  # Write the header
        for enrollment_detail in enrollments:
            csvwriter.writerow(enrollment_detail)
    
    print(f"Enrollment details have been written to '{csv_filename}'")
else:
    print(f"Error: Unable to fetch data (Status Code: {response.status_code})")
    print("Response content:", response.content.decode('utf-8'))  # Log the response content for debugging
