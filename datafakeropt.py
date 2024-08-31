import json
import random
import uuid
from datetime import datetime, timedelta

# Utility functions
def getDataElementIdToOptionMap():
    with open('DataElementIdToOptionMapping.json') as file:
        return json.load(file)

def getDataElementIdToOptionProbabilitiesMap():
    with open('OptionProbabilities.json') as file:
        return json.load(file)

def getTreatmentElements():
    with open('TreatmentElements.json') as file:
        return json.load(file)

def getEnrollments():
    with open('Enrollments.json') as file:
        return json.load(file)

# Synthesizer Class for Treatment Elements
class TreatmentDataSynthesizer:
    def __init__(self):
        self.dataElementIdToOptionProbabilitiesMap = getDataElementIdToOptionProbabilitiesMap()
        self.dataElementIdToOptionMap = getDataElementIdToOptionMap()
        self.treatmentElements = getTreatmentElements()

    def generateValue(self, enrollment, element):
        element_id = element['id']
        value_type = element['valueType']

        if element_id in self.dataElementIdToOptionProbabilitiesMap:
            options = list(self.dataElementIdToOptionProbabilitiesMap[element_id].keys())
            weights = list(self.dataElementIdToOptionProbabilitiesMap[element_id].values())
            return random.choices(options, weights=weights)[0]

        elif element_id in self.dataElementIdToOptionMap:
            return random.choice(self.dataElementIdToOptionMap[element_id]['options'])

        elif value_type == 'TRUE_ONLY':
            options = ['true', '']
            weights = self.getWeightsForTrueOnly(element_id)
            return random.choices(options, weights=weights)[0]

        elif value_type == 'DATE':
            return (datetime.fromisoformat(enrollment['incidentDate']) 
                    + timedelta(days=random.randint(1, 60))).isoformat()

        elif value_type == 'PHONE_NUMBER':
            return '0911-911-911'

        elif value_type == 'TEXT':
            return ""

        elif value_type == 'NUMBER':
            return ""

        else:
            return 'FAKE DATA'

    def getWeightsForTrueOnly(self, element_id):
        match element_id:
            case 't6qq4TXSE7n':
                return [0.40, 0.60]
            case 'ig3ZDT8Mgus':
                return [0.10, 0.90]
            case 'HHf4Vff0Xrx':
                return [0.15, 0.85]
            case 'BQ2qwbH5WXi':
                return [0.15, 0.85]
            case 'WqWIsCuYw14':
                return [0.175, 0.825]
            case _:
                return [0.50, 0.50]

    def synthesize(self, enrollment):
        dataValues = []
        dictionary = {}

        for treatmentElement in self.treatmentElements:
            value = self.generateValue(enrollment, treatmentElement)
            dataValues.append({
                "dataElement": treatmentElement['id'],
                "value": value
            })

        dictionary['event'] = ""
        dictionary['trackedEntityInstance'] = enrollment['trackedEntityInstance']
        dictionary['enrollment'] = enrollment['enrollment']
        dictionary['eventDate'] = (datetime.fromisoformat(enrollment['incidentDate']) 
                                   + timedelta(days=random.randint(1, 60))).isoformat()
        dictionary['orgUnit'] = enrollment['orgUnit']
        dictionary['dataValues'] = dataValues

        return dictionary

# Main logic to generate synthetic treatment data
if __name__ == "__main__":
    enrollments = getEnrollments()
    treatmentSynthesizer = TreatmentDataSynthesizer()

    syntheticData = []

    for enrollment in enrollments:
        treatmentEvent = treatmentSynthesizer.synthesize(enrollment)
        syntheticData.append(treatmentEvent)

    # Save the generated synthetic treatment data to a JSON file
    with open('SyntheticTreatmentData.json', 'w') as outfile:
        json.dump(syntheticData, outfile, indent=4)

    print("Synthetic treatment data generation complete!")
