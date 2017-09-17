import json
import numpy as np

from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from gat.core.gsa.misc import util
import xlrd
from gat.service import gsa_service

from gat.core.gsa.core import weights, regionalization
from gat.dao import dao

gsa_blueprint = Blueprint('gsa_blueprint', __name__)

@gsa_blueprint.route('/gsasheet', methods=['GET', 'POST'])
def gsa_select():
    case_num = request.args.get('case_num', None)
    fileDict = dao.getFileDict(case_num)
    #csv = "usjoin.csv" if sample_path == "usa" else "IRQcasualties.csv"
    #shp = "us48.shp" if sample_path == "usa" else "IRQ_adm1.shp"

    csv = "IRQcasualties.csv"
    shp = "IRQ_adm1.shp"

    fileDict['GSA_Input_CSV'] = url_for('static', filename="sample/gsa/" + csv)[1:]
    fileDict['GSA_Input_SHP'] = url_for('static', filename="sample/gsa/" + shp)[1:]

    '''
    if sample_path == "usa":
        localAutoCorrelation, globalAutoCorrelation, spatialDynamics = gsa_service.runGSA(case_num, "ALL", [2008],
                                                                                          "ALL",
                                                                                          list(range(1979, 2009)),
                                                                                          "STATE_NAME")
        fileDict['GSA_data'] = ('id-1', localAutoCorrelation, globalAutoCorrelation,
                                spatialDynamics[0], spatialDynamics[1], spatialDynamics[2], spatialDynamics[3])
        fileDict['GSA_meta'] = (
            'data-state-id', 'data-state-name', "STATE_NAME", list(range(1979, 2009)), "state-name")
    else:
    '''
    # TODO: take in years and file names instead of hard coding
    # TODO: reorganize use of gsa_meta

    class Input:
        def __init__(self, autoRow, autoCol, dynRow, dynCol, id):
            self.autoRow = autoRow
            self.autoCol = autoCol
            self.dynRow = dynRow
            self.dynCol = dynCol
            self.id = id

    info = Input("ALL", ["2014.0"], "ALL", np.arange(2014, 2017, 0.25).tolist(), "NAME_1")


    localAutoCorrelation, globalAutoCorrelation, spatialDynamics = gsa_service.runGSA(case_num, info.autoRow, info.autoCol,
                                                                                      info.dynRow,
                                                                                      info.dynCol,
                                                                                      info.id)
    fileDict['GSA_data'] = ('id-1', localAutoCorrelation, globalAutoCorrelation,
                            spatialDynamics[0], spatialDynamics[1], spatialDynamics[2], spatialDynamics[3])
    fileDict['GSA_meta'] = (
        'data-id-1', 'data-name-1', "NAME_1", np.arange(2014, 2017, 0.25).tolist(), "name-1")


    if request.method == 'POST':
        return redirect(url_for('visualize_blueprint.visualize', case_num=case_num))

    # if workbook only has one sheet, the user shouldn't have to specify it
    return render_template("gsaselect.html", info=info, case_num=case_num)

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
