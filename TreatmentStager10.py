import json
import random
from datetime import datetime

#################################################################################################
# Utility functions
#################################################################################################

def getEvents():
    with open('Month 3 treatmentStageOutputtest.json', 'r') as file:
        eventData = json.load(file)
    return eventData["events"]

def getTreatmentOutcomeElements():
    with open('TreatmentOutcomeElements.json', 'r') as file:
        treatmentOutcomeElements = json.load(file)
    return treatmentOutcomeElements

def getEventDateFromMonth3(event):
    return event["eventDate"]

def generateTreatmentStageDate(month3Event):
    # Calculate the date for the treatment stage.
    date = datetime.fromisoformat(month3Event["eventDate"])
    return date.isoformat()

class TreatmentOutcomeDataSynthesizer:
    def __init__(self):
        self.treatmentOutcomeElements = getTreatmentOutcomeElements()
    
    def synthesizeDataValues(self, month3Event):
        stageDataValues = []

        for treatmentElement in self.treatmentOutcomeElements:
            match treatmentElement['id']:
                case "J5kKvyU8mpY":
                    value = random.choices(
                        ["Yes", "No"], 
                        weights=[0.01, 0.99]
                    )[0]
                    stageDataValues.append({
                        "dataElement": treatmentElement['id'],
                        "value": value
                    })

                case "TFS9P7tu6U6":
                    outcome_value = random.choices(
                        [
                            "Cured",
                            "Treatment Completed",
                            "Treatment Failure",
                            "Lost to Follow up",
                            "Not Evaluated",
                            "Died"
                        ], 
                        weights=[0.45, 0.36, 0.01, 0.04, 0.01, 0.10]
                    )[0]
                    stageDataValues.append({
                        "dataElement": "TFS9P7tu6U6",
                        "value": outcome_value
                    })

                case _:
                    pass

        return stageDataValues

def main():
    synthesizer = TreatmentOutcomeDataSynthesizer()
    month3Events = getEvents()
    stageEvents = []

    for month3Event in month3Events:
        eventDate = getEventDateFromMonth3(month3Event)
        dataValues = synthesizer.synthesizeDataValues(month3Event)

        newEvent = {
            "dataValues": dataValues,
            "event": "",  # Generate or assign an event ID if needed
            "program": month3Event["program"],
            "programStage": "SJXASCwe3wQ",
            "programType": "WITH_REGISTRATION",
            "orgUnit": month3Event["orgUnit"],
            "eventDate": eventDate,
            "status": "COMPLETED",
            "completedDate": eventDate,
            "attributeOptionCombo": "HllvX50cXC0",
            "trackedEntityInstance": month3Event["trackedEntityInstance"],
        }

        stageEvents.append(newEvent)

    # Save the generated events to a file
    data = {"events": stageEvents}
    with open('TreatmentOutcome.json', 'w') as f:
        json.dump(data, f, indent=4)

    # Print the number of generated events
    print(f"Number of events generated: {len(stageEvents)}")

if __name__ == "__main__":
    main()
