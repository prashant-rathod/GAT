import tempfile
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import xlrd
from networkx.algorithms import bipartite as bi
from networkx.algorithms import centrality
import pandas as pd
import datetime

# Initializing graph for test case:
Graph = SNA("24OCT.xlsx", nodeSheet="Data Sheet", attrSheet="Attributes")
Graph.createNodeList(["ID"])
test = Graph.getNodes()
G = nx.Graph()
Graph.loadAttributes()

# Creating an attribute list and setting its length for the conditional iterations:
b = Graph.attrList
edgeList = []
actorList = []
beliefList = []
symbolsList = []
resourceList =[]
agentList = []
orgList = []
audList = []
eventList = []
roleList = []
knowList = []
taskModelList = []
locationList = []
titleList = []
positionList = []

# iterating through ontological entities to create text network
y = len(b)
for x in range(0, y):
    for q in range(0, len(b[x])):
        if b[x][q]['header'] == 'ID' and b[x][q]['val'] is not None:
            actorList.append(b[x][q]['val'])
            G.add_node(b[x][q]['val'])

        if b[x][q]['header'] == 'Belief' and b[x][q]['val'] is not None:
            beliefList.append(b[x][q]['val'])
            edgeList.append((actorList[x], b[x][q]['val'], (b[x][q+1]['val'])))
            G.add_weighted_edges_from(edgeList, 'W')


        if b[x][q]['header'] == 'Symbols' and b[x][q]['val'] is not None:
            symbolsList.append(b[x][q]['val'])
            edgeList.append((actorList[x], b[x][q]['val'], (b[x][q+1]['val'])))
            G.add_weighted_edges_from(edgeList, 'W')


        if b[x][q]['header'] == 'Resource' and b[x][q]['val'] is not None:
            resourceList.append(b[x][q]['val'])
            edgeList.append((actorList[x], b[x][q]['val'], (b[x][q+1]['val'])))
            G.add_weighted_edges_from(edgeList, 'W')


        if b[x][q]['header'] == 'Agent' and b[x][q]['val'] is not None:
            agentList.append(b[x][q]['val'])
            edgeList.append((actorList[x], b[x][q]['val'], (b[x][q+1]['val'])))
            G.add_weighted_edges_from(edgeList, 'W')


        if b[x][q]['header'] == 'Organization' and b[x][q]['val'] is not None:
            orgList.append(b[x][q]['val'])
            edgeList.append((actorList[x], b[x][q]['val'], (b[x][q+1]['val'])))
            G.add_weighted_edges_from(edgeList, 'W')


        if b[x][q]['header'] == 'Event' and b[x][q]['val'] is not None:
            eventList.append(b[x][q]['val'])
            edgeList.append((actorList[x], b[x][q]['val'], (b[x][q+1]['val'])))
            G.add_weighted_edges_from(edgeList, 'W')


        if b[x][q]['header'] == 'Title' and b[x][q]['val'] is not None:
            titleList.append(b[x][q]['val'])
            edgeList.append((actorList[x], b[x][q]['val'], (b[x][q+1]['val'])))
            G.add_weighted_edges_from(edgeList, 'W')

        if b[x][q]['header'] == 'Audience' and b[x][q]['val'] is not None:
            audList.append(b[x][q]['val'])
            edgeList.append((actorList[x], b[x][q]['val'], ((float(b[x][q+1]['val'])) + float((b[x][q+2]['val'])) / 2)))
            G.add_weighted_edges_from(audList, 'W')

actorList = set(actorList)
beliefList = set(beliefList)
symbolsList = set(symbolsList)
resourceList = set(resourceList)
agentList = set(agentList)
orgList =  set(orgList)
audList = set(audList)
eventList = set(eventList)
roleList = set(roleList)
knowList = set(knowList)
taskModelList = set(taskModelList)
locationList = set(locationList)
titleList = set(titleList)
positionList = set(positionList)

