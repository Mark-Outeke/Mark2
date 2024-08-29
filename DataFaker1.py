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

def getRandomDateBeforeEnrollment(enrollment):
    date = datetime.fromisoformat(enrollment["incidentDate"]) - timedelta(
        days = random.randrange(0, 30))
    return date.isoformat()
#################################################################################################
















class BaselineDataSynthesizer:
    def __init__(self):
        self.dataElementIdToOptionProbabilitiesMap = getDataElementIdToOptionProbabilitiesMap()
        self.dataElementIdToOptionMap = getDataElementIdToOptionMap()
        self.baselineElements = getBaseLineElements()




    def generateValue(self, enrollment, baselineDataElement = {}):
        element_id = baselineDataElement['id'];
        value_type = baselineDataElement['valueType']

        #check if the key exist in the dictonary
        if element_id in self.dataElementIdToOptionProbabilitiesMap:

            options = list(self.dataElementIdToOptionProbabilitiesMap[element_id].keys())
            weights = list(self.dataElementIdToOptionProbabilitiesMap[element_id].values())

            return random.choices(options, weights = weights)[0]

        elif element_id in self.dataElementIdToOptionMap:
            return random.choice(self.dataElementIdToOptionMap[element_id]['options'])

        elif value_type == 'TRUE_ONLY':
            options = ['True', 'False']
            
            match element_id:
                case 't6qq4TXSE7n':
                    weights = [0.40, 0.60]

                case 'ig3ZDT8Mgus':
                    weights = [0.10, 0.90]

                case 'HHf4Vff0Xrx':
                    weights = [0.15, 0.85]

                case 'BQ2qwbH5WXi':
                    weights = [0.15, 0.85]

                case 'WqWIsCuYw14':
                    weights = [0.175, 0.825]

                case _:
                    weights = [0.50, 0.50]

            return random.choices(options, weights = weights)[0]




        ####################################################################################
        #TODO:
        ####################################################################################
        elif value_type == 'DATE':
            match element_id:
                case 'EpvHxcDmxyT':
                    return getRandomDateBeforeEnrollment(enrollment)
                case  _:
                    return getRandomDateBeforeEnrollment(enrollment)

        elif value_type == 'PHONE_NUMBER':
            return '0911-911-911' #faker.phone_number()

        elif value_type == 'TEXT':
            return ""

        elif value_type == 'NUMBER':
            return random.randrange(10, 100)

        else:
            return 'FAKE DATA'













    def Synthesize(self, enrollment):
        dataValues = []
        dictionary = {}


        for baseLineElement in self.baselineElements:


            #"DSBS-08 : Started on 1st Line Treatment",
            if baseLineElement['id'] == "CxdzmL6vtnx" and dictionary["f0S6DIqAOE5"] == "Yes":
                dictionary[baseLineElement['id']] = "No"
                

            #"DSBS-09 :  DS-TB regimen"
            elif baseLineElement['id'] == "axDtvPeYL2Y" and dictionary["CxdzmL6vtnx"] == "No":
                dictionary[baseLineElement['id']] = ""

            #DSBS-35 : NAAT Results (Baseline)
            elif baseLineElement['id'] == "pD0tc8UxyGg":
                if dictionary["f0S6DIqAOE5"] == "Yes":
                    dictionary[baseLineElement['id']] = "MTB detected, rifampicin resistance detected"
                else:
                    dictionary[baseLineElement['id']] = "MTB detected, rifampicin resistance not detected"

            #"DSBS-12 : Started on DRTB treatment"
            elif baseLineElement['id'] == "eP1Yyb3h0ST":
                if dictionary["f0S6DIqAOE5"] == "Yes":
                    dictionary[baseLineElement['id']] = self.generateValue(enrollment, baseLineElement)
                else:
                    dictionary[baseLineElement['id']] = ""

            #"DSBS-14 : Date started on DR-TB treatment"
            elif baseLineElement['id'] == "EpvHxcDmxyT":
                if dictionary["eP1Yyb3h0ST"] == "No":
                    dictionary[baseLineElement['id']] = ""
                else:
                    dictionary[baseLineElement['id']] = getRandomDateBeforeEnrollment(enrollment)

            #"DSBS-20 : HIV status Date"
            elif baseLineElement['id'] == "Bivxg5n4goz" and dictionary["dtRfCJvzZRF"] in ["Unknown"]:
                dictionary[baseLineElement['id']] = ""

            #"DSBS-17 : ART Status"
            elif baseLineElement['id'] == "b801bG8cIxt" and dictionary["dtRfCJvzZRF"] in ["Negative", "Unknown"]:
                dictionary[baseLineElement['id']] = ""

            #"DSBS-18 : ART No"
            elif baseLineElement['id'] == "sQ4Z6lEiiq6":
                if dictionary["b801bG8cIxt"] == "":
                    dictionary[baseLineElement['id']] = ""
                else:
                    dictionary[baseLineElement['id']] = f"{uuid.uuid4()}"

            #"DSBS-19 : CPT/Dapson (Baseline)"
            elif baseLineElement['id'] == "pg6UUMn87eM" and dictionary["dtRfCJvzZRF"] in ["Negative", "Unknown"]:
                dictionary[baseLineElement['id']] = ""

            #"DSBS-22 : CPT/Dapson Initiation Date"
            elif baseLineElement['id'] == "FtWNuQmVu7j":
                if dictionary["pg6UUMn87eM"] in ["Not on CPT", ""]:
                    dictionary[baseLineElement['id']] = ""
                else:
                    dictionary[baseLineElement['id']] = getRandomDateBeforeEnrollment(enrollment)

            #"DSBS-20 : HIV status Date"
            elif baseLineElement['id'] == "Bivxg5n4goz":
                if dictionary["dtRfCJvzZRF"] == "Unknown":
                    dictionary[baseLineElement['id']] = ""
                else:
                    dictionary[baseLineElement['id']] = getRandomDateBeforeEnrollment(enrollment)

            #"DSBS-21 : ART Status Date"
            elif baseLineElement['id'] == "QcjaZKRl9D4":
                if dictionary["b801bG8cIxt"] == "":
                    dictionary[baseLineElement['id']] = ""
                else:
                    dictionary[baseLineElement['id']] = getRandomDateBeforeEnrollment(enrollment)

            #"DSBS-50 : 1st Line treatment start date"
            elif baseLineElement['id'] == "THirpMvAHgw":
                if dictionary["hDaev1EuehO"] != "New":
                    dictionary[baseLineElement['id']] = ""
                else:
                    dictionary[baseLineElement['id']] = getRandomDateBeforeEnrollment(enrollment)

            #"DSBS-51 : Extra Pulmonary TB Site"
            elif baseLineElement['id'] == "IGv6SjkM162" and dictionary["Aw9p1CCIkqL"] != "Extra pulmonary (EP) TB":
                dictionary[baseLineElement['id']] = ""

            #"DSBS-53: Date diagnosed with DRTB, "if diagnosed before"
            elif baseLineElement['id'] == "j9lDBfNNXlz":
                dictionary[baseLineElement['id']] = ""

            #"DSBS-54 Describe Lesions"
            elif baseLineElement['id'] == "jNdLczMvDPT" and dictionary["Aw9p1CCIkqL"] == "Extra pulmonary (EP) TB":
                dictionary[baseLineElement['id']] = ""

            #"DSBS-56 : CD4", "DSBS-57 : Viral Load", "DSBS-58 : ART Regimen"
            elif baseLineElement['id'] in ["Dq2CKpBrLem", "Rj4uJOP4t96", "pYsPUUxPn3v"] and dictionary["sQ4Z6lEiiq6"] == "":
                dictionary[baseLineElement['id']] = ""
            
            #"DSBS-39 : Microscopy Test Date"
            elif baseLineElement['id'] == "WoPIO7Jd8EL":
                if dictionary["x7uZB9y0Qey"] in ["Not Done", "Contaminated", "Others Specify"]:
                    dictionary[baseLineElement['id']] = ""
                else:
                    dictionary[baseLineElement['id']] = getRandomDateBeforeEnrollment(enrollment)

            #"DSBS-56 : CD4"
            elif baseLineElement['id'] == "Dq2CKpBrLem":
                if dictionary["sQ4Z6lEiiq6"] != "":
                    dictionary[baseLineElement['id']] = random.randrange(0, 2000)
                else:
                    dictionary[baseLineElement['id']] = ""

            #"DSBS-57 : Viral Load"
            elif baseLineElement['id'] == "Rj4uJOP4t96":
                if dictionary["sQ4Z6lEiiq6"] != "":
                    baseLineElement['id'] = random.randrange(0, 2000)
                else:
                     baseLineElement['id'] = ""

            #"DSTX-41 : Weight (kg) (TB Baseline Vitals)"
            elif baseLineElement['id'] == "dfNv7RZKIml":
                dictionary[baseLineElement['id']] = random.randrange(40, 190)

            #"DSTX-42 : Height (cm) (TB Baseline Vitals)"
            elif baseLineElement['id'] == "XwVhny4B7EV":
                dictionary[baseLineElement['id']] = random.randrange(140, 190)

            #"DSTX-44 : MUAC (TB Baseline Vitals)"
            elif baseLineElement['id'] == "XHkluF3EAg0":
                dictionary[baseLineElement['id']] = random.randrange(15, 30)

            #"DSTX-45 : HB (TB Baseline Vitals)"
            elif baseLineElement['id'] == "uIlwmJ26a6N":
                dictionary[baseLineElement['id']] = random.randrange(5, 14)

            #"DSTX-46 : BP (TB Baseline Vitals)"
            elif baseLineElement['id'] == "R0uqGCHWq4M":
                dictionary[baseLineElement['id']] = f"{random.randrange(90, 200)}/{random.randrange(50, 80)}"

            #"DSTX-49 : Temperature (TB Baseline Vitals)"
            elif baseLineElement['id'] == "CpNmdkKzz8O":
                dictionary[baseLineElement['id']] = random.randrange(35, 38)

            else:
                value = self.generateValue(enrollment, baseLineElement)
                dictionary[baseLineElement['id']] = value
        

        for element_id, value in dictionary.items():
            if value != "":
                dataValues.append({"dataElement" : element_id, "value" : value})


        return dataValues    





















