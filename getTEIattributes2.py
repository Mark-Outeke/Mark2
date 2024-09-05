import requests
import json

def fetch_data_from_dhis2(api_url, username, password, page=1, page_size=50):
    # Construct the URL with pagination parameters
    url = f"{api_url}?page={page}&pageSize={page_size}"
    response = requests.get(url, auth=(username, password))
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

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

def main():
    api_url = 'http://localhost:8080/dhis2-stable-40.4.1/api/trackedEntityInstances.json?fields*&enrollment&trackedEntityType=MCPQUTHX1Ze&ou=GuJvMV22ihs'
    username = 'admin'
    password = 'district'
    
    page = 1
    page_size = 50
    all_instances = []

    while True:
        data = fetch_data_from_dhis2(api_url, username, password, page, page_size)
        tracked_entity_instances = extract_tracked_entity_instances(data)
        
        if not tracked_entity_instances:
            break

        all_instances.extend(tracked_entity_instances)
        page += 1  # Move to the next page

    # Count the number of tracked entity instances
    count = len(all_instances)
    
    # Print the count
    print(f"Number of tracked entity instances: {count}")
    
    # Save the count and instances to a JSON file
    output_data = {
        "count": count,
        "trackedEntityInstances": all_instances
    }
    
    with open('tracked_entity_instances_output.json', 'w') as f:
        json.dump(output_data, f, indent=4)
        
if __name__ == "__main__":
    main()