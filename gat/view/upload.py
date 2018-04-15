import random

import validators
from flask import Blueprint, render_template, request, redirect, url_for

from gat.dao import dao
from gat.service import io_service

upload_blueprint = Blueprint('upload_blueprint', __name__)


@upload_blueprint.route('/', methods=['POST'])
def upload():
    # each new "session" has a random case number associated with it
    # obviously, there is a small chance that case numbers will collide.
    # In that case, the person who used it second would overwrite the other persons data.
    # So this is not how it should be in its final version. But it's fine for now.
    case_num = request.args.get('case_num', None)

    fileDict = dao.getFileDict(case_num)

    fileDict['research_question'] = request.form.get('smartsearch')
    if fileDict['research_question'] is not None and fileDict['research_question'].strip() != '':
        if validators.url(fileDict['research_question'].strip()):
            return redirect(url_for('visualize_blueprint.visualize',
                                    case_num=case_num))  # temporary submission for SmartSearch for demo
        else:
            return redirect(url_for('smart_search_blueprint.sheetSelect',
                                    case_num=case_num))  # if its not a url take it to smartSearch input

    # here the use of fileDict is probably more clear
    # the strings used to index request.files come from the HTML name of the input field
    # see upload.html
    files = io_service.storeGSA(request.files.getlist('GSA_Input_map'))
    fileDict['GSA_Input_SHP'] = files[0] if files is not None and len(files) == 2 else None
    fileDict['GSA_Input_DBF'] = files[1] if files is not None and len(files) == 2 else None
    fileDict['GSA_Input_CSV'] = io_service.storefile(request.files.get('GSA_Input_CSV'))
    fileDict['GSA_file_list'] = request.files.getlist('GSA_Input_map')

    fileDict['NLP_Input_corpus'] = io_service.storeNLP(request.files.getlist('NLP_Input_corpus'))
    fileDict['NLP_Input_LDP'] = io_service.storefile(request.files.get('NLP_Input_LDP'))
    fileDict['NLP_Input_Sentiment'] = io_service.storefile(request.files.get('NLP_Input_Sentiment'))

    fileDict["NLP_INPUT_NER"] = request.form.get("NLP_INPUT_NER")
    fileDict["NLP_INPUT_IOB"] = request.form.get("NLP_INPUT_IOB")

    fileDict['SNA_Input'] = io_service.storefile(request.files.get('SNA_Input'))
    fileDict['GSA_Input'] = io_service.storefile(request.files.get('SGA_Input'))

    fileDict['research_question'] = request.form.get('research_question')

    errors = io_service.checkExtensions(case_num)  # helper method to make sure there are no input errors by the user
    # i.e. if there are errors, we can't proceed so we stay on the upload page
    if len(errors) > 0:
        return render_template('upload.html',
                               errors=errors, case_num=case_num)

    # there are intermediary steps for SNA and NLP analyses
    if fileDict['SNA_Input']:
        return redirect(url_for('sna_blueprint.sheetSelect', case_num=case_num))

    if fileDict['GSA_Input_CSV']:
        return redirect(url_for('gsa_blueprint.gsa_select', case_num=case_num))

    # if a user does both SNA and NLP, as it stands, the NLP intermediary data will never be gotten to. This is a problem.
    if fileDict['NLP_Input_corpus']:
        return redirect(url_for('visualize_blueprint.visualize', case_num=case_num))

    # if NLP chosen, allow them to pick from the different tools available
    # do i redirect to another url to choose then save the results then redirect to visualize?
    # no, just add the radio buttons under the file upload before the hr (in the template)
    return redirect(url_for('visualize_blueprint.visualize', case_num=case_num))


@upload_blueprint.route('/', methods=['GET'])
def landing_page():
    case_num = 100000 + random.randint(0, 100000)
    dao.createFileDict(case_num)
    print("CREATED CASE NUM: " + str(case_num))
    return render_template("upload.html", case_num=case_num)
