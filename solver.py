import huepy
import csv
import time
import json
from halo import Halo
import regex as re
from tabulate import tabulate

testConfig = {
    "SR-1A" : {
        "rightCount":  10,
        "totalCount": 20,
        "solution":r'\b[a-zA-Z]{3}-\d{4}\b'
    },
    "SR-1B" : {
        "rightCount":  10,
        "totalCount": 20,
        "solution":r"^([\w\.\-]+)@([\w\-]+)((\.(\w+))+)$"
    },
    "SR-2A":{
        "rightCount":  10,
        "totalCount": 20,
        "solution": r"\b(orange|purple|strong)-(monkey|bike|bin|elephant)\b"
    },
    "SR-2B":{
        "rightCount":  10,
        "totalCount": 20,
        "solution": r"\bA[0-9]{4}[A-Z]{2}|A[0-9]{4}-[A-Z]{2}|B[0-9]{3}[a-z]{3}|B[0-9]{3}_[a-z]{3}\b"
    },
    "SR-3A":{
        "rightCount":  20, #update later
        "totalCount": 30,
        "solution": "(?<=^set CUTIL_)[A-Z]*(?==)"
    },
    "SR-3B":{
        "rightCount":  20, #update later
        "totalCount": 30,
        "solution": r'(?<=\b[iI][dD]\W*=\W*["\'])[a-zA-Z0-9_-]+(?=["\'])'
    }
}

@Halo(text='Validating Results...\n', spinner='dots')
def solve(roundNr : int, testConfig):
    time.sleep(1)

    toPrint = []

    pathToResponses = "./ParticipantResponses"

    caseNameA, caseNameB = getCaseNames(roundNr)
    testFileA, testFileB = getTestFileNames(roundNr)

    participantAnswersForRound = resultCSVToObject(f"{pathToResponses}/Round{roundNr}.csv")
    formattedParticipantAnswers = formatParticipantAnswers(participantAnswersForRound, roundNr)

    # print(formattedParticipantAnswers)
    
    print(f"Evaluating Test - {caseNameA}")
    perfectSolutionA = getPerfectSolution(testConfig, caseNameA, testFileA) #returns array
    for participant in formattedParticipantAnswers:
        participantSolution = getParticipantSolution(participant,caseNameA, testFileA)
        print(f"Score of team {participant['TeamName']} is {compareAndGetScore(participantSolution,perfectSolutionA)}")
        participant['TotalScore'] += compareAndGetScore(participantSolution,perfectSolutionA)

    print("-"*40)

    print(f"Evaluating Test - {caseNameB}")
    perfectSolutionB = getPerfectSolution(testConfig, caseNameB, testFileB)
    # print(perfectSolutionB)
    for participant in formattedParticipantAnswers:
        # print(participant)
        participantSolution = getParticipantSolution(participant,caseNameB,testFileB)
        print(f"Score of team {participant['TeamName']} is {compareAndGetScore(participantSolution,perfectSolutionB)}")
        participant['TotalScore'] += compareAndGetScore(participantSolution,perfectSolutionB)


    for participant in formattedParticipantAnswers:
        _ = removeKeysFromObject(participant, [caseNameA, caseNameB])
        toPrint.append(_)
    
    pprintTable(toPrint)
    
    
    return

def formatParticipantAnswers(solutionList, roundNr):
    #array of objects where each object is has the following keys:
    # [
    #   'Timestamp', 
    #   'Team Name', 
    #   'College Name', 
    #   'Participant 1 name', 
    #   'Participant 2 name', 
    #   'Qn A: Enter your Regex', 
    #   'Qn B: Enter your RegEx'
    #]

    newList = []
    for idx, oldObj in enumerate(solutionList):
        newObj = dict()
        caseA, caseB = getCaseNames(roundNr)
        newObj['TeamName'] = oldObj['Team Name']
        newObj['CollegeName'] = oldObj['College Name']
        newObj[caseA] = rf"{oldObj['Qn A: Enter your Regex']}"
        newObj[caseB] = rf"{oldObj['Qn B: Enter your RegEx']}"
        newObj['TimeStampIndex'] = idx #since the solutionList is already sorted by timestamp
        newObj['TotalScore'] = 0
        newList.append(newObj)
    return newList

def getPerfectSolution(testConfig, caseName : str, testFile : str):
    settings = testConfig
    case = settings[caseName]
    pattern = case["solution"]
    finalSolution = []
    
    for line in open(testFile):
        if re.search(pattern, line):
            _ = (re.search(pattern, line).group())            
            finalSolution.append(_)

    return finalSolution

def removeKeysFromObject(object, keys):
    objKeys = object.keys()
    newKeys = []
    newObj = {}
    for k in list(objKeys):
        if k not in keys:
            newKeys.append(k)

    for k in newKeys:
        newObj[k] = object[k]

    return newObj

# question code is like SR-1A, SR-2A, SR-3A, 
def getParticipantSolution(participantObject, questionCode : str ,testFile : str):
    pattern = participantObject[questionCode]
    finalSolution = []
    try:
        for line in open(testFile):
            if re.search(pattern, line):
                _ = (re.search(pattern, line).group())            
                finalSolution.append(_)
        
        return finalSolution
    except:
        return []

def makeParticipantObject(entry):
    #participantObject
    pass

def exportToCSV(data):
    pass

#returns two test cases according to round integer
def getCaseNames(roundNr : int) -> str:
    return f'SR-{roundNr}A', f'SR-{roundNr}B'    

def getTestFileNames(roundNr : int) -> str:
    pathToDataSets = "./Datasets"
    return f'{pathToDataSets}/SR-{roundNr}ATestCases.dat', f'{pathToDataSets}/SR-{roundNr}BTestCases.dat'    

def resultCSVToObject(fname):
    with open(fname, "rt") as raw_response:
        out = csv.reader(raw_response)
        data = list(out)
        raw_response.close()

    header = data[0]
    answers = data[1:]
    answersList = []

    for ans in answers:
        dataPoint = (dict(zip(header, ans))) #object maker 
        answersList.append(dataPoint)

    return answersList

def pprintTable(answerList):
    _headers = answerList[0].keys()
    table = [_.values() for _ in answerList[1:]]
    print(tabulate(table, headers=_headers, tablefmt="fancy_grid"))

def compareAndGetScore(participantSolution, finalSolution):
    score = 0
    plusScore = 1
    minusScore = 0.2
    if len(participantSolution) == 0:
        return 0
    for string in participantSolution:
        if string in finalSolution:
            score += plusScore
        elif string not in finalSolution:
            score -= minusScore
    return score

def main():
    global testConfig
    pathToResponses = "./ParticipantResponses"
    
    _ = int(input("Endha round vro: "))
    roundToEvaluate = _

    # answerList = resultCSVToObject(f"{pathToResponses}/Round2.csv")
    
    solve(roundToEvaluate, testConfig)

if __name__ == '__main__':
    main()