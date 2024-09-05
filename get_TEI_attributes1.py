import requests
import json

# Function to fetch JSON data from DHIS2 API
def fetch_data_from_dhis2(api_url, username, password):
    response = requests.get(api_url, auth=(username, password))
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

# Function to extract trackedEntityInstance and attributes
def extract_tracked_entity_instances(data):
    instances = data.get("trackedEntityInstances", [])
    result = []

    for instance in instances:
        instance_id = instance.get("trackedEntityInstance")
        attributes = instance.get("attributes", [])
        instance_data = {
            "trackedEntityInstance": instance_id,
            "attributes": [
                {
                    "attribute": attr.get("attribute"),
                    "displayName": attr.get("displayName"),
                    "value": attr.get("value"),
                    "valueType": attr.get("valueType")
                }
                for attr in attributes
            ]
        }
        result.append(instance_data)

    return result

# Main function to fetch and process data
def main():
    api_url = 'http://localhost:8080/dhis2-stable-40.4.1/api/trackedEntityInstances?paging=false&fields*&enrollment&trackedEntityType=MCPQUTHX1Ze&ou=GuJvMV22ihs'
    username = 'admin'
    password = 'district'
    try:
        data = fetch_data_from_dhis2(api_url, username, password)
        tracked_entity_instances = extract_tracked_entity_instances(data)
        
        # Count the number of tracked entity instances
        count = len(tracked_entity_instances)
        
        # Print the count
        print(f"Number of tracked entity instances: {count}")
        
        # Save the count and instances to a JSON file
        output_data = {
            "count": count,
            "trackedEntityInstances": tracked_entity_instances
        }
        
        with open('tracked_entity_instances_output.json', 'w') as f:
            json.dump(output_data, f, indent=4)
        
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    # Fetch data from DHIS2 API
    data = fetch_data_from_dhis2(api_url, username, password)
    
    # Extract tracked entity instances and attributes
    processed_data = extract_tracked_entity_instances(data)
    
     

if __name__ == "__main__":
    main()
