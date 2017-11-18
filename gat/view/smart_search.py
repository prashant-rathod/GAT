import time
from threading import Lock
import pandas as pd
from typing import Dict
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from gat.CameoPrediction.PredictCameo import top5CAMEO
from gat.dao import dao
from gat.service.SmartSearch.smart_search_thread import SmartSearchThread

smart_search_blueprint = Blueprint('smart_search_blueprint', __name__)

search_workers: Dict[str, SmartSearchThread] = {}


@smart_search_blueprint.route('/smart_search_select', methods=['GET', 'POST'])
def sheetSelect():
    if request.method == 'GET':
        # that means a form was submitted
        case_num = request.args.get("case_num", None)

        fileDict = dao.getFileDict(case_num)
        researchQuestion = fileDict.get('research_question', None).strip()
        sentences = top5CAMEO(researchQuestion)
        # read sentences.txt, read in sentences, and pass the results on to  that

        return render_template('smart_search_select.html', sentences=sentences)

    if request.method == 'POST':
        case_num = request.args.get('case_num', None)
        fileDict = dao.getFileDict(case_num)
        researchQuestion = fileDict.get('research_question', None).strip()
        sentences = top5CAMEO(researchQuestion)
        cameo_code = sentences[int(request.form.get('cameo', 0))]
        # Now it only works for radio button. Need to create a special case for
        # drop down menu
        articles_to_scrape = int(request.form.get('numArticlesScraped', 0))
        # Name entities is going to be subjects only
        subjects = request.form.get('name_entities', '')
        search_question = subjects + ' ' + cameo_code
        # fill in this follow example from sna_blueprint.sheet_select
        return redirect(url_for('smart_search_blueprint.landing',
                                case_num=case_num,
                                sentence=search_question,
                                article_count=articles_to_scrape))


@smart_search_blueprint.route('/landing/<case_num>/<sentence>/<article_count>', methods=['GET'])
def landing(case_num, sentence, article_count):
    new_search_thread = SmartSearchThread(search_question=sentence, article_count=article_count)
    search_workers[case_num + 'sentence' + sentence] = new_search_thread
    new_search_thread.start()
    return render_template('smart_search_landing.html')


@smart_search_blueprint.route('/progress/<case_num>/<sentence>', methods=['GET'])
def smart_search_progress(case_num, sentence):
    selected_thread = search_workers[case_num + 'sentence' + sentence]
    selected_thread.messages_lock.acquire()
    # Copy the list
    messages = list(selected_thread.messages)
    del selected_thread.messages[:]
    selected_thread.messages_lock.release()
    selected_thread.result_lock.acquire()
    if not selected_thread.result:
        selected_thread.result_lock.release()
        return jsonify(messages)
    else:
        selected_thread.result_lock.release()
        return redirect(url_for('smart_search_blueprint.results', case_num=case_num))


@smart_search_blueprint.route('/results/<casenum>/<sentence>', methods=['GET'])
def smart_search_results(case_num, sentence):
    selected_thread = search_workers[case_num + 'sentence' + sentence]
    selected_thread.result_lock.acquire()
    result = selected_thread.result
    selected_thread.result_lock.release()