def main():
    baselineDataSynthesizer = BaselineDataSynthesizer()
    enrollments = getEnrollments()
    trackedEntityInstances = []

    for enrollment in enrollments:
        newInstance = {
            "trackedEntityInstance" : enrollment["trackedEntityInstance"],
            "trackedEntityType"     : "MCPQUTHX1Ze",
            "orgUnit"               : enrollment["orgUnit"],
            "attributes"            : [],

            "enrollments"           : [
                {
                    "enrollment"    : enrollment["enrollment"],
                    "program"       : enrollment["Program"],
                    "status"        : "ACTIVE",
                    "orgUnit"       : enrollment["orgUnit"],
                    "incidentDate"  : enrollment["incidentDate"],
                    "enrollmentDate": enrollment["enrollmentDate"],

                    "events"        : [
                        {
                            "event"         : "EVENT_ID_1",
                            "programStage"  : "o9dq0aBejXc",
                            "orgUnit"       : "GuJvMV22ihs",
                            "eventDate"     : enrollment["incidentDate"],
                            "status"        : "COMPLETED",

                            "dataValues"    : baselineDataSynthesizer.Synthesize(enrollment),
                        },
                    ],
                },
            ],
        }


        
        trackedEntityInstances.append(newInstance)

    data = {"trackedEntityInstances" : trackedEntityInstances}
    f = open('Output.json', 'a')
    json.dump(data, f)
    f.close()
    

if "__main__":
    main()