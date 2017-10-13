from flask import Blueprint, render_template, request, redirect, url_for, jsonify

from gat.dao import dao
import subprocess
import argparse
import re

smart_search_blueprint = Blueprint('smart_search_blueprint', __name__)


@smart_search_blueprint.route('/smart_search_select', methods=['GET', 'POST'])
def sheetSelect():
    if request.method == 'GET':
        #that means a form was submitted
        case_num = request.args.get("case_num", None)
        print(case_num)
        fileDict = dao.getFileDict(case_num)
        researchQuestion = fileDict.get('research_question', None).strip()

        subprocess.call(
            'python2.7 gat/Pipeline/Project/test.py -sentence ' + researchQuestion, shell=True)

        #read sentences.txt, read in sentences, and pass the results on to  that
        sentences = ""
        with open('out/nlp/sentences', 'r') as file:
            sentences = file.readline()
        sentences = re.findall(r"'(.*?)'", sentences)
        # sentences = sentences.replace("'","")
        # sentences = sentences.replace("[","")
        # sentences = sentences.replace("]","")
        # sentenceList = sentences.split(",")
        #render sheet
        return render_template('smart_search_select.html', sentences = sentences)

    #fill in this follow example from sna_blueprint.sheet_select
    return redirect(url_for('visualize_blueprint.visualize'))

