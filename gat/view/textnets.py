import warnings
import xlrd
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, json

from gat.service import NLP_TO_NETWORK
from gat.service import file_io
from gat.dao import dao

textnets_blueprint = Blueprint('textnets_blueprint', __name__)


@textnets_blueprint.route('/textnetviz', methods=['GET', 'POST'])
def textnetviz():
    case_num = request.args.get('case_num', None)
    fileDict = dao.getFileDict(case_num)
    systemMeasures = {}
    systemMeasures["Description"] = "Description"
    return render_template("textnets_new_example.html",
                           case_num=case_num,
                           systemMeasures=systemMeasures)
