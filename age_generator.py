import json
import random

# Load enrollments from a JSON file
with open('Enrollments.json', 'r') as file:
    enrollments = json.load(file)

# Define a function to generate a random age between 18 and 65
def generate_random_age():
    return random.randint(18, 65)

# Create the desired JSON format for trackedEntityInstances
tracked_entity_instances = {
    "trackedEntityInstances": []
}

# Iterate through each enrollment and build the JSON structure
for enrollment in enrollments:
    instance = {
        "trackedEntityInstance": enrollment["trackedEntityInstance"],
        "trackedEntityType": "MCPQUTHX1Ze",
        "orgUnit": enrollment["orgUnit"],
        "attributes": [
            {
        
                "attribute": "Gy1jHsTp9P6",  # Replace with actual attribute ID for age
                "value": generate_random_age()
            }
        ]
    }
    tracked_entity_instances["trackedEntityInstances"].append(instance)

# Print the JSON data with random ages
print(json.dumps(tracked_entity_instances, indent=4))

# Optionally, save the generated JSON to a file
with open('output_tracked_entity_instances_Age.json', 'w') as outfile:
    json.dump(tracked_entity_instances, outfile, indent=4)
