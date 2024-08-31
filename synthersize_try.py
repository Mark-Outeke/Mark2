
import json
import random
import uuid
from datetime import datetime, timedelta



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

def getBaseLineElements():
    file = open('BaselineElements.json')
    baselineElements = json.load(file)
    file.close()
    return baselineElements
 
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



def Synthesize(self, enrollment):
        dataValues = []
        dictionary = {}

        for treatmentElement in self.treatmentElements:
            value = self.generateValue(enrollment, treatmentElement, dictionary)
            dictionary[treatmentElement['id']] = value

            #calculate the new BMI
            if treatmentElement['id'] == "HzhDngURGLk":
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
                    
            elif treatmentElement['id'] == "vZMCHh6nEBZ":
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

            elif treatmentElement['id'] == "LyiHJrtjNTX":
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

            elif treatmentElement['id'] == "muBnQUtbS9R":
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

            elif treatmentElement['id'] == "wpV8b2x6uDP":
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
            else:
                        value = self.generateValue(enrollment, treatmentElement, dictionary)
                        dictionary[treatmentElement['id']] = value      
        for element_id, value in dictionary.items():
            if value != "":
                dataValues.append({"dataElement" : element_id, "value" : value})
        
        # After processing, you might want to write the updated dictionary or dataValues to a file or return them
        return dataValues

# Example usage
#synthesizer = TreatmentDataSynthesizer()
synthesized_data = Synthesize(self, enrollment=None) 
print(synthesized_data)