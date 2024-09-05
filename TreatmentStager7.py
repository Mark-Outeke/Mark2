import json
import random
import uuid
from datetime import datetime, timedelta

#################################################################################################
# Utility functions
#################################################################################################

def getEvents():
    file = open('output.json')
    eventData = json.load(file)
    file.close()
    return eventData["events"]

def getTreatmentElements():
    file = open('TreatmentElements.json')
    treatmentElements = json.load(file)
    file.close()
    return treatmentElements

def getValueByID(dataValues = [], elementId = ""):
    for dataValue in dataValues:
        if elementId == dataValue["dataElement"]:
            return dataValue["value"]
    
    return ""

def generateTreatmentStageDate(baselineEvent, monthOfTreatment):
    #calcualte the date from incidentdate to the month of treatment and 
    # and generate the treatmentstage date .

    monthOfTreatmentToDays = {
        "1-2 Weeks" : 0,
        "3-4 Weeks" : 14,
        "5-6 Weeks" : 28,
        "7-8 Weeks" : 42 ,
        "Month 3"   : 56,
        "Month 4"   : 84,
        "Month 5"   : 112,
        "Month 6"   : 140,
        "Month 7"   : 168,
        "Month 8"   : 196,
        "Month 9"   : 224,
        "Month 10"  : 252,
        "Month 11"  : 280,
        "Month 12"  : 308
    }



    date = datetime.fromisoformat(baselineEvent["eventDate"]) + timedelta(
        days = monthOfTreatmentToDays[monthOfTreatment])
    
    return date.isoformat()


def getRegimen(typeOfPatient, monthOfTreatment, isExtraPulmonary):

    if monthOfTreatment in ["1-2 Weeks", "3-4 Weeks", "5-6 Weeks", "7-8 Weeks"]:
        return "RHZE"

    elif monthOfTreatment in ["Month 3", "Month 4", "Month 5", "Month 6"]:
        return "RH"

    elif monthOfTreatment in ["Month 7", "Month 8", "Month 9", "Month 10"]:
        if isExtraPulmonary or (typeOfPatient == "Treatment after failure"):
            return "RH"
        else:
            return ""

    elif monthOfTreatment in ["Month 11", "Month 12"] and isExtraPulmonary:
        return "RH"

    else:
        return ""

def getNumberOfDaysToDispense(monthOfTreatment):
    if monthOfTreatment in ["1-2 Weeks", "3-4 Weeks", "5-6 Weeks", "7-8 Weeks"]:
        return 14

    elif monthOfTreatment in [
        "Month 3", "Month 4", "Month 5", "Month 6",
        "Month 7", "Month 8", "Month 9", "Month 10",
        "Month 11", "Month 12"]:

        return 28

    else:
        return 0

def getPillCount(weight, numberOfDays):
    if weight in range(25, 40):
        return 2 * numberOfDays 

    elif weight in range(40, 55):
        return 3 * numberOfDays

    elif weight in range(55, 70):
        return 4 * numberOfDays

    elif weight >= 70:
        return 5 * numberOfDays

    else:
        return 0


def getNumberOfBlisterPacks(weight, monthOfTreatment):
    pillCount = getPillCount(weight, getNumberOfDaysToDispense(monthOfTreatment))
    pillsPerPack = 28;

    return (pillCount / pillsPerPack)


def getNutritionalStatusFromBMI(bmi):
    if bmi < 17.0:
        return "Severe Acute Malnutrition"

    elif bmi < 18.5:
        return "Moderate Acute Malnutrition"

    elif bmi >= 30.0:
        return "Obese"

    elif bmi >=25.0:
        return "Overweight"

    else:
        # (18.5 to 24.9) NormalWeight
        return ""
    
def getDataElementIdToOptionMap():
    file = open('DataElementIdToOptionMapping.json')
    dataElementIdToOptionMap = json.load(file)
    file.close()
    return dataElementIdToOptionMap

#################################################################################################
















