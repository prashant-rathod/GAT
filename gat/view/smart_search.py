from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from gat.CameoPrediction.PredictCameo import top5CAMEO

from gat.dao import dao
import subprocess
import re

smart_search_blueprint = Blueprint('smart_search_blueprint', __name__)

@smart_search_blueprint.route('/smart_search_select', methods=['GET', 'POST'])

def sheetSelect():
    if request.method == 'GET':
        #that means a form was submitted
        case_num = request.args.get("case_num", None)
        fileDict = dao.getFileDict(case_num)
        researchQuestion = fileDict.get('research_question', None).strip()
        print(researchQuestion)
        sentences = top5CAMEO(researchQuestion)
        return render_template('smart_search_select.html', sentences = sentences)

    #fill in this follow example from sna_blueprint.sheet_select
    return redirect(url_for('visualize_blueprint.visualize'))