color_map = []
for x in nx.nodes(G):
    if x in actorList:
        G.node[x]['ontClass'] = 'Actor'
        color_map.append('#D3D3D3')

    if x in beliefList:
        G.node[x]['ontClass'] = 'Belief'
        color_map.append('#FF4933')

    if x in symbolsList:
        G.node[x]['ontClass'] = 'Symbol'
        color_map.append('#FFD133')

    if x in resourceList:
        G.node[x]['ontClass'] = 'Resource'
        color_map.append('#ACFF33')

    if x in agentList:
        G.node[x]['ontClass'] = 'Agent'
        color_map.append('#8C8C8C')

    if x in orgList:
        G.node[x]['ontClass'] = 'Organization'
        color_map.append('#11C694')

    if x in audList:
        G.node[x]['ontClass'] = 'Audience'
        color_map.append('#11A0C6')

    if x in eventList:
        G.node[x]['ontClass'] = 'Event'

    if x in roleList:
        G.node[x]['ontClass'] = 'Role'
        color_map.append('#1187C6')

    if x in knowList:
        G.node[x]['ontClass'] = 'Knowledge'
        color_map.append('#113AC6')

    if x in taskModelList:
        G.node[x]['ontClass'] = 'Task Model'
        color_map.append('#5311C6')

    if x in locationList:
        G.node[x]['ontClass'] = 'Location'
        color_map.append('#B311C6')

    if x in titleList:
        G.node[x]['ontclass'] = 'Title'
        color_map.append('#C61176')

    if x in positionList:
        G.node[x]['ontClass'] = 'Position'
        color_map.append('#F57575')

print(nx.info(G))
print(G.edges(data=True))
pos = nx.fruchterman_reingold_layout(G)
plt.title('Test 24 OCT')
colors = range(len(G.edges()))
nx.draw(G,
       node_color=color_map,
       alpha=.8,
       edge_color=colors,
       edge_cmap=plt.cm.Blues,
       with_labels=True,
       font_size=8)
plt.show()

# import attacks xlsx into pandas
df = pd.read_excel("attacks_sub.xlsx")
bombData = df.to_dict(orient='index')
for x in range(0, len(bombData)):
    bombData[x]['Date'] = datetime.datetime.strptime(str(bombData[x]['Date']), '%Y%m%d')
print(bombData)
y = len(bombData)

# using datetime to create iterations of flexible length
dateList = [bombData[x]['Date'] for x in bombData]
dateIter = (max(dateList) - min(dateList)) / 10

nodeList_0 = [(bombData[x]['Source'], bombData[x]['Target']) for x in bombData if bombData[x]['Date'] <= min(dateList) + dateIter]
nodeList_1 = [(bombData[x]['Source'], bombData[x]['Target']) for x in bombData if min(dateList) + dateIter <= bombData[x]['Date'] < min(dateList) + dateIter*2]
nodeList_2 = [(bombData[x]['Source'], bombData[x]['Target']) for x in bombData if min(dateList) + dateIter*2 <= bombData[x]['Date'] < min(dateList) + dateIter*3]
nodeList_3 = [(bombData[x]['Source'], bombData[x]['Target']) for x in bombData if min(dateList) + dateIter*3 <= bombData[x]['Date'] < min(dateList) + dateIter*4]
nodeList_4 = [(bombData[x]['Source'], bombData[x]['Target']) for x in bombData if min(dateList) + dateIter*4 <= bombData[x]['Date'] < min(dateList) + dateIter*5]
nodeList_5 = [(bombData[x]['Source'], bombData[x]['Target']) for x in bombData if min(dateList) + dateIter*5 <= bombData[x]['Date'] < min(dateList) + dateIter*6]
nodeList_6 = [(bombData[x]['Source'], bombData[x]['Target']) for x in bombData if min(dateList) + dateIter*6 <= bombData[x]['Date'] < min(dateList) + dateIter*7]
nodeList_7 = [(bombData[x]['Source'], bombData[x]['Target']) for x in bombData if min(dateList) + dateIter*7 <= bombData[x]['Date'] < min(dateList) + dateIter*8]
nodeList_8 = [(bombData[x]['Source'], bombData[x]['Target']) for x in bombData if min(dateList) + dateIter*8 <= bombData[x]['Date'] < min(dateList) + dateIter*9]
nodeList_9 = [(bombData[x]['Source'], bombData[x]['Target']) for x in bombData if min(dateList) + dateIter*9 <= bombData[x]['Date'] < min(dateList) + dateIter*10]

