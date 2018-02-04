import warnings
import xlrd
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, json

from gat.service import NLP_TO_NETWORK, NLP_OTHER
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

@nlp_blueprint.route('/nlp2d', methods=['GET', 'POST'])
def sent():
	type = request.args.get('type', 0, type=str)
	print(type)
	case_num = request.args.get('case_num', None)
	fileDict = dao.getFileDict(case_num)
	NLP_new_example_file = fileDict.get('NLP_New_Example')
	filename = ''
	if(type == "tab-five"):
		filename = NLP_TO_NETWORK.sentiment_mining(NLP_new_example_file)
	elif (type == "tab-four"):
		filename = NLP_TO_NETWORK.relationship_mining(NLP_new_example_file)
	elif (type == "tab-six"):
		filename = NLP_OTHER.wordcloud(NLP_new_example_file)
	elif (type == "tab-seven"):
		filename = NLP_OTHER.stemmerize(NLP_new_example_file)
	elif (type == "tab-eight"):
		filename = NLP_OTHER.lemmatize(NLP_new_example_file)
	elif (type == "tab-nine"):
		filename = NLP_OTHER.abstract(NLP_new_example_file)
	elif (type == "tab-ten"):
		filename = NLP_OTHER.top20_verbs(NLP_new_example_file)
	elif (type == "tab-eleven"):
		filename = NLP_OTHER.top20_persons(NLP_new_example_file)
	elif (type == "tab-twelve"):
		filename = NLP_OTHER.top20_locations(NLP_new_example_file)
	elif (type == "tab-thirteen"):
		filename = NLP_OTHER.top20_organizations(NLP_new_example_file)
	elif (type == "tab-fourteen"):
		filename = NLP_OTHER.sentence_sentiment_distribution(NLP_new_example_file)
	return jsonify(result=filename)