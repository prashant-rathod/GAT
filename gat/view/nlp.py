import warnings
import xlrd
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, json

from gat.service import NLP_TO_NETWORK
from gat.service import file_io
from gat.dao import dao


nlp_blueprint = Blueprint('nlp_blueprint', __name__)

@nlp_blueprint.route('/nlpviz', methods=['GET', 'POST'])
def jgvis():
	case_num = request.args.get('case_num', None)
	fileDict = dao.getFileDict(case_num)
	NLP_new_example_file = fileDict.get('NLP_New_Example')
	jgdata, graph = NLP_TO_NETWORK.sentiment3D(NLP_new_example_file)
	systemMeasures={}
	systemMeasures["Description"] = "Description"
	return render_template("Jgraph.html",
							jgdata=jgdata,
							graph=graph,
							case_num=case_num,
							systemMeasures=systemMeasures)