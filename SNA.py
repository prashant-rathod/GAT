import networkx as nx
from networkx.algorithms import bipartite as bi
from networkx.algorithms import centrality
# import csv, might deveop in order to read bith xlsx and csv
import xlrd
import matplotlib.pyplot as plt
import tempfile

class SNA():
    def __init__(self,excel_file, sheet):
        self.header, self.list = self.readFile(excel_file, sheet)
        self.G = nx.complete_multipartite_graph()
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
    # Read xlsx file and save the header and all the rows (vector) containing features
    # Input: xlsx file, sheet
    def readFile(self, excel_file, sheet):
        workbook = xlrd.open_workbook(excel_file)
        sh = workbook.sheet_by_name(sheet)
        header = [str(sh.cell(0,col).value).strip("\n") for col in range(sh.ncols)]
        New_ncols = sh.ncols - 1
        # If any, delete all the emtpy features in the header
        while header[New_ncols] == '':
            header.remove(header[New_ncols])
            New_ncols -= 1
        list = []
        for row in range(1,sh.nrows):
            tempList = []
            for col in range(New_ncols + 1):
                if type(sh.cell(row,col).value) == type(""):
                    tempList.append(sh.cell(row,col).value.strip("\n"))
                else:
                    tempList.append(str(sh.cell(row,col).value))
            list.append(tempList)
        return header,list
    #create set of nodes for bipartite graph
    # name = names of the node. This is defined by the header. ex: Abbasi-Davani.F: Name  or Abbasi-Davani.F: Faction leader
    # nodeSet = names that define a set of node. For example, we can define Person, Faction Leader, and Party Leader as "Agent"
    # note: len(name) = len(nodeSet), else code fails
    def createNodeList(self, name, nodeSet):
        # Need to specify what sets from data are attributes of other sets (e.g. is title an attribute of name, or vice versa?)
        header, list = self.header, self.list          #need to use header for role analysis
        featureNo = 0 # which feature is being assessed
        self.nodeSet = nodeSet
        for feature in name:
            #nodesCollected = []
            nodeList = [] # make this a container of (node, attribute dict) tuples https://networkx.github.io/documentation/networkx-1.9/reference/generated/networkx.DiGraph.add_nodes_from.html
            for row in list:
                counter = 0
                nodeAttr = {}
                for item in row:
                    if item != row[feature]:
                        #create dict with corresponding node set
                        nodeAttr[header[counter]] = item
                    if item == row[feature]:
                        if row[feature] not in [x['name'] for x in nodeList]:
                            nodeList.append({'name': row[feature], 'attributes': nodeAttr})
                            #nodesCollected.append
                    counter += 1
                # Add attributes based on header input
            for node in nodeList:
                self.G.add_node(node['name'],node['attributes'],bipartite=nodeSet[featureNo])
            featureNo+=1
        self.nodes = nx.nodes(self.G)
        print(self.nodes)
    #create a list of edges that connect among sets
    #This part is currently still testing.
    #Right now trying to see if the graph is displayed successfully, but later on need to add a argument that passes the
    #list of features that we want the graph to display in bipartite
    def createEdgeList(self, featureList):
        list = self.list
        edgeList = []
        for row in list:
            for i in range(len(featureList)):
                for j in range(len(featureList) - 1):
                    if (row[featureList[i]] != '' and row[featureList[j]] != '') and (row[featureList[i]] != row[featureList[j]]):
                        edgeList.append((row[featureList[i]],row[featureList[j]]))
        self.G.add_edges_from(edgeList)
        self.edges = edgeList
    def addEdges(self, pair):
        data = self.list
        newEdgeList = []
        for row in data:
            if (row[pair[0]] != '' and row[pair[1]] != '') and (row[pair[0]] != row[pair[1]]):
                newEdgeList.append((row[pair[0]], row[pair[1]]))
        self.G.add_edges_from(newEdgeList)
        self.edges.extend(newEdgeList)


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
        self.nodes = nx.nodes(self.G)
        for i in connections:
            print("connecting to:",i)
            self.G.add_edge(node,i)
            self.edges.append([node,i])

    def removeEdge(self, node1, node2):
        if self.G.has_edge(node1,node2):
            self.G.remove_edge(node1,node2)

    # Change an attribute of a node
    def changeAttribute(self, node,  value, attribute="bipartite"):
        if self.G.has_node(node):
            self.G.node[node][attribute] = value
            print("New attribute for "+node+": "+self.G.node[node][attribute])

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
        self.communicability_centrality()
        self.communicability_centrality_exp()

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
    # draw 2D graph
    # attr is a dictionary that has color and size as its value.
    def graph_2D(self, attr, label=False):
        bipartite = nx.get_node_attributes(self.G, 'bipartite')
        Nodes = nx.nodes(self.G)
        pos = nx.spring_layout(self.G)
        labels = {}
        for node in bipartite:
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
        jgraph.draw(nx.edges(self.G), directed="false")
    
    #note: this is for Vinay's UI
    def plot_2D(self, attr, label=False):
        plt.clf()
        bipartite = nx.get_node_attributes(self.G, 'bipartite')
        Nodes = nx.nodes(self.G)
        pos = nx.spring_layout(self.G)
        labels = {}
        for node in bipartite:
            labels[node] = node
        for node in set(self.nodeSet):
            nx.draw_networkx_nodes(self.G, pos,
                                   with_labels=False,
                                   node_color = attr[node][0],
                                   node_size = attr[node][1],
                                   alpha=0.8)
        nx.draw_networkx_edges(self.G, pos, width=1.0, alpha=0.5)
        for key,value in pos.items():
            pos[key][1] += 0.01
        if label == True:
            nx.draw_networkx_labels(self.G, pos, labels, font_size=8)
        limits=plt.axis('off')
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
        bipartite = nx.get_node_attributes(self.G, 'bipartite')
        for edge in self.edges:
            edges.append({'source': edge[0], 'target': edge[1]})
        for node, feature in bipartite.items():
            temp = {}
            temp['color'] = color[name.index(feature)]
            nodes_property[node] = temp
        data['edges'] = edges
        data['nodes'] = nodes_property
        return data


############
####TEST####
############
'''
Graph = SNA("iran.xlsx", "2011")
Graph.createNodeList([1,4], ["Agent", "Institution"])
Graph.createEdgeList([1,4])

# test = Graph.getNodes()
# Graph.graph_2D({"Agent":['y',50], "Institution":['b',50]}, label=True)
Graph.clustering()
Graph.latapy_clustering()
Graph.robins_alexander_clustering()
Graph.closeness_centrality()
Graph.betweenness_centrality()
Graph.degree_centrality()
Graph.katz_centrality()
Graph.eigenvector_centrality()
Graph.load_centrality()
Graph.communicability_centrality()
Graph.communicability_centrality_exp()
'''
# print(Graph.get_clustering())
# print(Graph.get_closeness_centrality())
# print(Graph.get_betweenness_centrality())
# print(Graph.get_degree_centrality())
# print(Graph.get_latapy_clustering())
# print(Graph.get_robins_alexander_clustering())
# print(Graph.get_katz_centrality())
# print(Graph.get_eigenvector_centrality())
# print(Graph.get_load_centrality())
# print(Graph.get_communicability_centrality())
# print(Graph.get_communicability_centrality_exp())



