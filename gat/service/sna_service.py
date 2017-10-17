import copy

import matplotlib
import networkx as nx

from gat.dao import dao

colors = ["DeepSkyBlue", "Gold", "ForestGreen", "Ivory", "DarkOrchid", "Coral", "DarkTurquoise", "DarkCyan", "Blue"]
hexColors = {}
for color in colors:
    rgbVal = matplotlib.colors.colorConverter.to_rgb(color)
    hexVal = matplotlib.colors.rgb2hex(rgbVal).replace("#", "0x")
    hexColors[color] = hexVal


def SNA2Dplot(graph, request, label=False):
    attr = {}
    if graph == None:
        return None
    if request.form.get("options") == None:
        i = 0
        for nodeSet in graph.nodeSet:
            attr[nodeSet] = [colors[i], 50]
            i += 1
            if i > len(colors) + 1:
                i = 0
    else:
        for nodeSet in graph.nodeSet:
            c = request.form.get(nodeSet + "Color")
            attr[nodeSet] = [c, 50]

    return graph.plot_2D(attr, label=label)


# makes more sense to make a whole SNA viz method that outputs both 2D and 3D if so desired
# 2D is probably not desired in any case though
def SNA2Dand3D(graph, request, case_num, _3D=True, _2D=False, label=False):
    fileDict = dao.getFileDict(case_num)
    systemMeasures = {}

    if graph == None:
        return None, None, None, None

    # make both
    attr = {}
    colorInput = []

    if request.form.get("options") == None:
        i = 0
        for nodeSet in graph.nodeSet:
            attr[nodeSet] = [colors[i], 50]
            colorInput.append(hexColors[colors[i]])
            i += 1
            if i == 8:
                i = 0
    else:
        for nodeSet in graph.nodeSet:
            attr[nodeSet] = [request.form.get(nodeSet + "Color"), 50]
            c = request.form.get(nodeSet + "Color")
            colorInput.append(hexColors[c])

    if request.form.get("removeNodeSubmit") != None:
        graph.removeNode(request.form.get("a"))

    # Get new node info, if available
    if request.form.get("addNodeSubmit") != None:

        node = request.form.get("nodeName")

        attrDict = {
            'block': request.form.get("nodeSet")
        }
        i = 0
        while (request.form.get("attribute" + str(i)) is not None) and (
                    request.form.get("attribute" + str(i)) != '') and (
                    request.form.get("value" + str(i)) is not None) and (
                    request.form.get("value" + str(i)) != ''):
            key = request.form.get("attribute" + str(i))
            value = request.form.get("value" + str(i))
            if request.form.get("weight" + str(i)) is not None and request.form.get("weight" + str(i)) != '':
                value = [value, {'W': request.form.get("weight" + str(i))}]
            dictForm = {key: value}
            attrDict.update(dictForm)
            i += 1

        links = []
        j = 0
        while request.form.get("link" + str(j)) != None:
            links.append(request.form.get("link" + str(j)))
            j += 1

        graph.addNode(node, attrDict, links)

    # Add system measures dictionary
    try:
        systemMeasures["Node Connectivity"] = graph.node_connectivity() # Currently only returning zero...
    except:
        "No node connectivity"
    try:
        systemMeasures["Average Clustering"] = graph.average_clustering()
    except:
        "No average clustering"
    # try:
    #     systemMeasures["Average Degree Connectivity"] = graph.average_degree_connectivity()
    # except:
    #     "No average degree connectivity"
    try:
        systemMeasures["Degree Assortativity"] = graph.degree_assortativity()
    except:
        "No degree assortativity"
    try:
        systemMeasures["Center"] = graph.center()
    except:
        "No center"
    try:
        systemMeasures["Diameter"] = graph.diameter()
    except:
        "No periphery"
    try:
        systemMeasures["Periphery"] = graph.periphery()
    except:
        "No periphery"
    # try:
    #     systemMeasures["Triadic Census"] = graph.triadic_census()
    # except:
    #     "No triadic census"

    # systemMeasures["Attribute Assortivity"] = graph.attribute_assortivity() # Which attributes...? UI?
    if graph.is_strongly_connected():
        systemMeasures["Connection Strength"] = "Strong"
    elif graph.is_weakly_connected():
        systemMeasures["Connection Strength"] = "Weak"

    # Add system measures descriptions to dictionary
    systemMeasures["Description"] = {
        'Average Clustering': 'A high clustering coefficient indicates that actors within the network are closely connected to a statistically significant degree. It is a sophisticated measure of the density of a network.',
        'Connection Strength': 'Knowing whether a graph is strongly or weakly connected is helpful because it demonstrates the robustness of the graph based on its redundancy. If a graph is strongly connected, there are two links between each actor in the network, one in each direction. A strongly connected graph thus would likely have more redundant communication/information flow and be more difficult to perturb than a weakly connected graph.',
        'Resilience': 'The baseline value for resilience is determined by identifying the cliques associated with the most central nodes in the network, perturbing those subgraphs, and measuring the mean shortest path average over several perturbations. The results are scaled on a normal curve across all cliques and a percentile resilience is determined for each clique. A high percentile resilience denotes resilience to perturbation. These values are visualized on a color spectrum from red to blue, where red is low relative resilience and blue is high relative resilience.',
        'AddNode': 'Introduces a new node to the network, complete with a user-defined name, user-defined attributes and known links. Using the DRAG link prediction model, node attributes are used to form likely connections and intelligently model the effects of external change on the network. New nodes and their predicted links are colored red for easy identification.',
        'RemoveNode': 'Removes the node inputted in the box below and any links to which it belongs.',
        'eigenvector': 'Centrality measure which sums the centralities of all adjacent nodes.',
        'betweenness': 'Centrality based on the shortest path that passes through the node.'
    }

    # Calculate resilience when requested
    if request.form.get("resilienceSubmit") != None:
        try:
            systemMeasures["Baseline"], systemMeasures["Resilience"], systemMeasures["Robustness"] = graph.calculateResilience()  # gets a scaled resilience value for each clique identified in network
            # Add colors for each resilience measure
            def addColors(systemMeasure):
                for cluster in systemMeasure:
                    systemMeasure[cluster] = int(systemMeasure[cluster])
                    percentile = systemMeasure[cluster]
                    b = int(percentile)
                    r = int(100 - percentile)
                    systemMeasure[cluster] = [percentile, r, b]
            addColors(systemMeasures["Baseline"])
            addColors(systemMeasures["Resilience"])
            addColors(systemMeasures["Robustness"])
        except nx.exception.NetworkXError:
            systemMeasures["Resilience"] = "Could not calculate resilience, NetworkX error."

    copy_of_graph = copy.deepcopy(graph)
    fileDict['copy_of_graph'] = copy_of_graph
    # return based on inputs
    ret3D = graph.create_json(graph.nodeSet, colorInput) if _3D else None
    label = True if not label and len(graph.nodes) < 20 else False
    ret2D = graph.plot_2D(attr, label) if _2D else None
    fileDict['jgdata'] = ret3D

    return ret3D, ret2D, attr, systemMeasures


def prep(graph):
    if graph != None and len(graph.G) > 0:
        if nx.algorithms.bipartite.is_bipartite(graph.G):
            graph.clustering()
        graph.closeness_centrality()
        graph.betweenness_centrality()
        graph.degree_centrality()
        # graph.katz_centrality()
        graph.eigenvector_centrality()
        graph.load_centrality()