# adding attacks to test graph by datetime period and iterating through to change sentiments
iterEdgeList = []
G.add_nodes_from(nodeList_0[0])
for node in nodeList_0[0]:
    for others in G.nodes():
            if G.has_edge(node[0], others):
                sent = G.get_edge_data(node, others)
                iterEdgeList.append((node, others, (sent[node, others] * .1) + sent[node, others]))
print("iteration 0 = ", G.edges(data=True))
G.add_weighted_edges_from(iterEdgeList, 'W')

G.add_nodes_from(nodeList_1[0])
for node in nodeList_1[0]:
    for others in G.nodes():
            if G.has_edge(node[0], others):
                sent = G.get_edge_data(node, others)
                iterEdgeList.append((node, others, (sent[node, others] * .1) + sent[node, others]))
print("iteration 1 = ", G.edges(data=True))
G.add_weighted_edges_from(iterEdgeList, 'W')

G.add_nodes_from(nodeList_2[0])
for node in nodeList_2[0]:
    for others in G.nodes():
            if G.has_edge(node[0], others):
                sent = G.get_edge_data(node, others)
                iterEdgeList.append((node, others, (sent[node, others] * .1) + sent[node, others]))
print("iteration 2 = ", G.edges(data=True))
G.add_weighted_edges_from(iterEdgeList, 'W')

G.add_nodes_from(nodeList_3[0])
for node in nodeList_3[0]:
    for others in G.nodes():
            if G.has_edge(node[0], others):
                sent = G.get_edge_data(node, others)
                iterEdgeList.append((node, others, (sent[node, others] * .1) + sent[node, others]))
print("iteration 3 = ", G.edges(data=True))
G.add_weighted_edges_from(iterEdgeList, 'W')

G.add_nodes_from(nodeList_4[0])
for node in nodeList_4[0]:
    for others in G.nodes():
            if G.has_edge(node[0], others):
                sent = G.get_edge_data(node, others)
                iterEdgeList.append((node, others, (sent[node, others] * .1) + sent[node, others]))
print("iteration 4 = ", G.edges(data=True))
G.add_weighted_edges_from(iterEdgeList, 'W')

G.add_nodes_from(nodeList_5[0])
for node in nodeList_5[0]:
    for others in G.nodes():
            if G.has_edge(node[0], others):
                sent = G.get_edge_data(node, others)
                iterEdgeList.append((node, others, (sent[node, others] * .1) + sent[node, others]))
print("iteration 5 = ", G.edges(data=True))
G.add_weighted_edges_from(iterEdgeList, 'W')

G.add_nodes_from(nodeList_6[0])
for node in nodeList_6[0]:
    for others in G.nodes():
            if G.has_edge(node[0], others):
                sent = G.get_edge_data(node, others)
                iterEdgeList.append((node, others, (sent[node, others] * .1) + sent[node, others]))
print("iteration 6 = ", G.edges(data=True))
G.add_weighted_edges_from(iterEdgeList, 'W')

G.add_nodes_from(nodeList_7[0])
for node in nodeList_7[0]:
    for others in G.nodes():
            if G.has_edge(node[0], others):
                sent = G.get_edge_data(node, others)
                iterEdgeList.append((node, others, (sent[node, others] * .1) + sent[node, others]))
print("iteration 7 = ", G.edges(data=True))
G.add_weighted_edges_from(iterEdgeList, 'W')

G.add_nodes_from(nodeList_8[0])
for node in nodeList_8[0]:
    for others in G.nodes():
            if G.has_edge(node[0], others):
                sent = G.get_edge_data(node, others)
                iterEdgeList.append((node, others, (sent[node, others] * .1) + sent[node, others]))
print("iteration 8 = ", G.edges(data=True))
G.add_weighted_edges_from(iterEdgeList, 'W')

G.add_nodes_from(nodeList_9[0])
for node in nodeList_9[0]:
    for others in G.nodes():
            if G.has_edge(node[0], others):
                sent = G.get_edge_data(node, others)
                iterEdgeList.append((node, others, (sent[node, others] * .1) + sent[node, others]))
print("iteration 9 = ", G.edges(data=True))
G.add_weighted_edges_from(iterEdgeList, 'W')

