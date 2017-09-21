caseDict = {}


def getFileDict(case_num):
    return caseDict[int(case_num)]


def updateFileDict(case_num, key, value):
    caseDict[int(case_num)][key] = value


def createFileDict(case_num):
    caseDict[int(case_num)] = {}

def setFileDict(fileDict, case_num):
    caseDict[case_num] = fileDict