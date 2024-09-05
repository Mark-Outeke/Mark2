import json
import random
import uuid
from datetime import datetime, timedelta

#################################################################################################
# Utility functions
#################################################################################################

def getEvents():
    file = open('Month 3 treatmentStageOutputtest.json')
    eventData = json.load(file)
    file.close()
    return eventData["events"]

def getTreatmentOutcomeElements():
    file = open('TreatmentOutcomeElements.json')
    treatmentOutcomeElements = json.load(file)
    file.close()
    return treatmentOutcomeElements

def getValueByID(dataValues = [], elementId = ""):
    for dataValue in dataValues:
        if elementId == dataValue["dataElement"]:
            return dataValue["value"]
    
    return ""
def getEventDatefromMonth3():
    file = open('Month 3 treatmentStageOutputtest.json')
    month3Data = json.load(file)
    file.close()
    return month3Data

def generateTreatmentStageDate(month3DataEvent):
    #calcualte the date from incidentdate to the month of treatment and 
    # and generate the treatmentstage date .

    date = datetime.fromisoformat(Month3DataEvent["eventDate"])
    return date.isoformat()


class TreatmentOutcomeDataSynthesizer:
    def __init__(self):
        self.treatmentOutcomeElements = getTreatmentOutcomeElements()
    
    def SynthesizeDataValues(self, month3Event):

        month3EventDataValues = month3Event["dataValues"]
        stageDataValues = []  
        month3Event = getEvents(month3Event)
        for month3Data in self.month3Data:
   

            for treatmentOucomeElement in self.treatmentOutcomeElements:

                
                    match treatmentElement['id']:
                        case "TFS9P7tu6U6":
                            
                            value = random.choices(["Yes", "No"],
                            weights= [0.01, 0.99])

                            stageDataValues.append({
                                "dataElement" : treatmentElement['id'],
                                "value" : value
                                })
                        case _:
                            pass         
        return stageDataValues



def main():
    synthesizer = TreatmentOutcomeDataSynthesizer()
    month3Events = getEvents()

    for Events in month3Events:

        eventDate = getEventDatefromMonth3(eventData)

        dataValues = synthesizer.SynthesizeDataValues(month3Event)
        newEvent = {
                "dataValues"    : dataValues,
                "event"         : "",
                "program"       : baselineEvent["program"],
                "programStage"  : "tJ5SV8gfZaA",
                "programType"   : "WITH_REGISTRATION",
                "orgUnit"       : baselineEvent["orgUnit"],
                "eventDate"     : eventDate,
                "status"        : "COMPLETED",
                "completedDate" : eventDate,
                "attributeOptionCombo": "HllvX50cXC0",
                "trackedEntityInstance" : baselineEvent["trackedEntityInstance"],
            }

    stageEvents.append(newEvent)



        
    data = {"events" : stageEvents}
    f = open(f'treatmentoutcome.json.json', 'w')
    json.dump(data, f)
    f.close()
        
    
if "__main__":
    main()