import random

from flask import Blueprint, render_template, request, redirect, url_for

from gat.service import io_service

upload = Blueprint('upload', __name__)


@upload.route('/', methods=['POST'])
def upload():
    # each new "session" has a random case number associated with it
    # obviously, there is a small chance that case numbers will collide.
    # In that case, the person who used it second would overwrite the other persons data.
    # So this is not how it should be in its final version. But it's fine for now.
    caseDict[case_num] = {}

    # this fileDict is where the case data, e.g. uploaded files, are stored
    fileDict = caseDict[case_num]

    for f in request.files:
        print(str(f) + ": " + str(request.files.get(f)))

    # here the use of fileDict is probably more clear
    # the strings used to index request.files come from the HTML name of the input field
    # see upload.html
    fileDict['GSA_Input_CSV'] = io_service.storefile(request.files['GSA_Input_CSV'])
    fileDict['GSA_Input_SHP'] = io_service.storeGSA(request.files.getlist('GSA_Input_map'))
    fileDict['GSA_file_list'] = request.files.getlist('GSA_Input_map')
    fileDict['NLP_Input_corpus'] = io_service.storeNLP(request.files.getlist('NLP_Input_corpus'))
    fileDict['NLP_Input_LDP'] = io_service.storefile(request.files['NLP_Input_LDP'])
    fileDict['NLP_Input_Sentiment'] = io_service.storefile(request.files['NLP_Input_Sentiment'])

    fileDict["NLP_INPUT_NER"] = request.form.get("NLP_INPUT_NER")
    fileDict["NLP_INPUT_IOB"] = request.form.get("NLP_INPUT_IOB")

    fileDict['SNA_Input'] = io_service.storefile(request.files['SNA_Input'])
    # fileDict['NLP_Type'] 			= request.form['NLP_Type']

    fileDict['research_question'] = request.form.get('research_question')

    # for f in fileDict:
    # 	print(str(f) + ": " + str(request.files.get(f)))

    errors = checkExtensions(case_num)  # helper method to make sure there are no input errors by the user
    # i.e. if there are errors, we can't proceed so we stay on the upload page
    if len(errors) > 0:
        return render_template('upload.html',
                               errors=errors, case_num=case_num)

    # there are intermediary steps for SNA and NLP analyses
    if fileDict['SNA_Input']:
        return redirect(url_for('sheetSelect', case_num=case_num))

    # if a user does both SNA and NLP, as it stands, the NLP intermediary data will never be gotten to. This is a problem.
    if fileDict['NLP_Input_corpus']:
        return redirect(url_for('visualize', case_num=case_num))

    # if NLP chosen, allow them to pick from the different tools available
    # do i redirect to another url to choose then save the results then redirect to visualize?
    # no, just add the radio buttons under the file upload before the hr (in the template)
    return redirect(url_for('visualize', case_num=case_num))


@upload.route('/', methods=['GET'])
def landing_page():
    case_num = 100000 + random.randint(0, 100000)
    return render_template("upload.html", case_num=case_num)