class TreatmentDataSynthesizer:
    def __init__(self):
        self.treatmentElements = getTreatmentElements()
    
    def SynthesizeDataValues(self, baselineEvent, monthOfTreatment):

        baselineDataValues = baselineEvent["dataValues"]
        stageDataValues = []        

        isDrugResistant = (getValueByID(baselineDataValues,"f0S6DIqAOE5") == "Yes")

        if isDrugResistant:
            return []


        typeOfPatient = getValueByID(baselineDataValues, "hDaev1EuehO")

        regimen = getRegimen(typeOfPatient, monthOfTreatment, (
            getValueByID(baselineDataValues, "Aw9p1CCIkqL") == "Extra pulmonary (EP) TB"))

        if regimen == "":
            return []

        
        for treatmentElement in self.treatmentElements:
            match treatmentElement['id']:
                case "Aw9p1CCIkqL":
                    
                    value = getValueByID(baselineDataValues, "Aw9p1CCIkqL")

                    stageDataValues.append({
                        "dataElement" : treatmentElement['id'],
                        "value" : value
                        })

                #"dataElement": "DS: Month of Treatment"
                case "U4jSUZPF0HH":
                    stageDataValues.append({
                        "dataElement" : treatmentElement['id'],
                        "value" : monthOfTreatment
                        })

                case "xcTT5oXggBZ":
                #"dataElement": "DSTX-02 : Weight  (kg)"
                    value = getValueByID(baselineDataValues, "dfNv7RZKIml");

                    stageDataValues.append({
                        "dataElement" : treatmentElement['id'],
                        'value': value}
                    )


                case "WBsNDNQUgeX":
                    #"dataElement": "DSTX-03 : Height "
                    value = getValueByID(baselineDataValues, "XwVhny4B7EV");
                    
                    stageDataValues.append({
                        "dataElement" : treatmentElement['id'],
                        'value': value}
                    )

                #"dataElement": "DSTX-04 : MUAC Code"
                case "E0oIYbS2lcV":
                    value = getValueByID(baselineDataValues,  "XHkluF3EAg0");
                    
                    stageDataValues.append({
                        "dataElement" : treatmentElement['id'],
                        'value': value}
                    )

                #"dataElement": "DSTX-05 : BMI"
                case "HzhDngURGLk":
                    weight = int(getValueByID(stageDataValues, "xcTT5oXggBZ"));
                    height = int(getValueByID(stageDataValues, "WBsNDNQUgeX"));

                    value = f"{(weight * 10000) // (height * height)}"
                    
                    stageDataValues.append({
                        "dataElement" : treatmentElement['id'],
                        'value': value}
                    )

                #dataElement": "DSTX-12 : Suspected Adverse Event Drug Causing",
                case "DrbIE582o34":
                    pass


                #"dataElement": " DSTX-77: Assessed for Malnutrition at the last visit during the reporting quarter?"
                case "fOnOoUvD03d":
                    value = random.choice(["Yes", "No"])
                    
                    stageDataValues.append({
                        "dataElement" : treatmentElement['id'],
                        'value': value}
                    )

                #"dataElement": "DSBS-43 : Date Test Done"
                case "kvQ0Wz3ZqFr":
                    #TODO
                    pass

                #"dataElement": "DSLT-01 : Type of Test"
                case "t1wRW4bpRrj":
                    #TODO
                    if getValueByID(eventData, ["x7uZB9y0Qey",
                                                "pD0tc8UxyGg",
                                                "e0mTEFrXZDh",
                                                "LRzaAyb2vGk"]): 
                                                 
                                                

                        value = getDataElementIdToOptionMap(baselineDataValues, options[""]);
                    
                        stageDataValues.append({
                            "dataElement" : treatmentElement['id'],
                            'value': value}
                        )
                    

                #"dataElement": "DSLT-12 : Follow up lab Results"
                case "WTz4HSqoE5E":
                    #TODO
                    pass


                #"dataElement": "DSTX-27 : Adverse Event reported during the visit"
                case "sM7PAEYRqEP":
                    pass

                #"dataElement": "DSTX-28: Treatment Model"
                case "pDoTShM62yi":
                    value = random.choices(
                        ["Facility DOT",
                         "Digital Community DOT",
                         "Non-Digital Community DOT"],

                        weights=[0.00005, 0.00005, 0.9999])[0]
                    
                    stageDataValues.append({
                        "dataElement" : treatmentElement['id'],
                        'value': value}
                    )



                #"dataElement": "DSTX-29: RHZE(150/75/400/275 mg) given"
                case "FklL99yLd3h":
                    if regimen == "RHZE":
                        
                        value = "Yes"

                        stageDataValues.append({
                            "dataElement" : treatmentElement['id'],
                            'value': value}
                        )                    

                #"dataElement": "DSTX-30: RH (150/75mg) given"
                case "QzfjeqlwN2c":
                    if regimen == "RH":
                        
                        value = "Yes"

                        stageDataValues.append({
                            "dataElement" : treatmentElement['id'],
                            'value': value}
                        )

                #children
                #"dataElement": "DSTX-31: RHZ (75/50/150mg) given"
                case "pZgD6CYOa96":
                    pass
                #"dataElement": "DSTX-32: RH (75/50 mg) given"
                case "TevjEqHRBdC":
                    pass






                #ignore
                #"dataElement": "DSTX-33: Ethambutol (100mg) given"
                case "EWsKHldwJxa":
                    pass




                #"dataElement": "DSTX-35: RHZE(150/75/400/275 mg) blisters given"
                case "Ghsh3wqVTif":
                    if regimen == "RHZE":
                        
                        weight = int(getValueByID(stageDataValues, "xcTT5oXggBZ"))

                        value = f"{getNumberOfBlisterPacks(weight, monthOfTreatment)}"

                        stageDataValues.append({
                            "dataElement" : treatmentElement['id'],
                            'value': value}
                        )



                #"dataElement": "DSTX-36: RH (150/75mg) blisters given"
                case "vZMCHh6nEBZ":
                    if regimen == "RH":
                        
                        weight = int(getValueByID(stageDataValues, "xcTT5oXggBZ"))

                        value = f"{getNumberOfBlisterPacks(weight, monthOfTreatment)}"

                        stageDataValues.append({
                            "dataElement" : treatmentElement['id'],
                            'value': value}
                        )




