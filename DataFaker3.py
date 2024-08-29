import json
import random
import uuid
from datetime import datetime, timedelta

#################################################################################################
# Utility functions
#################################################################################################

def getDataElementIdToOptionMap():
    file = open('DataElementIdToOptionMapping.json')
    dataElementIdToOptionMap = json.load(file)
    file.close()
    return dataElementIdToOptionMap

def getDataElementIdToOptionProbabilitiesMap():
    file = open('OptionProbabilities.json')
    dataElementIdToOptionProbabilitiesMap = json.load(file)
    file.close()
    return dataElementIdToOptionProbabilitiesMap

##def getBaseLineElements():
    ##file = open('BaselineElements.json')
    #baselineElements = json.load(file)
    #file.close()
    #return baselineElements
 
def getEnrollments():
    file = open('Enrollments.json')
    enrollments = json.load(file)
    file.close()
    return enrollments

def getRandomDateTimeBeforeEnrollment(enrollment):
    date = datetime.fromisoformat(enrollment["incidentDate"]) - timedelta(
        days = random.randrange(0, 30))
    return date.isoformat()

def getTreatmentElements():
    file = open('TreatmentElements.json')
    treatmentElements = json.load(file)
    file.close()
    return treatmentElements
#################################################################################################
















class TreatmentDataSynthesizer:
    def __init__(self):
        self.dataElementIdToOptionProbabilitiesMap = getDataElementIdToOptionProbabilitiesMap()
        self.dataElementIdToOptionMap = getDataElementIdToOptionMap()
        self.treatmentElements = getTreatmentElements()




    def generateValue(self, enrollment, treatmentDataElement = {}):
        element_id = treatmentDataElement['id'];
        value_type = treatmentDataElement['valueType']

        #check if the key exist in the dictonary
        if element_id in self.dataElementIdToOptionProbabilitiesMap:

            options = list(self.dataElementIdToOptionProbabilitiesMap[element_id].keys())
            weights = list(self.dataElementIdToOptionProbabilitiesMap[element_id].values())

            return random.choices(options, weights = weights)[0]

        elif element_id in self.dataElementIdToOptionMap:
            return random.choice(self.dataElementIdToOptionMap[element_id]['options'])

        elif value_type == 'TEXT':
            options = ['Mild', ' Moderate', ' Severe', ' Life threatening']
            
            match element_id:
                case 'F5P1buF4RHP':
                    weights = [0.30, 0.40, 0.20, 0.10]

                case 'UtGpqsuTmrD':
                    weights = [0.35, 0.45, 0.15, 0.50]

                case 'rHEeM6ha268':
                   weights = [0.25, 0.35, 0.30, 0.10]

                case 'DHPzkmTcDUv':
                    weights = [0.20, 0.40, 0.30, 0.10]

                case 'RTKE58980U7':
                    weights = [0.30, 0.50, 0.15, 0.50]

                case 'luQQ9zNTgFM':
                    weights = [0.20, 0.40, 0.30, 0.10]

                case 'k5LrUGjAGD5':
                    weights = [0.10, 0.50, 0.30, 0.10]

                case 'EDFvw8DsJuH':
                    weights = [0.40, 0.40, 0.15, 0.50]
                
                case 'Wbp0DL9fQYj':
                    weights = [0.30, 0.50, 0.15, 0.50]
                
                case 'pDR49oOtJrc':
                    weights = [0.50, 0.30, 0.15, 0.50]
                
                case 'mDmVRrzihu0':
                    weights = [0.20, 0.50, 0.20, 0.10]
                
                case 'KAykkHp1p2F':
                    weights = [0.25, 0.40, 0.25, 0.10]
                
                case 'EoO16H5lLK5':
                    weights = [0.05, 0.15, 0.50, 0.30]

                case 'lpJPqjVUToo':
                    weights = [0.30, 0.50, 0.15, 0.05]

                case 'sM7PAEYRqEP':
                    weights = [0.40, 0.40, 0.15, 0.05]        

                case 'rluc10OPm1I':
                    weights = [0.05, 0.30, 0.15, 0.05]    

            return random.choices(options, weights = weights)[0]

        



        ####################################################################################
        #TODO:
        ####################################################################################
        elif value_type == 'DATE':
            return getRandomDateTimeBeforeEnrollment(enrollment)


        elif value_type == 'TEXT':
            return "FAKE TEXT"

        elif value_type == 'NUMBER':
            return "FAKE NUMBER"

        else:
            return 'FAKE DATA'







    def Synthesize(self, enrollment):
        dataValues = []
        dictionary = {}

        # Get the interval options for the specific data element ID
        interval_options = self.dataElementIdToOptionMap.get("U4jSUZPF0HH", [])

        # Define a mapping from interval descriptions to timedelta
        interval_to_timedelta = {
            "1-2 Weeks": timedelta(weeks=2),
            "3-4 Weeks": timedelta(weeks=4),
            "5-6 Weeks": timedelta(weeks=6),
            "7-8 Weeks": timedelta(weeks=8),
            "Month 3": timedelta(days=3*30),  # Approximation
            "Month 4": timedelta(days=4*30),
            "Month 5": timedelta(days=5*30),
            "Month 6": timedelta(days=6*30),
            "Month 7": timedelta(days=7*30),
            "Month 8": timedelta(days=8*30),
            "Month 9": timedelta(days=9*30),
            "Month 10": timedelta(days=10*30),
            "Month 11": timedelta(days=11*30),
            "Month 12": timedelta(days=12*30),
        }

        for treatmentElement in self.treatmentElements:

            if treatmentElement['id'] == "U4jSUZPF0HH":
                # Assuming 'Output.json' contains data that needs to be read and processed
                with open('Output.json', 'r') as infile:
                    data = json.load(infile)
                    
                    for event in data:
                        event_date = data.get('eventDate', "")
                        if event_date:
                            event_date = datetime.strptime(event_date, '%Y-%m-%dT%H:%M:%S.%f')

                        for dataElement in data.get('dataValues', []):
                            # Check if the value is not empty and matches one of the interval options
                            if dataElement.get('value', "") in interval_options:
                                # Calculate the new event date based on the selected interval
                                interval = dataElement['value']
                                new_event_date = event_date + interval_to_timedelta[interval]
                                dictionary['eventDate'] = new_event_date.strftime('%Y-%m-%dT%H:%M:%S.%f')
                                dataValues.append(dictionary['eventDate'])
                            else:
                                value = self.generateValue(enrollment, treatmentElement)
                                dictionary[treatmentElement['id']] = value   

            elif treatmentElement['id'] == "HzhDngURGLk":
                if "xcTT5oXggBZ" in dictionary and "WBsNDNQUgeX" in dictionary:
                    weight = int(dictionary["xcTT5oXggBZ"])
                    height = int(dictionary["WBsNDNQUgeX"])

                    dictionary[treatmentElement['id']] = f"{(weight * 10000) // (height * height)}"
                else: dictionary[treatmentElement['id']]= ""

            elif treatmentElement['id'] == "Ghsh3wqVTif":
                if "FklL99yLd3h" in dictionary and dictionary["FklL99yLd3h"] == "Yes":
                # Check the interval to timedelta option and assign a value accordingly
                    if dictionary["U4jSUZPF0HH"] == "1-2 Weeks":
                        dictionary[treatmentElement['id']] = 1
                    elif dictionary["U4jSUZPF0HH"] == "3-4 Weeks":
                        dictionary[treatmentElement['id']] = 1
                    elif dictionary["U4jSUZPF0HH"] == "5-6 Weeks":
                        dictionary[treatmentElement['id']] = 1
                    elif dictionary["U4jSUZPF0HH"] == "7-8 Weeks":
                        dictionary[treatmentElement['id']] = 2        
                    elif dictionary["U4jSUZPF0HH"] == "Month3":
                        dictionary[treatmentElement['id']] = 3
                    elif dictionary["U4jSUZPF0HH"] == "Month4":
                        dictionary[treatmentElement['id']] = 4
                    elif dictionary["U4jSUZPF0HH"] == "Month5":
                        dictionary[treatmentElement['id']] = 5
                    elif dictionary["U4jSUZPF0HH"] == "Month6":
                        dictionary[treatmentElement['id']] = 6
                    elif dictionary["U4jSUZPF0HH"] == "Month7":
                        dictionary[treatmentElement['id']] = 7
                    elif dictionary["U4jSUZPF0HH"] == "Month8":
                        dictionary[treatmentElement['id']] = 8 
                    elif dictionary["U4jSUZPF0HH"] == "Month9":
                        dictionary[treatmentElement['id']] = 9 
                    elif dictionary["U4jSUZPF0HH"] == "Month10":
                        dictionary[treatmentElement['id']] = 10 
                    elif dictionary["U4jSUZPF0HH"] == "Month11":
                        dictionary[treatmentElement['id']] = 11 
                    elif dictionary["U4jSUZPF0HH"] == "Mont12":
                        dictionary[treatmentElement['id']] = 12 
                else:     
                    dictionary[treatmentElement['id']] = ""
            
            
            for element_id, value in dictionary.items():
                if value != "":
                    dataValues.append({"dataElement" : element_id, "value" : value})

        #print(dataValues)
        # After processing, you might want to write the updated dictionary or dataValues to a file or return them
        return dataValues

