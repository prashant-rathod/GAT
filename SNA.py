import networkx as nx
from networkx.algorithms import bipartite as bi
from networkx.algorithms import centrality
# import csv, might deveop in order to read bith xlsx and csv
import xlrd
import matplotlib.pyplot as plt
import tempfile
import random
import numpy as np
import scipy as sp

class SNA():
    def __init__(self, excel_file, nodeSheet, attrSheet = None):
        self.subAttrs = ["W", "SENT", "SZE", "AMT"]
        self.header, self.list = self.readFile(excel_file, nodeSheet)
        if attrSheet != None:
            self.attrHeader, self.attrList = self.readFile( excel_file, attrSheet)
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
        self.katz_centraltiy_dict={}
        self.load_centrality_dict = {}
        self.communicability_centrality_dict = {}
        self.communicability_centrality_exp_dict = {}
        self.node_attributes_dict = {}
        self.nodeSet = []
        self.attrSheet = attrSheet

    # Read xlsx file and save the header and all the cells, each a dict with value and header label
    # Input: xlsx file, sheet
    def readFile(self, excel_file, sheet):

        workbook = xlrd.open_workbook(excel_file)
        sh = workbook.sheet_by_name(sheet)
        header = [str(sh.cell(0,col).value).strip("\n") for col in range(sh.ncols)]
        New_ncols = sh.ncols - 1

        # If any, delete all the empty features in the header
        while header[New_ncols] == '':
            header.remove(header[New_ncols])
            New_ncols -= 1

        # a list of nodes
        list = []
        for row in range(1,sh.nrows):
            tempList = []
            for col in range(New_ncols + 1):
                feature = str(sh.cell(0, col).value).strip("\n")
                cell = sh.cell(row,col).value
                if type(cell) == type(""):
                    val = cell.strip("\n")
                else:
                    val = str(cell)
                if val != "": # handle empty cells
                    # Make each node a dict with node name and node header, to assign later
                    tempList.append({'val': val, 'header': feature}) # need to define attributes later
            list.append(tempList)

        # remove repeated column titles
        consolidatedHeader = []
        for feature in header:
            if ( feature not in consolidatedHeader ) and ( feature not in self.subAttrs ) :
                consolidatedHeader.append(feature)

        return consolidatedHeader,list

    #create set of nodes for multipartite graph
    # name = names of the node. This is defined by the header. ex: Abbasi-Davani.F: Name  or Abbasi-Davani.F: Faction leader
    # nodeSet = names that define a set of node. For example, we can define Person, Faction Leader, and Party Leader as "Agent"
    # note: len(name) = len(nodeSet), else code fails
    def createNodeList(self, nodeSet):
        for row in self.list:
            for node in row:
                if node['header'] in nodeSet and node['val'] != "":
                    # strip empty cells
                    self.G.add_node(node['val'], block=node['header'])
        self.nodeSet = nodeSet
        self.nodes = nx.nodes(self.G)

    # Input: header list and list of attributes with header label from attribute sheet
    # Output: updated list of nodes with attributes
    def loadAttributes(self):
        #print("header",self.attrHeader)
        #print("list",self.attrList)
        for row in self.attrList:
            nodeID = row[0]['val']
            for cell in row[1:]:
                if cell['val'] != '':
                    if nodeID in self.nodes:
                        attrList = []
                        node = self.G.node[nodeID]
                        if cell['header'] in self.subAttrs:  # handle subattributes, e.g. weight
                            prevCell = row[row.index(cell) - 1]
                            key = {}
                            while prevCell['header'] in self.subAttrs:
                                key[prevCell['header']] = prevCell['val']
                                prevCell = row[row.index(prevCell) - 1]
                            key[cell['header']] = cell['val']
                            for value in node[prevCell['header']]:
                                #print("AttrList 108:",attrList)
                                if prevCell['val'] in value:
                                    listFlag = True if type(value) is list else False
                                    attrList.append([value[0],key] if listFlag else [value,key])
                                else:
                                    attrList.append(value)
                            attrID = prevCell['header']
                            # add the attribute as an attr-of-attr
                        else: # if the attribute is not a subattribute
                            if cell['header'] in self.G.node[nodeID]:
                                attrList = (node[cell['header']])
                            attrList.append(cell['val'])
                            attrID = cell['header']
                        self.changeAttribute(nodeID,attrList,attrID)

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
                        edgeList.append( (source,node['val']) ) # create a new link
        self.G.add_edges_from(edgeList)
        self.edges = edgeList
        #print("edges",self.G.edges())

    def addEdges(self, pair): # deprecated, needs fixing - doesn't handle new dict structure
        data = self.list
        #print(self.nodes)
        newEdgeList = []
        for row in data:
            first = row[pair[0]]['val']
            second = row[pair[1]]['val']
            if (first != '' and second != '') and (first != second):
                newEdgeList.append((first, second))
        self.G.add_edges_from(newEdgeList)
        self.edges.extend(newEdgeList)

    def calculatePropensities(self,emo=True,role=True):
        for edge in self.edges: # for every edge, calculate propensities and append as an attribute
            emoPropList = self.propCalc(edge)[0] if emo else None
            self.G[edge[0]][edge[1]]['Emotion'] = emoPropList if len(emoPropList)>0 else None

            rolePropList = self.propCalc(edge)[1] if role else None
            self.G[edge[0]][edge[1]]['Role'] = rolePropList if len(rolePropList) > 1 else None

            inflPropList = self.propCalc(edge)[2] if role else None
            self.G[edge[0]][edge[1]]['Role'] = inflPropList if len(inflPropList) > 1 else None

        self.edges = nx.edges(self.G)

    def propCalc(self, edge):
        emoProps = []
        roleProps = []
        inflProps = []
        emoAttrSet = ["Belief","Symbol","Agent"]
        roleAttrSet = ["Belief","Resource"]
        oppPairs = [
            ("IDBNATTUR", "IDBNATKUR"),
            ("IDBNATTUR","IDBPROUSA"),
            ('ROBMOSSUN', 'ROBMOSSHI'),
            ('IDBVEL', 'IDBSEC'),
            ('POBNOT', 'IDBNATIRQ'),
            ('POBNOT', 'IDBNATKUR'),
            ('POBNOT', 'IDBNATIRN'),
            ('IDBNATIRN', 'IDBNATIRQ'),
            ('ROBANTJEW', 'ROBMOSSHI'),
            ('TURGOVHOS_ERD', 'TURGOVHOS_ATA'),
            ('TURGOVHOS_ERD', 'FLGTUR'),
            ('IRQGOVHOS', 'IRNGOVHOG'),
            ('TURGOVHOS_ERD', 'IRNGOVHOS_KAM'),
            ('IDBJHD','IDBPROUSA'),
            ('IDBANT_IMGMOSISS','IDBJHD'),
            ('IRQGOV','IMGMOSISS'),
            ('IRNGOV','IMGMOSISS'),
            ('POBNATIRQ','POBNATTUR'),
            ('BELMS', 'BELSHI'),
            ('BELAMH', 'BELNEO'),
            ('BELKUR', 'BELNEO'),
            ('BELAMH', 'BELIRH'),
            ('BELPIS', 'BELIMS'),
            ('BELSHI', 'BELSUN'),
            ('BELUIQ', 'BELKUR'),
        ]
        compPairs = [
            ('IDBPROUSA', 'IDBPROEUR'),
            ('IDBANTEUR', 'IDBANTUSA'),
            ('POBNOT', 'IDBNATTUR'),
            ('FLGKUR', 'TURGOVHOS_ERD'),
            ('LANKUR', 'FLGTUR'),
            ('IRQGOVHOG_ABD', 'TURGOVHOS_ERD'),
            ('TURGOVHOS_ERD', 'IRQKURKRG_HOS'),
            ('TURGOVHOS_ERD', 'TURGOVSPM_KIL'),
            ('ROBMOSSUN','IDBJHD'),
            ('FLGTUR','POBNOT'),
            ('BELIRH', 'BELUIQ'),
            ('BELAMH', 'BELPIS'),
            ('BELAMH', 'BELKUR'),
            ('BELAMH', 'BELIMS'),
            ('BELAMH', 'BELUIQ'),
            ('BELSUN', 'BELNEO'),
        ]
        source = self.G.node[edge[0]]
        target = self.G.node[edge[1]]
        # Check if role attribute is present; if not, no role propensities calculated
        roleFlag = True if source.get("Role") is not None and target.get("Role") is not None else False
        for attr in ( target if len(source) > len(target) else source ):
            if attr not in ['block','newNode','Name'] and source.get(attr) is not None and target.get(attr) is not None:
                for src_val in [x for x in source.get(attr) if len(x) > 1]:
                    for trg_val in [x for x in target.get(attr) if len(x) > 1]:
                        #####################################
                        ### Propensity assignment section ###
                        #####################################
                        ## Emotion Propensities
                        src_w = float(src_val[1]["W"]) if "W" in src_val[1] else None
                        trg_w = float(trg_val[1]["W"]) if "W" in trg_val[1] else None

                        if src_w is not None and trg_w is not None:
                            # Cooperative propensities
                            if src_val[0] == trg_val[0]:
                                # Checking to see if each node's attribute weights fall within specified ranges:
                                if src_w >= 0.6 and trg_w >= 0.6:
                                    emoProps.append(("Trust",attr,src_val[0],trg_val[0],src_w,trg_w))
                                else: # all others are joy
                                    emoProps.append(("Joy", attr, src_val[0], trg_val[0],src_w,trg_w))
                                    # print("Appended Joy using attribute", attr, "(", src_val, "&", trg_val, ")",
                                    #       "for node pair (", source, ",", target, ")")

                            elif attr in emoAttrSet:
                                # Competitive propensities
                                if (src_val[0], trg_val[0]) in compPairs or (trg_val[0],src_val[0]) in compPairs:
                                # Checking to see if each node's attribute weights fall within specified ranges:
                                    if src_w < 0.6 and trg_w < 0.6:
                                        emoProps.append(("Surprise", attr, src_val[0], trg_val[0],src_w,trg_w))
                                    else:
                                        emoProps.append(("Anticipation", attr, src_val[0], trg_val[0],src_w,trg_w))

                                # Coercive propensities:
                                elif (src_val[0], trg_val[0]) in oppPairs or (trg_val[0],src_val[0]) in oppPairs:
                                    # Checking to see if each node's attribute weights fall within specified ranges:
                                    if (src_w >= 0.8 and trg_w >= 0.6) or (src_w >= 0.6 and trg_w >= 0.6):
                                        emoProps.append(("Anger", attr, src_val[0], trg_val[0],src_w,trg_w))
                                    elif (src_w >= 0.6 and trg_w >= 0.4) or (src_w >= 0.4 and trg_w >= 0.6):
                                        emoProps.append(("Sadness", attr, src_val[0], trg_val[0],src_w,trg_w))
                                    elif (src_w >= 0.4 and trg_w >= 0.2) or (src_w >= 0.2 and trg_w >= 0.4):
                                        emoProps.append(("Fear", attr, src_val[0], trg_val[0],src_w,trg_w))
                                    elif (src_w >= 0.8 and trg_w >= 0.2) or (src_w >= 0.2 and trg_w >= 0.8):
                                        emoProps.append(("Disgust", attr, src_val[0], trg_val[0],src_w,trg_w))

                        ## Role Propensities
                        # Still need to add conditional opposites, like in emotion

                        src_amt = float(src_val[1]["AMT"]) if attr == "Resource" and "AMT" in src_val[1] else None
                        trg_amt = float(trg_val[1]["AMT"]) if attr == "Resource" and "AMT" in trg_val[1] else None
                        if roleFlag and attr in roleAttrSet:
                            if src_val[0] == trg_val[0]:
                                roleProps.append(["Consumer or Provider",.5] if attr == "Resource" else None)
                                # print("Appended Cons. or Prov. using attribute", attr, "(", src_val, "&", trg_val, ")",
                                #       "for node pair (", source, ",", target, ")")
                                roleProps.append(["Protector",.75] if attr == "Belief" else None)
                                # print("Appended Protector using attribute", attr, "(", src_val, "&", trg_val, ")",
                                #       "for node pair (", source, ",", target, ")")

        return emoProps, roleProps, inflProps

    # copy the origin social network graph created with user input data.
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

    def addNode(self,node,attrDict={}, connections=[]):
        self.G.add_node(node,attrDict)
        for i in connections:
            #print("connecting to:",i)
            self.G.add_edge(node,i)
        for k in attrDict: # add attributes based on user input
            self.changeAttribute(node,[attrDict[k]],k)
        self.changeAttribute(node,True,'newNode')

        ## Smart prediction prototype
        for target in self.nodes:
            emoProps, roleProps, inflProps = self.propCalc((node,target))
            if len(emoProps) > 0:
                w = []
                for prop in emoProps:
                    w.append(prop[4] * prop[5]) # add the product of the attribute weights to a list for each prop
                w_avg = np.average(w) # find average propensity product weight
                prob = np.random.binomial(1, w_avg*1/2)
                # use w_avg as the probability for a bernoulli distribution
                if prob:
                    self.G.add_edge(node, target)
                    self.G[node][target]['Emotion'] = emoProps
                    self.G[node][target]['Role'] = roleProps if len(roleProps) > 0 else None
                    self.G[node][target]['Influence'] = inflProps if len(inflProps) > 0 else None
                    self.G[node][target]['Predicted'] = True


        self.nodes = nx.nodes(self.G) # update node list
        self.edges = nx.edges(self.G) # update edge list

    def removeEdge(self, node1, node2):
        if self.G.has_edge(node1,node2):
            self.G.remove_edge(node1,node2)

    # Change an attribute of a node
    def changeAttribute(self, node,  value, attribute="bipartite"):
        if self.G.has_node(node):
            self.G.node[node][attribute] = value
            #print("New attribute for "+node+": "+str(self.G.node[node][attribute]))
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


    #set all the properties with this function.
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
        self.communicability_centrality() # Not available for directed graphs
        self.communicability_centrality_exp()
        self.node_connectivity()
        self.average_clustering()

    def find_cliques(self):
        G = self.G.copy().to_undirected() # currently need undirected graph to find cliques with centrality method
        cliques = []

        # Find central nodes
        centralities = [self.eigenvector_centrality_dict.get(node) for node in G.nodes()]
        scaled = list(sp.stats.zscore(centralities))
        for i in range(len(scaled)):
            scaled[i] = (G.nodes()[i],scaled[i])
        selected = [key for key,val in scaled if "BEL" in key] # used z-score for top 20th percentile, temporary change to only show beliefs
        # TODO change back line above to "if val > 1.3" instead of "if 'BEL' in key"
        # Make subgraphs from those nodes
        def find_subgraph(centralNode,subGraph,depth):
                nodeList = [(centralNode,target) for target in G.neighbors(centralNode)]
                sub_G.add_edges_from(nodeList)
                if depth > 0:
                    for ancillary in G.neighbors(centralNode):
                        find_subgraph(ancillary,subGraph,depth-1)
        for centralNode in selected:
            sub_G = nx.DiGraph()
            find_subgraph(centralNode,sub_G,2)
            if len(list(sub_G.nodes())) > 5:
                cliques.append(sub_G.to_undirected())

        return cliques

    def averagePathRes(self,ta=20,iters=5):

        scaledResilienceDict = {}
        toScale = []
        cliques = self.find_cliques()

        # Find resilience of subgraphs
        for clique in cliques:

            initShortestPath = nx.average_shortest_path_length(clique)
            t0 = 0
            finShortestPathList = []

            # function to estimate integral
            def integral(x0, x1, rectangles):
                width = (float(x1) - float(x0)) / rectangles
                sum1 = 0
                for i in range(rectangles):
                    height = qw_shortestPath * (float(x0) + i * width)
                    area = height * width
                    sum1 += area
                return sum1

            # creating perturbation by removing random 10% of nodes and averaging result of x iterations
            for k in range(0, iters):  # x can be changed here
                G = clique.copy()
                nList = G.nodes()
                nNumber = G.number_of_nodes()
                sample = int(nNumber * 0.1)  # percent of nodes removed can be changed here
                rSample = random.sample(nList, sample)
                G.remove_nodes_from(rSample)

                # finding shortest path of largest subgraph in G after perturbation:
                # (average shortest path cannot be calculated if a graph has unconnected nodes)
                l = []
                for g in nx.connected_component_subgraphs(G):
                    l.append(len(g.edges()))
                    if len(g.edges()) == max(l) and len(g.edges()) != 0:
                        finShortestPathList.append(nx.average_shortest_path_length(g, weight='Salience'))
            # find mean of average shortest path from each iteration:
            finShortestPath = np.mean(finShortestPathList)

            # solve for resilience using integral function:
            qw_shortestPath = float(finShortestPath) / float(initShortestPath)
            t1 = t0 + ta
            resilience = integral(t0, t1, 5) / t1

            # add to list: resilience measure for each clique
            toScale.append(resilience)

        # scale resilience measures on a normal scale
        for i in range(len(cliques)):
            scaledResilienceDict[cliques[i].nodes()[0]] = sp.stats.percentileofscore(toScale,toScale[i])

        return scaledResilienceDict

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
        self.eigenvector_centrality_dict = nx.eigenvector_centrality(self.G)
        #self.eigenvector_centrality_dict = nx.eigenvector_centrality_numpy(self.G)
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
    def get_node_attributes(self,node):
        return self.G.node[node]
    def get_eigenvector_centrality(self, lst=[]):
        if len(lst) == 0:
            return self.eigenvector_centrality_dict
        else:
            sub_dict={}
            for key,value in self.clustering_dict:
                if key in lst:
                    sub_dict[key] = value
            return sub_dict
    def get_clustering(self, lst=[]):
        if len(lst) == 0:
            return self.clustering_dict
        else:
            sub_dict = {}
            for key,value in self.clustering_dict:
                if key in lst:
                    sub_dict[key] = value
            return sub_dict
    def get_latapy_clustering(self, lst=[]):
        if len(lst) == 0:
            return self.latapy_clustering_dict
        else:
            sub_dict={}
            for key, value in self.latapy_clustering_dict:
                if key in lst:
                    sub_dict[key] = value
            return sub_dict
    def get_robins_alexander_clustering(self, lst=[]):
        if len(lst) == 0:
            return self.robins_alexander_clustering_dict
        else:
            sub_dict={}
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

    # additional network-wide measures
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

    # draw 2D graph
    # attr is a dictionary that has color and size as its value.
    def graph_2D(self, attr, label=False):
        block = nx.get_node_attributes(self.G, 'block')
        Nodes = nx.nodes(self.G)
        pos = nx.spring_layout(self.G)
        labels = {}
        for node in block:
            labels[node] = node
        for node in set(self.nodeSet):
            nx.draw_networkx_nodes(self.G, pos,
                                   with_labels=False,
                                   nodelist = [n for n in Nodes if bipartite[n] == node],
                                   node_color = attr[node][0],
                                   node_size = attr[node][1],
                                   alpha=0.8)
        nx.draw_networkx_edges(self.G, pos, width=1.0, alpha=0.5)
        for key,value in pos.items():
            pos[key][1] += 0.01
        if label == True:
            nx.draw_networkx_labels(self.G, pos, labels, font_size=8)
        limits=plt.axis('off')
        plt.show()

    #draw 3 dimensional verison of the graph (returning html object)
    def graph_3D(self):
        n = nx.edges(self.G)
        removeEdge=[]
        for i in range(len(n)):
            if n[i][0] == '' or n[i][1] == '':
                removeEdge.append(n[i])
        for j in range(len(removeEdge)):
            n.remove(removeEdge[j])
        jgraph.draw(nx.edges(self.G), directed="true")

    #note: this is for Vinay's UI
    def plot_2D(self, attr, label=False):
        #print("attr", attr)
        plt.clf()
        block = nx.get_node_attributes(self.G, 'block')
        #print("block",block)
        pos = nx.spring_layout(self.G)
        labels = {}
        for node in block:
            labels[node] = node
            #print("node",node)
        for node in set(self.nodeSet):
            #print("Node",node)
            #print("attr[node]",attr[node])
            nx.draw_networkx_nodes(self.G, pos,
                                   with_labels=False,
                                   nodelist = [key for key, val in block.items() if val == node],
                                   node_color = attr[node][0],
                                   node_size = attr[node][1],
                                   alpha=0.8)
        nx.draw_networkx_edges(self.G, pos, width=1.0, alpha=0.5)
        for key,value in pos.items():
            pos[key][1] += 0.01
        if label == True:
            nx.draw_networkx_labels(self.G, pos, labels, font_size=7)
        plt.axis('off')
        f = tempfile.NamedTemporaryFile(
            dir='static/temp',
            suffix = '.png', delete=False)
        # save the figure to the temporary file
        plt.savefig(f, bbox_inches='tight')
        f.close() # close the file
        # get the file's name
        # (the template will need that)
        plotPng = f.name.split('/')[-1]
        plotPng = plotPng.split('\\')[-1]
        return plotPng

    #create json file for 3 dimensional graph
    #name ex: {name, institution}, {faction leaders, institution}, etc...
    #color: {"0xgggggg", "0xaaaaaa"} etc. (Takes a hexadecimal "String").
    #returns a json dictionary
    def create_json(self, name, color):
        data = {}
        edges = []
        nodes_property = {}
        block = nx.get_node_attributes(self.G, 'block')
        for edge in self.edges:
            if self.G[edge[0]][edge[1]].get('Emotion') is not None:
                # links with propensities can be given hex code colors for arrow, edge; can also change arrow size
                edges.append({'source': edge[0], 'target': edge[1], 'name': edge[0] + "," + edge[1], 'arrowColor':'0xE74C3C', 'arrowSize':2})
            if self.G[edge[0]][edge[1]].get('Predicted') is not None:
                edges.append(
                    {'source': edge[0], 'target': edge[1], 'name': edge[0] + "," + edge[1], 'color':'0xE74C3C', 'arrowColor': '0xE74C3C',
                     'arrowSize': 2})
            else:
                edges.append(
                    {'source': edge[0], 'target': edge[1], 'name': edge[0] + "," + edge[1]})
        for node, feature in block.items():
            temp = {}
            if self.G.node[node].get('newNode') is True:
                temp['color'] = '0x8B0000'
            else:
                temp['color'] = color[name.index(feature)]
            nodes_property[node] = temp
        data['edges'] = edges
        data['nodes'] = nodes_property
        return data
