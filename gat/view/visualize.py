from flask import Blueprint, render_template

visualize = Blueprint('visualize', __name__)


@visualize.route('/visualize/<int:case_num>', methods = ['GET', 'POST'])
def visualize(case_num):
    fileDict = caseDict[case_num]
    GSA_file_CSV 		= fileDict.get('GSA_Input_CSV')
    GSA_file_SHP 		= fileDict.get('GSA_Input_SHP')
    GSA_file_SVG 		= fileDict.get('GSA_Input_SVG')
    NLP_dir 			= fileDict.get('NLP_Input_corpus')
    NLP_file_LDP		= fileDict.get('NLP_Input_LDP')
    NLP_urls                    = fileDict.get('NLP_LDP_terms')
    NLP_file_sentiment 	= fileDict.get('NLP_Input_Sentiment')
    NLP_NER_sentence 	= fileDict.get('NLP_INPUT_NER')
    NLP_IOB_sentence 	= fileDict.get('NLP_INPUT_IOB')
    SNA_file 			= fileDict.get('SNA_Input')
    #NLP_type 			= fileDict.get('NLP_Type')
    research_question 	= fileDict.get('research_question')
    tropes 				= fileDict.get('tropes')
    #research_question = None # temporary: Smart Search is under development
    graph 				= fileDict.get('graph')
    GSA_sample			= fileDict.get('GSA_data')
    error = False

    auto = None
    sp_dyn = None
    svgNaming = None
    if GSA_sample != None:
        svgNaming = GSA_sample[0]
        auto = GSA_sample[1:3]
        sp_dyn = [mat for mat in GSA_sample[3:]]
        calc_ac(case_num)


    if graph != None and len(graph.G)>0:

        if nx.algorithms.bipartite.is_bipartite(graph.G):
            graph.clustering()
        graph.closeness_centrality()
        graph.betweenness_centrality()
        graph.degree_centrality()
        #graph.katz_centrality()
        graph.eigenvector_centrality()
        graph.load_centrality()

    jgdata, SNAbpPlot, attr, systemMeasures = SNA2Dand3D(graph, request, case_num, _2D = True)
    fileDict['SNAbpPlot'] = '/' + SNAbpPlot if SNAbpPlot != None else None
    gsaCSV = None
    mymap = None
    nameMapping = None

    if (GSA_file_CSV is not None and GSA_file_SHP is not None and fileDict.get('GSA_meta') is not None):
        gsaCSV, mymap, nameMapping = tempParseGSA(GSA_file_CSV, GSA_file_SHP, fileDict['GSA_meta'][0], fileDict['GSA_meta'][1])
    if GSA_file_SVG != None:
        gsaCSV, mymap = parseGSA(GSA_file_CSV, GSA_file_SVG)

    if gsaCSV == None and mymap == True:
        error = True
        mymap = None

    copy_of_graph = copy.deepcopy(graph)
    fileDict['copy_of_graph'] = copy_of_graph


    return render_template('visualizations.html',
        research_question = research_question,
        SNAbpPlot = SNAbpPlot,
        graph = copy_of_graph,
        attr = attr,
        colors = colors,
        #nltkPlot = nltkPlot,
        gsaCSV = gsaCSV,
        mymap = mymap,
        svgNaming = svgNaming,
        nameMapping = nameMapping,
        jgdata = jgdata,
        tropes = tropes,
        GSA_sample = GSA_sample,
        auto = auto,
        sp_dyn = sp_dyn,
        error=error,
        case_num = case_num,
        nlp_sentiment = nlp_sentiment,
        nlp_ner = ner,
        nlp_iob = iob,
        nlp_data_show = nlp_data_show,
        nlp_summary = nlp_summary,
        nlp_entities = nlp_entities,
        #nlp_network = nlp_network,
        nlp_sources =  nlp_sources,
        nlp_tropes = nlp_tropes
        )