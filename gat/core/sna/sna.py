import tempfile
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from networkx.algorithms import bipartite as bi
from networkx.algorithms import centrality
from itertools import product
from collections import defaultdict, namedtuple
from flask import jsonify
import pandas as pd
import datetime

from gat.core.sna import propensities
from gat.core.sna import resilience
from gat.core.sna import cliques
from gat.core.sna import ergm
from gat.core.sna import excel_parser


class SNA():
    def __init__(self, excel_file, nodeSheet, attrSheet=None):
        self.subAttrs = ["W", "SENT", "SZE", "AMT"]
        self.header, self.list = excel_parser.readFile(self.subAttrs, excel_file, nodeSheet)
        self.header = [head[0] for head in self.header]
        if attrSheet != None:
            self.attrHeader, self.attrList = excel_parser.readFile(self.subAttrs, excel_file, attrSheet)
        self.G = nx.DiGraph()
        self.nodes = []
        self.edges = []
        self.nodeSet = []
        self.clustering_dict = {}
        self.latapy_clustering_dict = {}
        self.closeness_centrality_dict = {}
        self.betweenness_centrality_dict = {}
        self.degree_centrality_dict = {}
        self.eigenvector_centrality_dict = {}
        self.katz_centraltiy_dict = {}
        self.load_centrality_dict = {}
        self.communicability_centrality_dict = {}
        self.communicability_centrality_exp_dict = {}
        self.node_attributes_dict = {}
        self.sentiment_dict = {}
        self.classList = ['Agent','Organization','Audience','Role','Event','Belief','Symbol','Knowledge','Task','Actor']
        self.attrSheet = attrSheet
        self.sent_outputs = []

    # create set of nodes for multipartite graph
    # name = names of the node. This is defined by the header. ex: Abbasi-Davani.F: Name  or Abbasi-Davani.F: Faction leader
    # nodeSet = names that define a set of node. For example, we can define Person, Faction Leader, and Party Leader as ".['agent']"
    # note: len(name) = len(nodeSet), else code fails
    def createNodeList(self, nodeSet):
        for row in self.list:
            for node in row:
                if node['header'] in nodeSet and node['val'] != "":
                    # strip empty cells
                    self.G.add_node(node['val'], block=node['header'])
        self.nodeSet = nodeSet
        self.nodes = nx.nodes(self.G)

    def loadOntology(self, source, classAssignments):

        # Creating an edge list and setting its length for the conditional iterations:
        b = self.attrList
        y = len(b)

        # Creating master edge list, and empty lists to fill from each ontology class
        classLists = defaultdict(list)  # creates a dictionary with default list values, no need to initialize - nifty!
        edgeList = []

        # iterating through ontology classes to add them to the network as nodes connected by weighted
        # edge attributes to other ontological entities
        for x in range(0, y):
            for q in range(0, len(b[x])):
                nodeHeader = b[x][q]['header']
                nodeClass = classAssignments.get(nodeHeader)
                if nodeHeader == source and b[x][q]['val'] is not None:
                    classLists['actor'].append(b[x][q]['val'])
                if nodeClass == 'Belief' and b[x][q]['val'] is not None:
                    classLists['belief'].append(b[x][q]['val'])
                if nodeClass == 'Symbols' and b[x][q]['val'] is not None:
                    classLists['symbol'].append(b[x][q]['val'])
                if nodeClass == 'Resource' and b[x][q]['val'] is not None:
                    classLists['resource'].append(b[x][q]['val'])
                if nodeClass == 'Agent' and b[x][q]['val'] is not None:
                    classLists['agent'].append(b[x][q]['val'])
                if nodeClass == 'Organization' and b[x][q]['val'] is not None:
                    classLists['org'].append(b[x][q]['val'])
                if nodeClass == 'Event' and b[x][q]['val'] is not None:
                    classLists['event'].append(b[x][q]['val'])
                if nodeClass == 'Audience' and b[x][q]['val'] is not None:
                    classLists['aud'].append(b[x][q]['val'])

        # removing duplicates from each list
        # (this does not remove the effect that numerous connections to one node have on the network)
        classLists = {key: set(val) for key, val in classLists.items()}  # dict comprehension method

        # adding ontological class to each node as node attribute
        stringDict = {
            'actor': 'Actor',
            'belief': 'Belief',
            'symbol': 'Symbol',
            'resource': 'Resource',
            'agent': 'Agent',
            'org': 'Organization',
            'aud': 'Audience',
            'event': 'Event',
            'role': 'Role',
            'know': 'Knowledge',
            'taskModel': 'Task Model',
            'location': 'Location',
            'title': 'Title',
            'position': 'position',
        }
        for x in nx.nodes(self.G):
            for key, entityList in classLists.items():
                if x in entityList:
                    self.G.node[x]['ontClass'] = stringDict[key]

    # Input: header list and list of attributes with header label from attribute sheet
    # Output: updated list of nodes with attributes
    def loadAttributes(self):
        for row in self.attrList:
            nodeID = row[0]['val']
            for cell in row[1:]:
                if cell['val'] != '':
                    if nodeID in self.nodes:
                        attrList = []
                        node = self.G.node[nodeID]
                        if cell['header'] in self.subAttrs:  # handle subattributes, e.g. weight
                            key = {}
                            while prevCell['header'] in self.subAttrs:
                                key[prevCell['header']] = prevCell['val']
                                prevCell = row[row.index(prevCell) - 1]
                            key[cell['header']] = cell['val']
                            for value in node[prevCell['header']]:
                                if prevCell['val'] in value:
                                    listFlag = True if type(value) is list else False
                                    attrList.append([value[0], key] if listFlag else [value, key]) # weighted attributes take the form [value, weight]
                                else:
                                    attrList.append(value)
                            attrID = prevCell['header']

                        else:  # if the attribute is not a subattribute
                            if cell['header'] in self.G.node[nodeID]:
                                attrList = (node[cell['header']])
                            attrList.append(cell['val'])
                            attrID = cell['header']
                        self.changeAttribute(nodeID, attrList, attrID)

                prevCell = cell # save cell in case of subattribute data

    # Input: the node set that will serve as the source of all links
    # Output: updated list of edges connecting nodes in the same row
    def createEdgeList(self, sourceSet):
        list = self.list
        edgeList = []
        for row in list:
            sourceNodes = []
            for node in row:
                if node['header'] in sourceSet:
                    sourceNodes.append(node['val'])
            for source in sourceNodes:
                for node in row:
                    if node['val'] != source and node['header'] in self.nodeSet:
                        sourceDict = self.G.node[source]
                        edge = (source, node['val'])
                        edgeList.append(edge)
                        # for ontological elements: add a weighted link if attribute appears in graph
                        for attrs in [val for key,val in sourceDict.items()]:
                            for attr in attrs:
                                if attr[0] == node['val']:
                                    avg_w = np.average([float(val) for key, val in attr[1].items()])
                                    self.G.add_edge(source, attr[0], weight=avg_w)

        self.G.add_edges_from(edgeList)
        self.edges = edgeList

    def addEdges(self, pair):  # deprecated, needs fixing - doesn't handle new dict structure
        data = self.list
        newEdgeList = []
        for row in data:
            first = row[pair[0]]['val']
            second = row[pair[1]]['val']
            if (first != '' and second != '') and (first != second):
                newEdgeList.append((first, second))
        self.G.add_edges_from(newEdgeList)
        self.edges.extend(newEdgeList)

    def calculatePropensities(self, propToggle={'emo':True,'infl':True,'role':True}):
        self.propToggle = propToggle

        for edge in self.edges:  # for every edge, calculate propensities and append as an attribute
            attributeDict = {"propsFlag": True}

            IO, emoPropList, rolePropList, inflPropList = propensities.propCalc(self, edge, propToggle)
            attributeDict['IO'] = IO

            if propToggle['emo'] and len(emoPropList) > 0:
                attributeDict['Emotion'] = emoPropList

            if propToggle['role'] and len(rolePropList) > 0:
                attributeDict['Role'] = rolePropList

            if propToggle['infl'] and len(inflPropList) > 0:
                attributeDict['Influence'] = inflPropList

            self.G[edge[0]][edge[1]].update(attributeDict)

        self.edges = nx.edges(self.G)

    def drag_predict(self,node):
        ## Smart prediction prototype - combines propensities and data-based statistical model

        # ERGM generates probability matrix where order is G.nodes() x G.nodes()
        ergm_prob_mat = ergm.probability(G=self.G)

        # Assigning propensities probabilities and generating add_node links
        for target in self.G.nodes_iter():
            IO, emoProps, roleProps, inflProps = propensities.propCalc(self, (node, target))
            if len(emoProps) > 0:
                w = []
                for prop in emoProps:
                    w.append(prop[4] * prop[5])  # add the product of the attribute weights to a list for each prop
                w_avg = np.average(w)  # find average propensity product weight
                prob = np.random.binomial(1, w_avg * 1 / 2 if w_avg * 1/2 > 0 else 0)
                # use w_avg as the probability for a bernoulli distribution
                if prob:
                    self.G.add_edge(node, target)
                    self.G[node][target]['Emotion'] = emoProps
                    self.G[node][target]['Role'] = roleProps if len(roleProps) > 0 else None
                    self.G[node][target]['Influence'] = inflProps if len(inflProps) > 0 else None
                    self.G[node][target]['Predicted'] = True
        # iterate through all possible edges
        for i, j in product(range(len(self.G.nodes())), repeat=2):
            if i != j:
                node = self.G.nodes()[i]
                target = self.G.nodes()[j]
                prob = ergm_prob_mat[i, j] * 0.05

                # check props
                if self.G[node].get(target) is not None:
                    ## check emo props to modify adjacency prob matrix if present
                    if self.G[node][target].get('Emotion') is not None:
                        w = []
                        for prop in emoProps:
                            w.append(prop[4] * prop[5])  # add the product of the attribute weights to a list for each prop
                        w_avg = np.average(w)
                        prob = (prob + w_avg * 0.5) / 2

                presence = np.random.binomial(1, prob) if prob < 1 else 1
                # use adjacency prob mat as the probability for a bernoulli distribution
                if presence:
                    self.G.add_edge(node, target)
                    self.G[node][target]['Predicted'] = True
        self.feedbackUpdate()

    def feedbackUpdate(self):
        currentSents = self.sentiment(types=self.classList,key="W",operation='average')
        for type in self.classList:
            # nodes = [node for node in self.G.nodes_iter() if node.get("ontClass") == type]
            # for typeNode in nodes:
            for node in self.G.nodes_iter():
                sent = self.G.node[node].get(type)
                if sent is not None:
                    for i in range(len(sent)):
                        if len(sent[i]) == 2 and currentSents.get(sent[i][0]) is not None:
                            item = sent[i]
                            # update this sentiment weight
                            globalSent = currentSents.get(item[0])
                            # some function to decide the weighting, dependent on node sent
                            globalWeight = (float(item[1]['W'])**2 * globalWeight**2) / 2 # another 3D parabola - the greater the difference, the higher the weight
                            # set new sentiment
                            self.G.node[node][type][i][1]['W'] = str((1-globalWeight)*float(item[1]['W']) + globalWeight*globalSent)
        self.calculatePropensities(self.propToggle)


    # input: spreadsheet of bomb attacks
    # output: updated dict of sentiment changes for each of attack events
    def event_update(self, event_sheet, max_iter):
        df = pd.read_excel(event_sheet)
        bombData = df.to_dict(orient='index')
        for x in range(0, len(bombData)):
            bombData[x]['Date'] = datetime.datetime.strptime(str(bombData[x]['Date']), '%Y%m%d')
        # using datetime to create iterations of flexible length
        dateList = [bombData[x]['Date'] for x in bombData]
        dateIter = (max(dateList) - min(dateList)) / 10
        SentChange = namedtuple('SentChange', ['source','target','change'])

        ret = []

        def checkScale(num):
            num = round(num, 5)
            if num > 1:
                num = 1
            if num < 0:
                num = 0
            return num


        for i in range(max_iter):
            output_rows = []
            nodeList = [(bombData[x]['Actor'], bombData[x]['Target'], bombData[x]['CODE']) for x in bombData if
                         min(dateList) + dateIter * i <= bombData[x]['Date'] < min(dateList) + dateIter * (i + 1)]
            # adding attacks to test graph by datetime period and iterating through to change sentiments
            iterEdgeList = []
            for node in nodeList:
                for others in self.G.nodes_iter():
                    # rejection of source
                    # if self.G.has_edge(node[0], others) or self.G.has_edge(node[1], others):
                    for ontClass in self.classList:
                        sent = self.G.node[others].get(ontClass)  # the attribute, if it exists
                        if sent is not None:
                            for item in [item for item in sent if len(item) == 2]:
                                original_output = float(item[1]['W'])
                                if item[1].get('W') is not None:
                                    if item[0] == node[0]:
                                        original = float(item[1]['W'])

                                        item[1]['W'] = original * 0.99

                                        output_rows.append(
                                            SentChange(node[0], others, checkScale(item[1]['W'] - original)))
                                        # output_dict[node[0] + " towards " + others] = item[1]['W'] - original
                                    if item[0] == node[1]:
                                        original = float(item[1]['W'])

                                        item[1]['W'] = original * 1.05
                                        output_rows.append(
                                            SentChange(node[0], others, checkScale(item[1]['W'] - original)))
                                        # output_dict[node[1] + " towards " + others] = item[1]['W'] - original

                                    # response of city populations - HARDCODED
                                    if item[0] == "Shi'ism" and float(item[1]['W']) > -0.5:
                                        if node[1] == 'Najaf':
                                            original = float(item[1]['W'])
                                            item[1]['W'] = original * 1.05
                                            output_rows.append(
                                                SentChange(node[0], others, checkScale(item[1]['W'] - original)))
                                            # output_dict[node[1] + " towards " + others] = item[1]['W'] - original
                                        if node[1] == 'Basra':
                                            original = float(item[1]['W'])
                                            item[1]['W'] = original * 1.05
                                            output_rows.append(
                                                SentChange(node[0], others, checkScale(item[1]['W'] - original)))
                                            # output_dict[node[1] + " towards " + others] = item[1]['W'] - original
                                    if item[0] == "Kurdish Nationalism" and float(item[1]['W']) > -0.5:
                                        if node[1] == 'Kirkuk':
                                            original = float(item[1]['W'])
                                            item[1]['W'] = original * 1.05
                                            output_rows.append(
                                                SentChange(node[0], others, checkScale(item[1]['W'] - original)))
                                    if item[0] == "Sunni'ism" and float(item[1]['W']) > -0.5:
                                        if node[1] == 'Fallujah':
                                            original = float(item[1]['W'])
                                            item[1]['W'] = original * 1.05
                                            output_rows.append(SentChange(node[0], others, checkScale(item[1]['W'] - original)))
                                            # output_dict[node[1] + " towards " + others] = item[1]['W'] - original
                                    if others == 'ISIL_al-Baghdadi':
                                        original = float(item[1]['W'])
                                        item[1]['W'] = original * 0.99
                                        output_rows.append(
                                            SentChange(node[0], others, checkScale(item[1]['W'] - original)))
                                        # output_dict[node[1] + " towards " + others] = item[1]['W'] - original
                # add an event node
                event = 'Event ' + str(node[2]) + ': ' + node[0] + ' to ' + node[1]
                self.G.add_node(event, {'ontClass': 'Event', 'Name': [
                    'Event' + str(i) + ' ' + str(node[2]) + ': ' + node[0] + ' to ' + node[1]], 'block': 'Event',
                                        'Description': 'Conduct suicide, car, or other non-military bombing', 'code': node[2]})
                self.G.add_edge(node[0], event)
                self.G.add_edge(event, node[1])
            self.G.add_weighted_edges_from(iterEdgeList, 'W')
            ret.append(list(output_rows))

        self.nodes = nx.nodes(self.G)  # update node list
        self.edges = nx.edges(self.G)  # update edge list
        self.sent_outputs = ret
        self.feedbackUpdate()

        return ret

    def meaning_value_chains(self):
    # this function takes an attribute list and constructs meaning value chains by iterating through attribute...
    # combinations for each node and returning a list of the average weight for each value chain. The final result...
    # is a list of every possible value chain for each actor and the average weight of each value chain. 'Heavier'...
    # VCs can be seen as having higher centers of gravity.

        b = self.attrList
        y = len(b)
        tit_list = []
        pos_list = []
        org_list = []
        age_list = []
        rol_list = []
        bel_list = []

        # iterating through attribute sheet to create lists of the ID, attribute and weight for every actor for...
        # each possible attribute.
        for n in range(0, y):
            for attr in range(0, (len(b[n]))):
                if b[n][attr]['header'] == 'Title':
                    tit_list.append(
                        (b[n][0]['val'], b[n][attr]['val'], b[n][attr]['header'], b[n][attr + 1]['val']))
                if b[n][attr]['header'] == 'Position':
                    pos_list.append(
                        (b[n][0]['val'], b[n][attr]['val'], b[n][attr]['header'], b[n][attr + 1]['val']))
                if b[n][attr]['header'] == 'Org':
                    org_list.append(
                        (b[n][0]['val'], b[n][attr]['val'], b[n][attr]['header'], b[n][attr + 1]['val']))
                if b[n][attr]['header'] == 'Agent':
                    age_list.append(
                        (b[n][0]['val'], b[n][attr]['val'], b[n][attr]['header'], b[n][attr + 1]['val']))
                if b[n][attr]['header'] == 'Role':
                    rol_list.append(
                        (b[n][0]['val'], b[n][attr]['val'], b[n][attr]['header'], b[n][attr + 1]['val']))
                if b[n][attr]['header'] == 'Belief':
                    bel_list.append(
                        (b[n][0]['val'], b[n][attr]['val'], b[n][attr]['header'], b[n][attr + 1]['val']))

        # combining the above attribute lists into a single node list that follows the form of the VC's we're making
        nod_list = []
        for x in range(0, len(pos_list)):
            for y in range(0, len(org_list)):
                if pos_list[x][0] == org_list[y][0]:
                    nod_list.append((pos_list[x][0], pos_list[x][1], org_list[y][1], org_list[y][3]))

        for x in range(0, len(org_list)):
            for y in range(0, len(age_list)):
                if org_list[x][0] == age_list[y][0]:
                    nod_list.append((org_list[x][0], org_list[x][1], age_list[y][1], age_list[y][3]))

        for x in range(0, len(age_list)):
            for y in range(0, len(rol_list)):
                if age_list[x][0] == rol_list[y][0]:
                    nod_list.append((age_list[x][0], age_list[x][1], rol_list[y][1], rol_list[y][3]))

        for x in range(0, len(rol_list)):
            for y in range(0, len(bel_list)):
                if rol_list[x][0] == bel_list[y][0]:
                    nod_list.append((rol_list[x][0], rol_list[x][1], bel_list[y][1], bel_list[y][3]))

        # creating a list of every possible value chain for each actor
        av_weight_list = []
        vc_list = []
        [vc_list.append((tm_1[0], tm_1[1], tm_1[2], tm_1[3],
                         tm_2[0], tm_2[1], tm_2[2], tm_2[3],
                         tm_3[0], tm_3[1], tm_3[2], tm_3[3],))
            for tm_1 in nod_list
            for tm_2 in nod_list
            for tm_3 in nod_list if tm_1[0] == tm_2[0] and tm_2[0] == tm_3[0]]

        # creating a graph for each value chain and returning the edges as weights to be used to calculate the...
        # average weight for each task model. I spent a lot of time trying to find a measure that we could..
        # effectively use incorporating a more robust method, but ASPL can run into significant problems with...
        # negative edge weights in hierarchical graphs. nx.bellman_ford() works with negative edge weights, but...
        # it's really slow for the amount of iterations necessary here.
        for vc in vc_list:
            self.vc_graph = nx.Graph()
            vc_edge_list = ([vc[0], vc[2], float(vc[3])],
                            [vc[2], vc[6], float(vc[7])],
                            [vc[6], vc[10], float(vc[11])])
            self.vc_graph.add_weighted_edges_from(vc_edge_list, 'W')
            weights = nx.get_edge_attributes(self.vc_graph, 'W')
            weights_list = list(weights.values())
            weights_mean = np.mean(weights_list)
            av_weight_list.append((vc_edge_list, weights_mean))

        return av_weight_list

    # copy the original social network graph created with user input data.
    # this will be later used to reset the modified graph to inital state
    def copyGraph(self):
        self.temp = self.G

    def resetGraph(self):
        self.G = self.temp

    # remove edge and node. Note that when we remove a certain node, edges that are
    # connected to such nodes are also deleted.
    def removeNode(self, node):
        if self.G.has_node(node):
            self.G.remove_node(node)
            self.nodes = nx.nodes(self.G)
        for edge in self.edges:
            if node in edge:
                self.edges.remove(edge)

    def addNode(self, node, attrDict={}, connections=[]):
        self.G.add_node(node, attrDict)
        for i in connections:
            self.G.add_edge(node, i)
        for k in attrDict:  # add attributes based on user input
            self.changeAttribute(node, [attrDict[k]], k)
        self.changeAttribute(node, True, 'newNode')

        self.drag_predict(node)

        self.nodes = nx.nodes(self.G)  # update node list
        self.edges = nx.edges(self.G)  # update edge list

    def removeEdge(self, node1, node2):
        if self.G.has_edge(node1, node2):
            self.G.remove_edge(node1, node2)

    # Change an attribute of a node
    def changeAttribute(self, node, value, attribute="bipartite"):
        if self.G.has_node(node):
            self.G.node[node][attribute] = value
        self.nodes = nx.nodes(self.G)

    # Change node name
    def relabelNode(self, oldNode, newNode):
        if self.G.has_node(oldNode):
            self.G.add_node(newNode, self.G.node[oldNode])
            self.G.remove_node(oldNode)
        self.nodes = nx.nodes(self.G)

    # Check if node exists
    def is_node(self, node):
        return self.G.has_node(node)

    # Getter for nodes and edges
    def getNodes(self):
        return self.nodes

    def getEdges(self):
        return self.edges

    def communityDetection(self):
        undirected = self.G.to_undirected()
        self.eigenvector_centrality()
        return cliques.louvain(G = undirected, centralities = self.eigenvector_centrality_dict)

    def calculateResilience(self,baseline=True,robustness=True):
        cliques_found = self.communityDetection()
        baseline, simple, trace = resilience.resilience(cliques_found, ergm_iters=1500)
        robustness = resilience.laplacianRes(cliques_found, iters=5) if robustness else None
        return baseline,simple,robustness, trace

    ##########################
    ## System-wide measures ##
    ##########################

    # set all the properties with this function.
    def set_property(self):
        self.clustering()
        self.latapy_clustering()
        self.robins_alexander_clustering()
        self.closeness_centrality()
        self.betweenness_centrality()
        self.degree_centrality()
        self.katz_centrality()
        self.eigenvector_centrality()
        self.load_centrality()
        self.communicability_centrality()  # Not available for directed graphs
        self.communicability_centrality_exp()
        self.node_connectivity()
        self.average_clustering()

    def center(self):
        return nx.center(self.G)
    def diameter(self):
        return nx.diameter(self.G)
    def periphery(self):
        return nx.periphery(self.G)
    def eigenvector(self):
        return nx.eigenvector_centrality(self.G)
    def triadic_census(self):
        return nx.triadic_census(self.G)
    def average_degree_connectivity(self):
        return nx.average_degree_connectivity(self.G)
    def degree_assortativity_coefficient(self):
        return nx.degree_assortativity_coefficient(self.G)

    # node connectivity:
    def node_connectivity(self):
        return nx.node_connectivity(self.G)

    # average clustering coefficient:
    def average_clustering(self):
        return nx.average_clustering(self.G.to_undirected())

    # attribute assortivity coefficient:
    def attribute_assortivity(self, attr):
        return nx.attribute_assortativity_coefficient(self.G, attr)

    # is strongly connected:
    def is_strongly_connected(self):
        return nx.is_strongly_connected(self.G)

    # is weakly connected:
    def is_weakly_connected(self):
        return nx.is_weakly_connected(self.G)

    #############################
    ## Node-dependent measures ##
    #############################

    # Sum sentiment for belief nodes
    def sentiment(self,types,key,operation='sum'):
        sentiment_dict = {}
        if operation == 'average':
            counts = {}
        for type in types:
            # nodes = [node for node in self.G.nodes_iter() if node.get("ontClass") == type]
            # for typeNode in nodes:
            for node in self.G.nodes_iter():
                sent = self.G.node[node].get(type)
                if sent is not None:
                    items = [item for item in sent if len(item) == 2]
                    for item in items:
                        if sentiment_dict.get(item[0]) is None:
                            sentiment_dict[item[0]] = float(item[1][key])
                            if operation == 'average':
                                counts[item[0]] = 1
                        else:
                            sentiment_dict[item[0]] += float(item[1][key])
                            if operation == 'average':
                                counts[item[0]] += 1
                        sentiment_dict[item[0]] = round(sentiment_dict[item[0]],2)
        if operation == 'average':
            for key in sentiment_dict:
                sentiment_dict[key] /= counts[key]
        if operation == 'sum':
            self.sentiment_dict = sentiment_dict
        return sentiment_dict


    # Find clustering coefficient for each nodes
    def clustering(self):
        self.clustering_dict = bi.clustering(self.G)

    # set lapaty clustering to empty dictionary if there are more then 2 nodesets
    # else return lapaty clustering coefficients for each nodes
    def latapy_clustering(self):
        if len(self.nodeSet) != 2 or len(set(self.nodeSet)) != 2:
            self.latapy_clustering_dict = {}
        else:
            self.latapy_clustering_dict = bi.latapy_clustering(self.G)

    def robins_alexander_clustering(self):
        self.robins_alexander_clustering_dict = bi.robins_alexander_clustering(self.G)

    # Find closeness_centrality coefficient for each nodes
    def closeness_centrality(self):
        self.closeness_centrality_dict = bi.closeness_centrality(self.G, self.nodes)

    # Find degree_centrality coefficient for each nodes
    def degree_centrality(self):
        self.degree_centrality_dict = nx.degree_centrality(self.G)

    # Find betweenness_centrality coefficient for each nodes
    def betweenness_centrality(self):
        self.betweenness_centrality_dict = nx.betweenness_centrality(self.G)

    def eigenvector_centrality(self):
        self.eigenvector_centrality_dict = nx.eigenvector_centrality(self.G, max_iter=500, tol=1e-01)
        # self.eigenvector_centrality_dict = nx.eigenvector_centrality(self.G)
        # self.eigenvector_centrality_dict = nx.eigenvector_centrality_numpy(self.G)

    def katz_centrality(self):
        self.katz_centrality_dict = centrality.katz_centrality(self.G)

    def load_centrality(self):
        self.load_centrality_dict = nx.load_centrality(self.G)

    def communicability_centrality(self):
        self.communicability_centrality_dict = nx.communicability_centrality(self.G)

    def communicability_centrality_exp(self):
        self.communicability_centrality_exp_dict = nx.communicability_centrality(self.G)

    def node_attributes(self):
        self.node_attributes_dict = self.G.node

    def get_node_attributes(self, node):
        return self.G.node[node]

    def get_eigenvector_centrality(self, lst=[]):
        if len(lst) == 0:
            return self.eigenvector_centrality_dict
        else:
            sub_dict = {}
            for key, value in self.clustering_dict:
                if key in lst:
                    sub_dict[key] = value
            return sub_dict

    def get_clustering(self, lst=[]):
        if len(lst) == 0:
            return self.clustering_dict
        else:
            sub_dict = {}
            for key, value in self.clustering_dict:
                if key in lst:
                    sub_dict[key] = value
            return sub_dict

    def get_latapy_clustering(self, lst=[]):
        if len(lst) == 0:
            return self.latapy_clustering_dict
        else:
            sub_dict = {}
            for key, value in self.latapy_clustering_dict:
                if key in lst:
                    sub_dict[key] = value
            return sub_dict

    def get_robins_alexander_clustering(self, lst=[]):
        if len(lst) == 0:
            return self.robins_alexander_clustering_dict
        else:
            sub_dict = {}
            for key, value in self.robins_alexander_clustering_dict:
                if key in lst:
                    sub_dict[key] = value
            return sub_dict

    def get_closeness_centrality(self, lst=[]):
        if len(lst) == 0:
            return self.closeness_centrality_dict
        else:
            sub_dict = {}
            for key, value in self.closeness_centrality_dict:
                if key in lst:
                    sub_dict[key] = value
            return sub_dict

    def get_degree_centrality(self, lst=[]):
        if len(lst) == 0:
            return self.degree_centrality_dict
        else:
            sub_dict = {}
            for key, value in self.degree_centrality_dict:
                if key in lst:
                    sub_dict[key] = value
            return sub_dict

    def get_betweenness_centrality(self, lst=[]):
        if len(lst) == 0:
            return self.betweenness_centrality_dict
        else:
            sub_dict = {}
            for key, value in self.betweenness_centrality_dict:
                if key in lst:
                    sub_dict[key] = value
            return sub_dict

    def get_katz_centrality(self, lst=[]):
        if len(lst) == 0:
            return self.katz_centrality_dict
        else:
            sub_dict = {}
            for key, value in self.katz_centrality_dict:
                if key in lst:
                    sub_dict[key] = value
            return sub_dict

    def get_load_centrality(self, lst=[]):
        if len(lst) == 0:
            return self.load_centrality_dict
        else:
            sub_dict = {}
            for key, value in self.load_centrality_dict:
                if key in lst:
                    sub_dict[key] = value
            return sub_dict

    def get_communicability_centrality(self, lst=[]):
        if len(lst) == 0:
            return self.load_centrality_dict
        else:
            sub_dict = {}
            for key, value in self.load_centrality_dict:
                if key in lst:
                    sub_dict[key] = value
            return sub_dict

    def get_communicability_centrality_exp(self, lst=[]):
        if len(lst) == 0:
            return self.communicability_centrality_dict
        else:
            sub_dict = {}
            for key, value in self.communicability_centrality_dict:
                if key in lst:
                    sub_dict[key] = value
            return sub_dict

    # draw 2D graph
    # attr is a dictionary that has color and size as its value.
    def graph_2D(self, attr, label=False):
        block = nx.get_node_attributes(self.G, 'block')
        Nodes = nx.nodes(self.G)
        pos = nx.fruchterman_reingold_layout(self.G)
        labels = {}
        for node in block:
            labels[node] = node
        for node in set(self.nodeSet):
            nx.draw_networkx_nodes(self.G, pos,
                                   with_labels=False,
                                   nodelist=[n for n in Nodes if bipartite[n] == node],
                                   node_color=attr[node][0],
                                   node_size=attr[node][1],
                                   alpha=0.8)
        nx.draw_networkx_edges(self.G, pos, width=1.0, alpha=0.5)
        for key, value in pos.items():
            pos[key][1] += 0.01
        if label == True:
            nx.draw_networkx_labels(self.G, pos, labels, font_size=8)
        limits = plt.axis('off')
        plt.show()

    # draw 3 dimensional verison of the graph (returning html object)
    def graph_3D(self):
        n = nx.edges(self.G)
        removeEdge = []
        for i in range(len(n)):
            if n[i][0] == '' or n[i][1] == '':
                removeEdge.append(n[i])
        for j in range(len(removeEdge)):
            n.remove(removeEdge[j])
        jgraph.draw(nx.edges(self.G), directed="true")

    # note: this is for Vinay's UI
    def plot_2D(self, attr, label=False):
        plt.clf()
        ontClass = nx.get_node_attributes(self.G, 'ontClass')
        pos = nx.fruchterman_reingold_layout(self.G)
        labels = {}
        for node in ontClass:
            labels[node] = node
        for node in set(self.classList):
            nx.draw_networkx_nodes(self.G, pos,
                                   with_labels=False,
                                   nodelist=[key for key, val in ontClass.items() if val == node],
                                   node_color=attr[node][0],
                                   node_size=attr[node][1],
                                   alpha=0.8)
        nx.draw_networkx_edges(self.G, pos, width=1.0, alpha=0.5)
        for key, value in pos.items():
            pos[key][1] += 0.01
        if label == True:
            nx.draw_networkx_labels(self.G, pos, labels, font_size=7)
        plt.axis('off')
        f = tempfile.NamedTemporaryFile(
            dir='out/sna',
            suffix='.png', delete=False)
        # save the figure to the temporary file
        plt.savefig(f, bbox_inches='tight')
        f.close()  # close the file
        # get the file's name
        # (the template will need that)
        plotPng = f.name.split('/')[-1]
        plotPng = plotPng.split('\\')[-1]
        return plotPng

    # create json file for 3 dimensional graph
    # name ex: {name, institution}, {faction leaders, institution}, etc...
    # color: {"0xgggggg", "0xaaaaaa"} etc. (Takes a hexadecimal "String").
    # returns a json dictionary
    def create_json(self, classes, color, graph=None):
        data = {}
        edges = []
        nodes_property = {}
        if graph is None:
            graph = self.G
        for edge in self.G.edges_iter():
            if graph[edge[0]][edge[1]].get("propsFlag") is True:
                # links with propensities can be given hex code colors for arrow, edge; can also change arrow size
                edges.append(
                    {'source': edge[0],
                     'target': edge[1],
                     'name': edge[0] + "," + edge[1],
                     'arrowColor': '0xE74C3C',
                     'arrowSize': 2})
            if graph[edge[0]][edge[1]].get('Predicted') is not None:
                edges.append(
                    {'source': edge[0],
                     'target': edge[1],
                     'name': edge[0] + "," + edge[1],
                     'color': '0xE74C3C',
                     'arrowColor': '0xE74C3C',
                     'arrowSize': 2})
            elif graph[edge[0]][edge[1]].get('W') is not None:
                edges.append(
                    {'source': edge[0],
                     'target': edge[1],
                     'name': edge[0] + "," + edge[1],
                     'arrowColor': '0x32CD32',
                     'arrowSize': 2})
            else:
                edges.append(
                    {'source': edge[0],
                     'target': edge[1],
                     'name': edge[0] + "," + edge[1]
                     }) #TODO clean up repeated code above
        for node in self.G.nodes_iter():
            temp = {}
            ontClass = self.G.node[node].get('ontClass')
            if graph.node[node].get('newNode') is True:
                temp['color'] = '0x8B0000'
            else:
                if ontClass is None:
                    temp['color'] = '0xD3D3D3'
                else:
                    temp['color'] = color[classes.index(ontClass)]
            if graph.node[node].get('Name') is not None:
                temp['name'] = graph.node[node].get('Name')[0]
            nodes_property[node] = temp
        data['edges'] = edges
        data['nodes'] = nodes_property
        return data