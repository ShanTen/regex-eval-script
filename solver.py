import huepy
import csv
import time
import json
from halo import Halo
import regex as re


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

    caseNameA, caseNameB = getCaseNames(roundNr)
    testFileA, testFileB = getTestFileNames(roundNr)

    print(f"Evaluating Test - {caseNameA}")
    perfectSolutionA = getPerfectSolution(testConfig, caseNameA, testFileA) #returns array
    print(perfectSolutionA)

    print("-"*40)

    print(f"Evaluating Test - {caseNameB}")
    perfectSolutionB = getPerfectSolution(testConfig, caseNameB, testFileB)
    print(perfectSolutionB)
    
    return

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
        print(dataPoint)
        answersList.append(dataPoint)

    return answersList

def main():
    pathToDataSets = "./Datasets"
    pathToResponses = "./ParticipantResponses"
    global testConfig
    

    roundToEvaluate = 1
    _ = int(input("Endha round vro: "))
    roundToEvaluate = _
    
    solve(roundToEvaluate, testConfig)

    # resultCSVToObject(f"{pathToResponses}/Round2.csv")



if __name__ == '__main__':
    main()