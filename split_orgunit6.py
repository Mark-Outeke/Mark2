import json
from collections import defaultdict
import os

def split_json_by_orgUnit(input_file):
    # Load the JSON data
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Group data by orgUnit
    orgUnit_groups = defaultdict(list)
    for event in data["events"]:
        orgUnit = event["orgUnit"]
        orgUnit_groups[orgUnit].append(event)
    
    # Write each group to a separate file
    base_name, _ = os.path.splitext(input_file)
    
    for orgUnit, events in orgUnit_groups.items():
        output_file = f"{base_name}_{orgUnit}.json"
        with open(output_file, 'w') as f:
            json.dump({"events": events}, f, indent=4)
        print(f'Successfully wrote {len(events)} events to {output_file}')

# Example usage
input_file = 'Month 6 treatmentStageOutputtest.json'
split_json_by_orgUnit(input_file)