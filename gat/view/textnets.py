import warnings
import xlrd
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, json

from gat.service import NLP_TO_NETWORK
from gat.service import file_io
from gat.dao import dao
from gat.service.PythonTextnetsPort import textnetAllText
import os
textnets_blueprint = Blueprint('textnets_blueprint', __name__)


@textnets_blueprint.route('/textnetviz', methods=['GET', 'POST'])
def textnetviz():
    case_num = request.args.get('case_num', None)
    fileDict = dao.getFileDict(case_num)
    textnets_input = fileDict.get('textnets_New_Example')
    textnetAllText(csvPath=textnets_input, textColumnName='Text', groupVarColumnName='President')
    os.rename("sotu_textnet.html", "templates/sotu_textnet.html")
    systemMeasures = {}
    systemMeasures["Description"] = "Description"
    return render_template("sotu_textnet.html",
                           case_num=case_num,
                           systemMeasures=systemMeasures)
