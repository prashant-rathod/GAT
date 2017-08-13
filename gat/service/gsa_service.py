import json
import csv

from gat.gsa.misc import util, map_generator

#TODO utilize temp dir

def tempParseGSA(GSA_file_CSV, GSA_file_SHP, idVar, nameVar):
    if GSA_file_CSV == None or GSA_file_SHP == None:
        return (None, None)

    gsaCSV = []
    with open(GSA_file_CSV) as csvfile:
        try:
            reader = csv.reader(csvfile)
            for row in reader:
                tempRow = [x.replace("'", "APOSTROPHE") for x in row]
                gsaCSV.append(tempRow)
        except:
            return (None, True)

    gsaSVG = "out/generated/mymap.svg"
    map_generator.generateMap(GSA_file_SHP, gsaSVG)


    with open(gsaSVG, 'r') as myfile:
        data = None
        try:
            data = myfile.read()
        except:
            return (None, True)
    data = data.replace('"', "'")
    nameMapping = util.getNameMapping(gsaSVG, idVar, nameVar)
    nameMapping = {key : value.replace("'", "APOSTROPHE") for key, value in nameMapping.items()}
    return json.dumps(str(gsaCSV).replace('"', "'")), json.dumps(data), json.dumps(str(nameMapping).replace('"', "'"))


def parseGSA(GSA_file_CSV, GSA_file_SVG):

    if GSA_file_CSV == None or GSA_file_SVG == None:
        print("csv or svg is none")
        return (None, None)

    gsaCSV = []
    with open(GSA_file_CSV) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            gsaCSV.append(row)

    with open(GSA_file_SVG, 'r') as myfile:
        data = myfile.read()
    data = data.replace('"', "'")
    return json.dumps(gsaCSV), json.dumps(data)

def calc_ac(case_num):
    fileDict = caseDict[case_num]
    GSA_file_CSV = fileDict.get('GSA_Input_CSV')
    GSA_file_SHP = fileDict.get('GSA_Input_SHP')
    y1 = 1929
    yn = 2010
    fileDict['ac'] = {}
    for year in range(y1,yn):
        fileDict['ac'][year] = tuple(GSA_sample_autocorrelation[year-y1])
    return

GSA_sample_autocorrelation=[
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.002],
[0.001, 0.002],
[0.002, 0.003],
[0.01 ,0.005],
[0.003, 0.006],
[0.005, 0.005],
[0.004, 0.002],
[0.002, 0.003],
[0.001, 0.002],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.003, 0.001],
[0.001, 0.001],
[0.001, 0.001],
[0.002, 0.002],
[0.001, 0.003],
[0.001, 0.002],
[0.001, 0.001],
[0.002, 0.001],
[0.001, 0.001],
[0.001, 0.002],
[0.001, 0.001],
[0.001, 0.002],
[0.001, 0.001],
[0.001, 0.001],
[0.001, 0.001]]