import json

from flask import Blueprint, render_template, request, jsonify
from gat.core.gsa.misc import util

from gat.core.gsa.core import weights, regionalization
from gat.dao import dao

gsa_blueprint = Blueprint('gsa_blueprint', __name__)


@gsa_blueprint.route('/regionalization')
def reg():
    case_num = request.args.get('case_num', None)
    fileDict = dao.getFileDict(case_num)
    GSA_file_CSV = fileDict.get('GSA_Input_CSV')
    GSA_file_SHP = fileDict.get('GSA_Input_SHP')
    gsa_meta = fileDict.get('GSA_meta')
    svgNaming = fileDict.get('GSA_data')[0]
    with open('out/gsa/mymap.svg', 'r') as myfile:
        mymap = myfile.read()

    mymap = mymap.replace('"', "'")

    observations = weights.extractObservations(GSA_file_CSV, "ALL", gsa_meta[3])
    w = weights.generateWeightsUsingShapefile(GSA_file_SHP, idVariable=gsa_meta[2])

    regions = regionalization.generateRegions(w=w, observations=observations)[0]
    regions = regionalization.getNamesFromRegions(regions)
    nameMapping = util.getNameMapping('out/gsa/mymap.svg', gsa_meta[0], gsa_meta[1])
    nameMapping = {key: value.replace("'", "APOSTROPHE") for key, value in nameMapping.items()}
    numRegs = len(set(regions.values()))
    return render_template("regionalization.html",
                           case_num=case_num,
                           mymap=json.dumps(mymap),
                           regions=json.dumps(regions),
                           numRegs=numRegs,
                           svgNaming=svgNaming,
                           nameMapping=json.dumps(str(nameMapping)))


@gsa_blueprint.route("/_get_autocorrelation")
def get_autocorrelation(case_num):
    case_num = request.args.get('case_num', None)
    fileDict = dao.getFileDict(case_num)
    GSA_file_CSV = fileDict.get('GSA_Input_CSV')
    GSA_file_SHP = fileDict.get('GSA_Input_SHP')
    year = request.args.get('year', 0, type=int)
    if year != 0:
        loc, glob = fileDict['ac'][year]
        return jsonify(year=year, loc=loc, glob=glob)
    return jsonify(year="something went wrong", loc=0, glob=0)