#############################################################################################
                #Note: These are paediatric Drugs & Dosages so we skip because we are
                #dealing with 18+ years of age

                #"dataElement": "DSTX-37: RHZ (75/50/150mg) blisters given"
                case "LyiHJrtjNTX":
                    pass

                #"dataElement": "DSTX-38: RH (75/50 mg) blisters given"
                case "muBnQUtbS9R":
                    pass

                #"dataElement": "DSTX-39: Ethambutol (100mg) blisters given"
                case "wpV8b2x6uDP":
                    pass
#############################################################################################










                #"dataElement": "DSTX-43 : Oedema"
                case "aNj8BNicATN":
                    value = random.choice(["No Oedema", "+", "++", "+++"])
                    
                    stageDataValues.append({
                        "dataElement" : treatmentElement['id'],
                        'value': value}
                    )

                #"dataElement": "DSTX-45 Nutrition Status"
                case "Jl3oWFGGt1U":
                    #TODO: Use BMI CutOffs
                    
                    bmi = int(getValueByID(stageDataValues, "HzhDngURGLk"))
                    value = getNutritionalStatusFromBMI(bmi)

                    if value != "":
                        stageDataValues.append({
                            "dataElement" : treatmentElement['id'],
                            'value': value}
                        )                        


                #"dataElement": "DSTX-46 Nutrition Support Provided"
                case "YwZN88UJ98d":
                    if getValueByID(stageDataValues, "Jl3oWFGGt1U") in [
                        "Severe Acute Malnutrition", 
                        "Moderate Acute Malnutrition"]:

                        value = random.choice([
                            "Nutrition Counselling",
                            "Referral",
                            "Therapeutic foods",
                            "Supplementary Foods"])
                        
                        stageDataValues.append({
                            "dataElement" : treatmentElement['id'],
                            'value': value}
                        )
                    else:
                        pass














                #"dataElement": "DSTX-47 : FBS (TB Baseline Vitals)"
                case "OjPmMe220KO":
                    pass

                #"dataElement": "DSTX-47 : INR No."
                case "FbAAnGS1hMd":
                    pass

                #"dataElement": "DSTX-48 : RBS (TB Baseline Vitals)"
                case "CXUI1Yrr9gd":
                    pass

                #"dataElement": "DSTX-57 : OGTT"
                case "SaUrKUfG5sq":
                    pass

                #"dataElement": "DSTX-59 : Diabetes Status"
                case "nVaN4Cpoe9Z":
                    value = random.choices(
                        ["New DM (NDM)", "Known DM (KDM)", ""],

                        weights = [0.0001, 0.0001, 0.9998])[0]
                    
                    stageDataValues.append({
                        "dataElement" : treatmentElement['id'],
                        'value': value}
                    )

                #"dataElement": "DSTX-71 : Mental Health Diagnosis"
                case "AfgbZ88OenB":
                    pass

                #"dataElement": "DSTX-72 : Mental Health Treatment"
                case "w8g4nfzSSkl":
                    pass



                #"dataElement": "DSTX-73 : DSD Model"
                case "sVFokCQ8LTV":
                    value = "IMF"
                    
                    stageDataValues.append({
                        "dataElement" : treatmentElement['id'],
                        'value': value}
                    )

                #"dataElement": "DSTX-75 : Number of contacts illicited"
                case "p7VnF86krhW":
                    pass

                #"dataElement": "DSTX-76 : Date recorded in in contact tracing register"
                case "fwrDFvuQXJf":
                    pass

                #"dataElement": "DSTX-78: Malnourished at the last visit"
                case "OxiGxyWZtZh":
                    pass
















                case _:
                    #"dataElement": "DSTX-11 : Adverse Event Gastrointestinal"
                    # case "rluc10OPm1I"
                    #"dataElement": "DSTX-13 : Adverse Event Hepatotoxicity"
                    # case "F5P1buF4RHP"
                    #"dataElement": "DSTX-14 : Adverse Event Musculoskeletal"
                    # case "UtGpqsuTmrD"
                    #"dataElement": "DSTX-15 : Adverse Event Renal toxicity"
                    # case "rHEeM6ha268"
                    #"dataElement": "DSTX-16 : Adverse Event Vestibular/Ototoxicity"
                    # case "DHPzkmTcDUv"
                    #"dataElement": "DSTX-17 : Adverse Event Vision changes"
                    # case "RTKE58980U7"
                    #"dataElement": "DSTX-18 : Adverse Event Neuropathy"
                    # case "luQQ9zNTgFM"
                    #"dataElement": "DSTX-19 : Adverse Event Psychiatric"
                    # case "k5LrUGjAGD5"
                    #"dataElement": "DSTX-20 : Adverse Event Hypothyroid"
                    # case "EDFvw8DsJuH"
                    #"dataElement": "DSTX-21 : Adverse Event Dysglycemia"
                    # case "Wbp0DL9fQYj"
                    #"dataElement": "DSTX-22 : Adverse Event Dermatologic"
                    # case "pDR49oOtJrc"
                    #"dataElement": "DSTX-23 : Adverse Event Cardiovascular"
                    # case "mDmVRrzihu0"
                    #"dataElement": "DSTX-24 : Adverse Event Hematological"
                    # case "KAykkHp1p2F"
                    #"dataElement": "DSTX-25 : Adverse Event New onset Seizure"
                    # case "EoO16H5lLK5"
                    #"dataElement": "DSTX-26 : Adverse Event Electrolyte Abnormality"
                    # case "lpJPqjVUToo"
                    #"dataElement": "DSTX-X : Burning sensation in the feet"
                    # case "ywUNEl0vi3Y"
                    #"dataElement": "DSTX-X : Deafness"
                    # case "XzNqEEXo00j"
                    #"dataElement": "DSTX-X : dermatitis"
                    # case "Ep0hN5HdQKS"
                    #"dataElement": "DSTX-X : Dizziness"
                    #"dataElement": "DSTX-X : Flu syndrome"
                    # case "OZkvrZWZL0u"
                    #"dataElement": "DSTX-X : Hepatitis"
                    # case "H85OvvFGG6i"
                    #"dataElement": "DSTX-X : Jaundice"
                    # case "P9DY4UW3BTo"
                    #"dataElement": "DSTX-X : Joint pains"
                    # case "iUyb0JGgeqn"
                    #"dataElement": "DSTX-X : Low appetite nausea abdominal pain"
                    # case "vvlAUOFU1lc"
                    #"dataElement": "DSTX-X : Mental confusion"
                    # case "omFhxVHAHW8"
                    #"dataElement": "DSTX-X : nystagmus"
                    # case "hZ4HR3lEOWm"
                    #"dataElement": "DSTX-X : peripheral neuropathy"
                    # case "G0m1TnJ9CaB"
                    #"dataElement": "DSTX-X : reddish-brown coloration of urine"
                    # case "fhEVXFPNNUc"
                    #"dataElement": "DSTX-X : Skin rash"
                    # case "cdGuoKHI3fp"
                    #"dataElement": "DSTX-X : vertigo"
                    # case "WLqYnkV6qx1"
                    #"dataElement": "DSTX-X : Visual impairment"
                    # case "P6eKotYRIvT"
                    value = random.choices(
                        ["Mild", "Moderate", "Severe", "Life threatening", "No side effects"],
                        weights = [0.148, 0.05, 0.001, 0.001, 0.80])[0]
                    
                    stageDataValues.append({
                        "dataElement" : treatmentElement['id'],
                        'value': value}
                    )


        return stageDataValues




def main():
    synthesizer = TreatmentDataSynthesizer()
    
    baselineEvents = getEvents()
    

    monthOfTreatments = (
      "1-2 Weeks",
      "3-4 Weeks",
      "5-6 Weeks",
      "7-8 Weeks",
      "Month 3",
       "Month 4",
       "Month 5",
       "Month 6",
       "Month 7",
    #   "Month 8",
    #   "Month 9",
    #   "Month 10",
    #   "Month 11",
    #   "Month 12"
    )



    for monthOfTreatment in monthOfTreatments:
        
        print(f"Synthesizing Events for TreatmentMonth {monthOfTreatment}")
        stageEvents = []

        for baselineEvent in baselineEvents:
            

            dataValues = synthesizer.SynthesizeDataValues(baselineEvent,  monthOfTreatment)

            if len(dataValues) == 0:
                continue        


            else:
                
                eventDate = generateTreatmentStageDate(baselineEvent, monthOfTreatment)


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
        f = open(f'{monthOfTreatment} treatmentStageOutputtest.json', 'w')
        json.dump(data, f)
        f.close()
        
    
if "__main__":
    main()