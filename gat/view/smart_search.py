from io import StringIO
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, Response
from gat.CameoPrediction.PredictCameo import top5CAMEO
from gat.dao import dao
from gat.service.SmartSearch.smart_search_thread import SmartSearchThread

smart_search_blueprint = Blueprint('smart_search_blueprint', __name__)
search_workers = {}


@smart_search_blueprint.route('/smart_search_select', methods=['GET', 'POST'])
def sheetSelect():
    # case_num = None
    case_num = request.args.get("case_num", None)

    if request.method == 'GET':
        # that means a form was submitted
        case_num = request.args.get("case_num", None)

        fileDict = dao.getFileDict(case_num)
        researchQuestion = fileDict.get('research_question', None).strip()
        sentences = top5CAMEO(researchQuestion)
        # read sentences.txt, read in sentences, and pass the results on to  that
        cameoCodes = []
        with open("static/resources/smartsearch/cameocodes.txt", 'r') as file:
            for line in file:
                cameoCodes.append(line)

        return render_template('smart_search_select.html', sentences=sentences, cameoCodes=cameoCodes)

    if request.method == 'POST':
        case_num = request.args.get('case_num', None)
        fileDict = dao.getFileDict(case_num)
        researchQuestion = fileDict.get('research_question', None).strip()
        sentences = top5CAMEO(researchQuestion)
        if request.form.get('cameo') != 'SeeDropdown':
            cameo_code = sentences[int(request.form.get('cameo', 0))]
        else:
            cameo_code = request.form.get('cameos', '')
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
    return render_template('smart_search_landing.html',
                           case_num=case_num,
                           sentence=sentence)


@smart_search_blueprint.route('/progress/<case_num>/<sentence>', methods=['GET'])
def smart_search_progress(case_num, sentence):
    selected_thread = search_workers[case_num + 'sentence' + sentence]
    selected_thread.messages_lock.acquire()
    # Copy the list
    messages = list(selected_thread.messages)
    selected_thread.messages_lock.release()
    selected_thread.result_ontology_lock.acquire()
    result_ontology = selected_thread.result_ontology
    selected_thread.result_ontology_lock.release()
    if result_ontology is not None:
        messages.append('###FINISHED###')
    return jsonify(messages)


@smart_search_blueprint.route('/results/<case_num>/<sentence>', methods=['GET'])
def smart_search_results(case_num, sentence):
    selected_thread = search_workers[case_num + 'sentence' + sentence]
    selected_thread.result_lock.acquire()
    result_df = selected_thread.result
    selected_thread.result_lock.release()
    if result_df is not None:
        # Create a new buffer, let pandas to write to that buffer,
        # then set the start pos of the buffer to zero.
        # Finally, get the string value from the buffer.
        # Return the string, but set content as attachment, and then set filename.
        result_buffer = StringIO()
        result_df.to_csv(result_buffer, encoding='utf-8')
        result_buffer.seek(0)
        return Response(result_buffer.getvalue(),
                        mimetype='text/csv',
                        headers={'Content-disposition':
                                     'attachment; filename=' + case_num + '_result.csv'}
                        )
    else:
        return Response('Analysis Not Finished', content_type='text/plain')


@smart_search_blueprint.route('/results_ontology/<case_num>/<sentence>', methods=['GET'])
def smart_search_ontology_results(case_num, sentence):
    selected_thread = search_workers[case_num + 'sentence' + sentence]
    selected_thread.result_ontology_lock.acquire()
    result_df = selected_thread.result_ontology
    selected_thread.result_ontology_lock.release()
    if result_df is not None:
        result_buffer = StringIO()
        result_df.to_csv(result_buffer, encoding='utf-8')
        result_buffer.seek(0)
        return Response(result_buffer.getvalue(),
                        mimetype='text/csv',
                        headers={'Content-disposition':
                                     'attachment; filename=' + case_num + '_ontology_result.csv'}
                        )
    else:
        return Response('Analysis Not Finished', content_type='text/plain')
