from flask import Blueprint, redirect, url_for

sample = Blueprint('sample', __name__)

@sample.route('/<int:case_num>/<path:sample_path>')
def sample(sample_path, case_num):
    fileDict = caseDict[case_num]
    arr = sample_path.split('/')
    if arr[0] == 'GSA':
        fileDict['GSA_Input_CSV'] = url_for('static', filename="sample/GSA/" + arr[1])[1:]
        fileDict['GSA_Input_SHP'] = url_for('static', filename="sample/GSA/" + arr[2])[1:]
        if arr[1] == "usjoin.csv":
            fileDict['GSA_data'] = ('state-id', 0.001, 0.002, array([[252., 27., 1., 0., 0.],
                                                                     [28., 226., 20., 0., 0.],
                                                                     [1., 25., 239., 15., 0.],
                                                                     [0., 0., 18., 237., 22.],
                                                                     [0., 0., 0., 24., 257.]]),
                                    matrix([[0.9, 0.09642857, 0.00357143, 0., 0.],
                                            [0.10218978, 0.82481752, 0.0729927, 0., 0.],
                                            [0.00357143, 0.08928571, 0.85357143, 0.05357143, 0.],
                                            [0., 0., 0.06498195, 0.85559567, 0.07942238],
                                            [0., 0., 0., 0.08540925, 0.91459075]]),
                                    array([[0.31780822, 0.26712329, 0.13561644, 0.23013699, 0.04931507],
                                           [0.32951514, 0.25812019, 0.13180606, 0.1625608, 0.1179978],
                                           [0.3007761, 0.26782838, 0.22843755, 0.16869234, 0.03426563],
                                           [0.29380902, 0.25603358, 0.30535152, 0.03903463, 0.10577125],
                                           [-0., 0.09811321, 0.09433962, 0.25660377, 0.5509434]]),
                                    matrix([[3.98789072, 11.01167278, 35.43877551, 100.43628118,
                                             166.20696764],
                                            [28.92208853, 4.19293283, 26.38095238, 91.37845805,
                                             157.14914451],
                                            [55.71301248, 28.32683784, 5.07303106, 64.99750567,
                                             130.76819213],
                                            [85.41208655, 58.02591192, 29.69907407, 6.15356836,
                                             65.77068646],
                                            [97.12041989, 69.73424525, 41.40740741, 11.70833333,
                                             6.61742518]]))
            fileDict['GSA_meta'] = (
            'data-state-id', 'data-state-name', "STATE_NAME", list(range(1979, 2009)), "state-name")
        else:
            # TODO: take in years instead of hard coding
            # TODO: reorganize use of gsa_meta
            observations = Weights.extractObservations(fileDict['GSA_Input_CSV'], "ALL", ["2014.0"])
            w = Weights.generateWeightsUsingShapefile(fileDict['GSA_Input_SHP'], idVariable="NAME_1")
            globalAutoCorrelation = AutoCorrelation.globalAutocorrelation(observations, w)
            localAutoCorrelation = AutoCorrelation.localAutocorrelation(observations, w)
            observations = Weights.extractObservations(fileDict['GSA_Input_CSV'], "ALL",
                                                       np.arange(2014, 2017, 0.25).tolist())
            spatialDynamics = SpatialDynamics.markov(observations, w, method="spatial")
            fileDict['GSA_data'] = ('id-1', localAutoCorrelation, globalAutoCorrelation,
                                    spatialDynamics[0], spatialDynamics[1], spatialDynamics[2], spatialDynamics[3])
            fileDict['GSA_meta'] = (
            'data-id-1', 'data-name-1', "NAME_1", np.arange(2014, 2017, 0.25).tolist(), "name-1")

            # return fileDict['GSA_file_CSV'] + " " + fileDict['GSA_file_SVG']
    if arr[0] == 'NLP':
        if arr[1] == 'iran':
            fileDict['NLP_Input_Sentiment'] = 'static/sample/NLP/sample_sentiment.txt'
            return redirect(url_for('visualize', case_num=case_num))
        else:
            fileDict['NLP_Input_corpus'] = url_for('static', filename="sample/NLP/" + arr[1] + '/')[1:]
            return redirect(url_for('visualize', case_num=case_num))
    if arr[0] == 'SNA':
        fileDict['SNA_Input'] = url_for('static', filename="sample/SNA/" + arr[1])[1:]
        return redirect(url_for('sheetSelect', case_num=case_num))

    return redirect(url_for('visualize', case_num=case_num))