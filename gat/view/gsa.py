import json
import numpy as np
import ast

from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from gat.core.gsa.misc import util
from gat.service import gsa_service
from gat.service import io_service

from gat.core.gsa.core import weights, regionalization
from gat.dao import dao

gsa_blueprint = Blueprint('gsa_blueprint', __name__)

@gsa_blueprint.route('/gsasheet', methods=['GET', 'POST'])
def gsa_select():

    case_num = request.args.get('case_num', None)
    fileDict = dao.getFileDict(case_num)
    #csv = "usjoin.csv" if sample_path == "usa" else "IRQcasualties.csv"
    #shp = "us48.shp" if sample_path == "usa" else "IRQ_adm1.shp"

    #csv = "IRQcasualties.csv"
    csv = "IRQattacks_Oct27_GSA.csv"
    shp = "IRQ_adm1.shp"

    if 'GSA_Input_CSV' not in fileDict:
        fileDict['GSA_Input_CSV'] = url_for('static', filename="sample/gsa/" + csv)[1:]
        fileDict['GSA_Input_SHP'] = url_for('static', filename="sample/gsa/" + shp)[1:]

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

    if request.method == 'GET':
        return render_template("gsaselect.html", info=info, case_num=case_num)

    if request.method == 'POST':

        info.autoRow = request.form.get('auto-row')
        info.autoCol = ast.literal_eval(request.form.get('auto-col'))
        info.dynRow = request.form.get('dyn-row')
        #info.dynCol = ast.literal_eval(request.form.get('dyn-col'))
        info.id = request.form.get('gsa-id')
        #id = fileDict['GSA_SHP_VARS'][0]

        localAutoCorrelation, globalAutoCorrelation, spatialDynamics = gsa_service.runGSA(case_num, info.autoRow,
                                                                                          info.autoCol, info.dynRow,
                                                                                          info.dynCol, info.id)

        fileDict['GSA_data'] = ('id-1', localAutoCorrelation, globalAutoCorrelation,
                                spatialDynamics[0], spatialDynamics[1], spatialDynamics[2], spatialDynamics[3])
        #fileDict['GSA_meta'] = ('data-id-1', 'data-name-1', "NAME_1", np.arange(2014, 2017, 0.25).tolist(), fileDict['GSA_SHP_VARS'][1])
        fileDict['GSA_meta'] = ('data-id-1', 'data-name-1', "NAME_1", np.arange(2014, 2017, 0.25).tolist(), "name-1")

        return redirect(url_for('visualize_blueprint.visualize', case_num=case_num))


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

@gsa_blueprint.route('/geonet', methods=['GET', 'POST'])
def get_json():

    case_num = request.args.get('case_num', None)
    return redirect(url_for('visualize_blueprint.visualize', case_num=case_num))

@gsa_blueprint.route('/emo', methods=['GET', 'POST'])
def emotional_space():

    case_num = request.args.get('case_num', None)
    return redirect(url_for('visualize_blueprint.visualize', case_num=case_num))


@gsa_blueprint.route("/_gsa_csv", methods = ['GET'])
def upload_csv_get():
    case_num = request.args.get('case_num', None)
    fileDict = dao.getFileDict(case_num)
    GSA_file_SHP = fileDict.get('GSA_Input_SHP')
    gsaSVG = "out/gsa/mymap.svg"
    #gsa_service.generateMap(GSA_file_SHP, gsaSVG)
    nameMapping = gsa_service.getNameMapping(gsaSVG, fileDict['GSA_SHP_VARS'][1])
    return render_template("gsaUploadCsv.html", names = nameMapping)

@gsa_blueprint.route("/_gsa_csv", methods = ['POST'])
def upload_csv_post():
    case_num = request.args.get('case_num', None)
    fileDict = dao.getFileDict(case_num)
    #TODO: check for .csv extention error
    fileDict['GSA_Input_CSV'] = io_service.storefile(request.files.get('GSA_Input_CSV'))
    return redirect(url_for("gsa_blueprint.gsa_select", case_num = case_num))

@gsa_blueprint.route("/_gsa_vars", methods = ['GET'])
def shp_vars_get():
    case_num = request.args.get('case_num', None)
    fileDict = dao.getFileDict(case_num)
    possible_names = gsa_service.getColumns(fileDict['GSA_Input_DBF'])
    return render_template("gsaVars.html", id="NAME_1", names=possible_names)
    #return render_template("gsaVars.html", id = "NAME_1", name_var = "data-name-1", names = possible_names)

@gsa_blueprint.route("/_gsa_vars", methods=['POST'])
def shp_vars_post():
    case_num = request.args.get('case_num', None)
    fileDict = dao.getFileDict(case_num)
    name_var = "data-" + request.form.get('gsa-id').lower()
    fileDict['GSA_SHP_VARS'] = [request.form.get('gsa-id'), name_var]
    #fileDict['GSA_SHP_VARS'] = [request.form.get('gsa-id'), request.form.get('gsa-name-var')]
    return redirect(url_for("gsa_blueprint.upload_csv_get", case_num = case_num))
