import numpy as np
from flask import Blueprint, redirect, url_for, request

from gat.dao import dao
from gat.service import gsa_service

sample_blueprint = Blueprint('sample_blueprint', __name__)

'''
@sample_blueprint.route('/gsa/<path:sample_path>')
def gsa_sample(sample_path):
    case_num = request.args.get('case_num', None)
    fileDict = dao.getFileDict(case_num)
    csv = "usjoin.csv" if sample_path == "usa" else "IRQcasualties.csv"
    shp = "us48.shp" if sample_path == "usa" else "IRQ_adm1.shp"
    fileDict['GSA_Input_CSV'] = url_for('static', filename="sample/gsa/" + csv)[1:]
    fileDict['GSA_Input_SHP'] = url_for('static', filename="sample/gsa/" + shp)[1:]
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
        # TODO: take in years and file names instead of hard coding
        # TODO: reorganize use of gsa_meta

        localAutoCorrelation, globalAutoCorrelation, spatialDynamics = gsa_service.runGSA(case_num, "ALL", ["2014.0"],
                                                                                          "ALL",
                                                                                          np.arange(2014, 2017,
                                                                                                    0.25).tolist(),
                                                                                          "NAME_1")
        fileDict['GSA_data'] = ('id-1', localAutoCorrelation, globalAutoCorrelation,
                                spatialDynamics[0], spatialDynamics[1], spatialDynamics[2], spatialDynamics[3])
        fileDict['GSA_meta'] = (
            'data-id-1', 'data-name-1', "NAME_1", np.arange(2014, 2017, 0.25).tolist(), "name-1")
    return redirect(url_for('visualize_blueprint.visualize', case_num=case_num))

'''

@sample_blueprint.route('/gsa/<path:sample_path>')
def gsa_sample(sample_path):
    case_num = request.args.get('case_num', None)
    fileDict = dao.getFileDict(case_num)
    fileDict['GSA_Input'] = url_for('static', filename="sample/sna/" + sample_path)[1:]
    return redirect(url_for('gsa_blueprint.gsa_select', case_num=case_num))

@sample_blueprint.route('/nlp/<path:sample_path>')
def nlp_sample(sample_path):
    case_num = request.args.get('case_num', None)
    fileDict = dao.getFileDict(case_num)
    if sample_path == 'iran':
        fileDict['NLP_Input_Sentiment'] = 'static/sample/nlp/sample_sentiment.txt'
    else:
        fileDict['NLP_Input_corpus'] = url_for('static', filename="sample/nlp/" + sample_path + '/')[1:]
    return redirect(url_for('visualize_blueprint.visualize', case_num=case_num))


@sample_blueprint.route('/sna/<path:sample_path>')
def sna_sample(sample_path):
    case_num = request.args.get('case_num', None)
    fileDict = dao.getFileDict(case_num)
    fileDict['SNA_Input'] = url_for('static', filename="sample/sna/" + sample_path)[1:]
    return redirect(url_for('sna_blueprint.sheetSelect', case_num=case_num))
