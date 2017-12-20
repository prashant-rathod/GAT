import warnings

import xlrd
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, json, send_file

from gat.core.sna.sna import SNA
from gat.dao import dao
from gat.service import sna_service
from gat.core.sna.propensities import IOCalc

sna_blueprint = Blueprint('sna_blueprint', __name__)


@sna_blueprint.route('/sheet', methods=['GET', 'POST'])
def sheetSelect():
    case_num = request.args.get('case_num', None)
    fileDict = dao.getFileDict(case_num)
    inputFile = fileDict['SNA_Input']
    workbook = xlrd.open_workbook(inputFile, on_demand=True)
    fileDict['sheets'] = workbook.sheet_names()

    # if workbook only has one sheet, the user shouldn't have to specify it
    if len(fileDict['sheets']) == 1:
        fileDict['nodeSheet'] = fileDict['sheets'][0]
        fileDict['attrSheet'] = None
        return redirect(url_for('sna_blueprint.nodeSelect', case_num=case_num))

    if request.method == 'POST':
        fileDict['nodeSheet'] = request.form.get('nodeSheet')
        fileDict['attrSheet'] = request.form.get('attrSheet')
        return redirect(url_for('sna_blueprint.nodeSelect', case_num=case_num))

    return render_template("sheetselect.html",
                           sheets=fileDict['sheets'], case_num=case_num)


@sna_blueprint.route('/nodeinfo', methods=['GET', 'POST'])
def nodeSelect():
    case_num = request.args.get('case_num', None)
    fileDict = dao.getFileDict(case_num)
    graph = SNA(fileDict['SNA_Input'], nodeSheet=fileDict['nodeSheet'], attrSheet=fileDict['attrSheet'])
    fileDict['graph'] = graph

    if request.method == 'POST':

        nodeColNames = []
        classAssignments = {}

        nodeColNames.append(graph.header[0])  # add source column
        for header in graph.header[1:]:  # exclude first column, automatically included as source set
            fileDict[header + "IsNode"] = True if request.form.get(header + "IsNode") == "on" else False
            classAssignments[header] = request.form[header + "Class"]
            fileDict[header + "Name"] = request.form[header + "Name"]
            if fileDict[header + "IsNode"] == True:
                nodeColNames.append(fileDict[header + "Name"])
        fileDict['nodeColNames'] = nodeColNames

        graph.createNodeList(nodeColNames)
        if fileDict['attrSheet'] != None:
            graph.loadAttributes()
        graph.createEdgeList(nodeColNames[0])
        graph.loadOntology(source=nodeColNames[0], classAssignments=classAssignments)
        if fileDict['attrSheet'] != None:
            graph.calculatePropensities(emo=True)

        # Only the first column is a source
        graph.closeness_centrality()
        graph.degree_centrality()
        graph.betweenness_centrality()
        return redirect(url_for('visualize_blueprint.visualize', case_num=case_num))

    return render_template("nodeselect.html",
                           nodes=graph.header, case_num=case_num)


@sna_blueprint.route('/snaviz', methods=['GET', 'POST'])
def jgvis():
    case_num = request.args.get('case_num', None)
    fileDict = dao.getFileDict(case_num)
    graph = fileDict.get('copy_of_graph')
    jgdata, SNAbpPlot, attr, systemMeasures = sna_service.SNA2Dand3D(graph, request, case_num, _2D=False)
    return render_template("Jgraph.html",
                           jgdata=jgdata,
                           SNAbpPlot=SNAbpPlot,
                           attr=attr,
                           graph=graph,
                           colors=sna_service.colors,
                           case_num=case_num,
                           systemMeasures=systemMeasures
                           )


@sna_blueprint.route("/_get_node_data")
def get_node_data():
    case_num = request.args.get('case_num', None)
    fileDict = dao.getFileDict(case_num)
    graph = fileDict.get('copy_of_graph')
    name = request.args.get('name', '', type=str)
    if graph == None or len(graph.G) == 0:
        return jsonify(name=name,
                       eigenvector=None,
                       betweenness=None,
                       sentiment=None
                       )
    graph.closeness_centrality()
    graph.betweenness_centrality()
    graph.degree_centrality()
    # graph.katz_centrality()
    graph.eigenvector_centrality()
    graph.load_centrality()
    if graph.eigenvector_centrality_dict != {} and graph.eigenvector_centrality_dict != None and graph.eigenvector_centrality_dict.get(
            name) != None:
        eigenvector = str(round(graph.eigenvector_centrality_dict.get(name), 4));
    else:
        eigenvector = "clustering not available"
    if graph.betweenness_centrality_dict != {} and graph.betweenness_centrality_dict != None and graph.betweenness_centrality_dict.get(
            name) != None:
        betweenness = str(round(graph.betweenness_centrality_dict.get(name), 4));
    else:
        betweenness = "clustering not available"
    if graph.sentiment_dict != {} and graph.sentiment_dict != None and graph.sentiment_dict.get(name) != None:
        sentiment = str(round(graph.sentiment_dict.get(name), 4));
    else:
        sentiment = "Sentiment not available for this node."
    attributes = graph.get_node_attributes(name)
    toJsonify = dict(name=name,
                     eigenvector=eigenvector,
                     betweenness=betweenness,
                     sentiment=sentiment,
                     attributes=attributes)
    return jsonify(toJsonify)


@sna_blueprint.route("/_get_edge_data")
def get_edge_data():
    case_num = request.args.get('case_num', None)
    fileDict = dao.getFileDict(case_num)
    graph = fileDict.get('copy_of_graph')
    name = request.args.get('name', '', type=str)
    if graph == None or len(graph.G) == 0:
        return jsonify(name=name)
    pair = name.split(",")
    link = graph.G[pair[0]][pair[1]]
    toJsonify = dict(name=name, source=pair[0], target=pair[1])
    for attr in link:
        toJsonify[attr] = link[attr]
    return jsonify(toJsonify)


@sna_blueprint.route("/_subgraph_viz")
def subgraph_viz():
    case_num = request.args.get('case_num', None)
    fileDict = dao.getFileDict(case_num)
    centralNode = request.args.get('centralNode', '', type=str)
    toJson = {}
    for item in fileDict['Cliques']:
        if item[0] == centralNode:
            toJson = item[1]
            return jsonify(toJson)
    return jsonify(toJson)


@sna_blueprint.route("/_sentiment_change")
def view_sent_change():
    case_num = request.args.get('case_num', None)
    fileDict = dao.getFileDict(case_num)
    response = fileDict["SentimentChange"]
    return render_template("sentiment_change.html",
                           sent_json=json.dumps(response, sort_keys=True, indent=4, separators=(',', ':'))
                           )