# Example usage
#synthesizer = TreatmentDataSynthesizer()
#synthesized_data = synthesizer.Synthesize(enrollment=None)  # Replace None with actual enrollment data if needed
#print(dataValues)



            

  



def main():
    treatmentDataSynthesizer = TreatmentDataSynthesizer()
    enrollments = getEnrollments()
    events = []

    for enrollment in enrollments:
        # Synthesize data and capture the new event date
        dataValues = treatmentDataSynthesizer.Synthesize(enrollment)
        new_event_date =  dataValues[0] if  dataValues else enrollment["incidentDate"]
        
        newEvent = {
           "dataValues"             : dataValues,
            "event"                 : "",
            "program"               : enrollment["Program"],
            "programStage"          : "tJ5SV8gfZaA",
            "programType"           : "WITH_REGISTRATION",
            "orgUnit"               : enrollment["orgUnit"],
            "eventDate"             : new_event_date,
            "status"                : "COMPLETED",
            "completedDate"         : new_event_date,
            "attributeOptionCombo"  : "HllvX50cXC0",
            "trackedEntityInstance" : enrollment["trackedEntityInstance"],
        }
        

    


        
        events.append(newEvent)

    data = {"events" : events}
    f = open('TreatmentOutput.json', 'w')
    json.dump(data, f)
    f.close()
    

if "__main__":
    main()