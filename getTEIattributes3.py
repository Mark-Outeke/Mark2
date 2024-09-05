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
        yield instance_data

def fetch_tracked_entity_instances(api_url, username, password, page_size=50):
    page = 1
    while True:
        data = fetch_data_from_dhis2(api_url, username, password, page, page_size)
        instances = data.get("trackedEntityInstances", [])
        if not instances:
            break
        yield from extract_tracked_entity_instances(data)
        page += 1

def main():
    api_url = 'http://localhost:8080/dhis2-stable-40.4.1/api/trackedEntityInstances.json?fields*&enrollment&trackedEntityType=MCPQUTHX1Ze&ou=GuJvMV22ihs'
    username = 'admin'
    password = 'district'
    
    # Count the number of tracked entity instances
    count = 0
    
    # Save the instances to a JSON file
    with open('tracked_entity_instances_output.json', 'w') as f:
        f.write('[\n')
        for i, instance in enumerate(fetch_tracked_entity_instances(api_url, username, password)):
            if i > 0:
                f.write(',\n')
            json.dump(instance, f, indent=4)
            count += 1
        f.write('\n]')
    
    # Print the count
    print(f"Number of tracked entity instances: {count}")

if __name__ == "__main__":
    main()