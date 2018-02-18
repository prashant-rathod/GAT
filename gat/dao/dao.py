import spacy

caseDict = {}
nlp = None


def getFileDict(case_num):
    return caseDict[int(case_num)]


def updateFileDict(case_num, key, value):
    caseDict[int(case_num)][key] = value


def createFileDict(case_num):
    caseDict[int(case_num)] = {}

def spacy_load_en():
    global nlp
    if nlp == None:
        nlp = spacy.load('en')
    return nlp