import pandas as pd
import datetime


def event_update(event_sheet):
    # input: spreadsheet of bomb attacks
    # output: updated dict of sentiment changes for each of attack events
    df = pd.read_excel(event_sheet)
    bombData = df.to_dict(orient='index')
    for x in range(0, len(bombData)):
        bombData[x]['Date'] = datetime.datetime.strptime(str(bombData[x]['Date']), '%Y%m%d')

    # using datetime to create iterations of flexible length
    dateList = [bombData[x]['Date'] for x in bombData]
    dateIter = (max(dateList) - min(dateList)) / 10

    nodeList_0 = [(bombData[x]['Source'], bombData[x]['Target']) for x in bombData if
                  bombData[x]['Date'] <= min(dateList) + dateIter]
    nodeList_1 = [(bombData[x]['Source'], bombData[x]['Target']) for x in bombData if
                  min(dateList) + dateIter <= bombData[x]['Date'] < min(dateList) + dateIter * 2]
    nodeList_2 = [(bombData[x]['Source'], bombData[x]['Target']) for x in bombData if
                  min(dateList) + dateIter * 2 <= bombData[x]['Date'] < min(dateList) + dateIter * 3]
    nodeList_3 = [(bombData[x]['Source'], bombData[x]['Target']) for x in bombData if
                  min(dateList) + dateIter * 3 <= bombData[x]['Date'] < min(dateList) + dateIter * 4]
    nodeList_4 = [(bombData[x]['Source'], bombData[x]['Target']) for x in bombData if
                  min(dateList) + dateIter * 4 <= bombData[x]['Date'] < min(dateList) + dateIter * 5]
    nodeList_5 = [(bombData[x]['Source'], bombData[x]['Target']) for x in bombData if
                  min(dateList) + dateIter * 5 <= bombData[x]['Date'] < min(dateList) + dateIter * 6]
    nodeList_6 = [(bombData[x]['Source'], bombData[x]['Target']) for x in bombData if
                  min(dateList) + dateIter * 6 <= bombData[x]['Date'] < min(dateList) + dateIter * 7]
    nodeList_7 = [(bombData[x]['Source'], bombData[x]['Target']) for x in bombData if
                  min(dateList) + dateIter * 7 <= bombData[x]['Date'] < min(dateList) + dateIter * 8]
    nodeList_8 = [(bombData[x]['Source'], bombData[x]['Target']) for x in bombData if
                  min(dateList) + dateIter * 8 <= bombData[x]['Date'] < min(dateList) + dateIter * 9]
    nodeList_9 = [(bombData[x]['Source'], bombData[x]['Target']) for x in bombData if
                  min(dateList) + dateIter * 9 <= bombData[x]['Date'] < min(dateList) + dateIter * 10]

    # adding attacks to test graph by datetime period and iterating through to change sentiments
    iterEdgeList = []
    self.G.add_nodes_from(nodeList_0[0])
    for node in nodeList_0[0]:
        for others in self.G.nodes():
            if self.G.has_edge(node[0], others):
                sent = self.G.get_edge_data(node, others)
                iterEdgeList.append((node, others, (sent[node, others] * .1) + sent[node, others]))
    self.G.add_weighted_edges_from(iterEdgeList, 'W')
    updateDict = {'0': (self.G.edges(data=True))}

    self.G.add_nodes_from(nodeList_1[0])
    for node in nodeList_1[0]:
        for others in self.G.nodes():
            if self.G.has_edge(node[0], others):
                sent = self.G.get_edge_data(node, others)
                iterEdgeList.append((node, others, (sent[node, others] * .1) + sent[node, others]))
    self.G.add_weighted_edges_from(iterEdgeList, 'W')
    updateDict['1'] = [self.G.edges(data=True)]

    self.G.add_nodes_from(nodeList_2[0])
    for node in nodeList_2[0]:
        for others in self.G.nodes():
            if self.G.has_edge(node[0], others):
                sent = self.G.get_edge_data(node, others)
                iterEdgeList.append((node, others, (sent[node, others] * .1) + sent[node, others]))
    self.G.add_weighted_edges_from(iterEdgeList, 'W')
    updateDict['2'] = [self.G.edges(data=True)]

    self.G.add_nodes_from(nodeList_3[0])
    for node in nodeList_3[0]:
        for others in self.G.nodes():
            if self.G.has_edge(node[0], others):
                sent = self.G.get_edge_data(node, others)
                iterEdgeList.append((node, others, (sent[node, others] * .1) + sent[node, others]))
    self.G.add_weighted_edges_from(iterEdgeList, 'W')
    updateDict['3'] = [self.G.edges(data=True)]

    self.G.add_nodes_from(nodeList_4[0])
    for node in nodeList_4[0]:
        for others in self.G.nodes():
            if self.G.has_edge(node[0], others):
                sent = self.G.get_edge_data(node, others)
                iterEdgeList.append((node, others, (sent[node, others] * .1) + sent[node, others]))
    self.G.add_weighted_edges_from(iterEdgeList, 'W')
    updateDict['4'] = [self.G.edges(data=True)]

    self.G.add_nodes_from(nodeList_5[0])
    for node in nodeList_5[0]:
        for others in self.G.nodes():
            if self.G.has_edge(node[0], others):
                sent = self.G.get_edge_data(node, others)
                iterEdgeList.append((node, others, (sent[node, others] * .1) + sent[node, others]))
    self.G.add_weighted_edges_from(iterEdgeList, 'W')
    updateDict['5'] = [self.G.edges(data=True)]

    self.G.add_nodes_from(nodeList_6[0])
    for node in nodeList_6[0]:
        for others in self.G.nodes():
            if self.G.has_edge(node[0], others):
                sent = self.G.get_edge_data(node, others)
                iterEdgeList.append((node, others, (sent[node, others] * .1) + sent[node, others]))
    self.G.add_weighted_edges_from(iterEdgeList, 'W')
    updateDict['6'] = [self.G.edges(data=True)]

    self.G.add_nodes_from(nodeList_7[0])
    for node in nodeList_7[0]:
        for others in self.G.nodes():
            if self.G.has_edge(node[0], others):
                sent = self.G.get_edge_data(node, others)
                iterEdgeList.append((node, others, (sent[node, others] * .1) + sent[node, others]))
    self.G.add_weighted_edges_from(iterEdgeList, 'W')
    updateDict['7'] = [self.G.edges(data=True)]

    self.G.add_nodes_from(nodeList_8[0])
    for node in nodeList_8[0]:
        for others in self.G.nodes():
            if self.G.has_edge(node[0], others):
                sent = self.G.get_edge_data(node, others)
                iterEdgeList.append((node, others, (sent[node, others] * .1) + sent[node, others]))
    self.G.add_weighted_edges_from(iterEdgeList, 'W')
    updateDict['8'] = [self.G.edges(data=True)]

    self.G.add_nodes_from(nodeList_9[0])
    for node in nodeList_9[0]:
        for others in self.G.nodes():
            if self.G.has_edge(node[0], others):
                sent = self.G.get_edge_data(node, others)
                iterEdgeList.append((node, others, (sent[node, others] * .1) + sent[node, others]))
    self.G.add_weighted_edges_from(iterEdgeList, 'W')
    updateDict['9'] = [self.G.edges(data=True)]

    return

event_update()