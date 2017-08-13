from flask import Blueprint, render_template

gsa = Blueprint('gsa', __name__)

@gsa.route('/regionalization/<int:case_num>')
def reg(case_num):
    fileDict = caseDict[case_num]
    GSA_file_CSV = fileDict.get('GSA_Input_CSV')
    GSA_file_SHP = fileDict.get('GSA_Input_SHP')
    gsa_meta = fileDict.get('GSA_meta')
    svgNaming = fileDict.get('GSA_data')[0]
    with open('static/sample/GSA/mymap.svg', 'r') as myfile:
        mymap = myfile.read()

    mymap = mymap.replace('"', "'")

    observations = Weights.extractObservations(GSA_file_CSV, "ALL", gsa_meta[3])
    w = Weights.generateWeightsUsingShapefile(GSA_file_SHP, idVariable=gsa_meta[2])

    regions = Regionalization.generateRegions(w=w, observations=observations)[0]
    regions = Regionalization.getNamesFromRegions(regions)
    nameMapping = Util.getNameMapping('static/sample/GSA/mymap.svg', gsa_meta[0], gsa_meta[1])
    nameMapping = {key: value.replace("'", "APOSTROPHE") for key, value in nameMapping.items()}
    numRegs = len(set(regions.values()))
    return render_template("regionalization.html",
                           case_num = case_num,
                           mymap = json.dumps(mymap),
                           regions = json.dumps(regions),
                           numRegs = numRegs,
                           svgNaming = svgNaming,
                           nameMapping = json.dumps(str(nameMapping)))

@gsa.route("/_get_autocorrelation/<int:case_num>")
def get_autocorrelation(case_num):
    fileDict = caseDict[case_num]
    GSA_file_CSV = fileDict.get('GSA_Input_CSV')
    GSA_file_SHP = fileDict.get('GSA_Input_SHP')
    year = request.args.get('year',0,type=int)
    if year != 0:
        loc, glob = fileDict['ac'][year]
        return jsonify(year = year, loc = loc, glob = glob)
    return jsonify(year="something went wrong", loc = 0, glob = 0)