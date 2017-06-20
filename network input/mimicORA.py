from flask import Flask, render_template, request, redirect, url_for, session
import SNA_bipartite as sna
import xlrd
fileDict = {}

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def fileSelect():
	if request.method == 'POST':
		if 'Input' in request.files:
			fileDict['Input'] = request.files['Input'].filename
		# if SSA chosen, allow them to pick from the different tools available
		# do i redirect to another url to choose then save the results then redirect to visualize?
		# no, just add the radio buttons under the file upload before the hr (in the template)
		return redirect(url_for('sheetSelect'))
	return render_template("input.html")

@app.route('/sheet', methods = ['GET', 'POST'])
def sheetSelect():

	inputFile = fileDict['Input']
	workbook = xlrd.open_workbook(inputFile, on_demand = True)
	fileDict['sheets'] = workbook.sheet_names()

	if request.method == 'POST':
		fileDict['sheet'] = request.form.get('sheet')
		return redirect(url_for('nodeSelect'))

	return render_template("sheetselect.html",
		sheets = fileDict['sheets'])

@app.route('/nodeinfo', methods = ['GET', 'POST'])
def nodeSelect():

	graph = sna.SNA(fileDict["Input"], fileDict['sheet'])
	fileDict['graph'] = graph

	if request.method == 'POST':
		
		nodeset = []
		colNames = []
		nodeColNames = []
		i = 0
		for header in graph.header:
			fileDict[header + "IsNode"] = True if request.form[header + "IsNode"]=="True" else False
			if fileDict[header + "IsNode"] == True:
				nodeset.append(i)
			fileDict[header + "Class"] = request.form[header + "Class"]
			fileDict[header + "Name"] = request.form[header + "Name"]
			if fileDict[header + "IsNode"] == True:
				nodeColNames.append(fileDict[header + "Name"])
			i+=1

		graph.createNodeList(nodeset,nodeColNames)
		return redirect(url_for('edgeSelect'))

	
	return render_template("nodeselect.html",
		nodes = graph.header)

@app.route('/edgeinfo', methods = ['GET', 'POST'])
def edgeSelect():

	graph = fileDict['graph']

	nodes = []
	for header in graph.header:
		if fileDict[header + "IsNode"]:
			nodes.append(fileDict[header + "Name"])

	combos = allCombos(nodes)
	fileDict['combos'] = combos

	if request.method == 'POST':
		for combo in combos:
			if request.form.get(combo[2]) == "on":
				graph.addEdges([combo[0],combo[1]])

		graph.closeness_centrality()
		graph.degree_centrality()
		graph.betweenness_centrality()

		return redirect(url_for('visualize'))


	return render_template("edgeselect.html",
		combos = combos)


@app.route('/visualize', methods = ['GET', 'POST'])
def visualize():

	graph = fileDict.get('graph')

	if request.method == 'POST':
		node = request.form["searchedNode"]

		if node not in graph.nodes:
			return render_template("visualize.html",
				picture = "",
				invalid = True,
				searchedNode = node)

		centrality = [
			graph.closeness_centrality_dict[node],
			graph.degree_centrality_dict[node],
			graph.betweenness_centrality_dict[node],
		]

		return render_template("visualize.html",
			picture = "",
			invalid = False,
			searchedNode = node,
			centrality = centrality)

	
	return render_template("visualize.html",
		picture = ""



def allCombos(nodes):
	combos = []
	for i in range(len(nodes)):
		for j in range(i+1,len(nodes)):
			combos.append((i, j, nodes[i] + " x " + nodes[j]))

	return combos






if __name__ == "__main__":
	app.debug = True
	app.run()