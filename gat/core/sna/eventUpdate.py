import decimal
import random
import tempfile
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import xlrd
from networkx.algorithms import bipartite as bi
from networkx.algorithms import centrality
import pandas as pd

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

#print(b)
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

df = pd.read_excel("attacks.xlsx")
bombData = df.to_dict(orient='index')
print(bombData)
y = len(bombData)

jan_13 = [bombData[x] for x in bombData if int(bombData[x]['Date']) < 20130200]
nodeList_jan_13 = [(jan_13[x]['Source'], jan_13[x]['Target'], jan_13[x]['Date']) for x in range(len(jan_13))]

feb_13 = [bombData[x] for x in bombData if 20130200 <= int(bombData[x]['Date']) < 20130300]
nodeList_feb_13 = [(feb_13[x]['Source'], feb_13[x]['Target'], feb_13[x]['Date']) for x in range(len(feb_13))]

mar_13 = [bombData[x] for x in bombData if 20130300 <= int(bombData[x]['Date']) < 20130400]
nodeList_mar_13 = [(mar_13[x]['Source'], mar_13[x]['Target'], mar_13[x]['Date']) for x in range(len(mar_13))]

apr_13 = [bombData[x] for x in bombData if 20130400 <= int(bombData[x]['Date']) < 20130500]
nodeList_apr_13 = [(apr_13[x]['Source'], apr_13[x]['Target'], apr_13[x]['Date']) for x in range(len(apr_13))]

may_13 = [bombData[x] for x in bombData if 20130500 <= int(bombData[x]['Date']) < 20130600]
nodeList_may_13 = [(may_13[x]['Source'], may_13[x]['Target'], may_13[x]['Date']) for x in range(len(may_13))]

jun_13 = [bombData[x] for x in bombData if 20130600 <= int(bombData[x]['Date']) < 20130700]
nodeList_jun_13 = [(jun_13[x]['Source'], jun_13[x]['Target'], jun_13[x]['Date']) for x in range(len(jun_13))]

jul_13 = [bombData[x] for x in bombData if 20130700 <= int(bombData[x]['Date']) < 20130800]
nodeList_jul_13 = [(jul_13[x]['Source'], jul_13[x]['Target'], jul_13[x]['Date']) for x in range(len(jul_13))]

aug_13 = [bombData[x] for x in bombData if 20130800 <= int(bombData[x]['Date']) < 20130900]
nodeList_aug_13 = [(aug_13[x]['Source'], aug_13[x]['Target'], aug_13[x]['Date']) for x in range(len(aug_13))]

sep_13 = [bombData[x] for x in bombData if 20130900 <= int(bombData[x]['Date']) < 20131000]
nodeList_sep_13 = [(sep_13[x]['Source'], sep_13[x]['Target'], sep_13[x]['Date']) for x in range(len(sep_13))]

oct_13 = [bombData[x] for x in bombData if 20131000 <= int(bombData[x]['Date']) < 20131100]
nodeList_oct_13 = [(oct_13[x]['Source'], oct_13[x]['Target'], oct_13[x]['Date']) for x in range(len(oct_13))]

nov_13 = [bombData[x] for x in bombData if 20131100 <= int(bombData[x]['Date']) < 20131200]
nodeList_nov_13 = [(nov_13[x]['Source'], nov_13[x]['Target'], nov_13[x]['Date']) for x in range(len(nov_13))]

dec_13 = [bombData[x] for x in bombData if 20131200 <= int(bombData[x]['Date']) < 20140100]
nodeList_dec_13 = [(dec_13[x]['Source'], dec_13[x]['Target'], dec_13[x]['Date']) for x in range(len(dec_13))]

jan_14 = [bombData[x] for x in bombData if 20140100 <= int(bombData[x]['Date']) < 20140200]
nodeList_jan_14 = [(jan_14[x]['Source'], jan_14[x]['Target'], jan_14[x]['Date']) for x in range(len(jan_14))]

feb_14 = [bombData[x] for x in bombData if 20140200 <= int(bombData[x]['Date']) < 20140300]
nodeList_feb_14 = [(feb_14[x]['Source'], feb_14[x]['Target'], feb_14[x]['Date']) for x in range(len(feb_14))]

mar_14 = [bombData[x] for x in bombData if 20140300 <= int(bombData[x]['Date']) < 20140400]
nodeList_mar_14 = [(mar_14[x]['Source'], mar_14[x]['Target'], mar_14[x]['Date']) for x in range(len(mar_14))]

apr_14 = [bombData[x] for x in bombData if 20140400 <= int(bombData[x]['Date']) < 20140500]
nodeList_apr_14 = [(apr_14[x]['Source'], apr_14[x]['Target'], apr_14[x]['Date']) for x in range(len(apr_14))]

may_14 = [bombData[x] for x in bombData if 20140500 <= int(bombData[x]['Date']) < 20140600]
nodeList_may_14 = [(may_14[x]['Source'], may_14[x]['Target'], may_14[x]['Date']) for x in range(len(may_14))]

jun_14 = [bombData[x] for x in bombData if 20140600 <= int(bombData[x]['Date']) < 20140700]
nodeList_jun_14 = [(jun_14[x]['Source'], jun_14[x]['Target'], jun_14[x]['Date']) for x in range(len(jun_14))]

jul_14 = [bombData[x] for x in bombData if 20140700 <= int(bombData[x]['Date']) < 20140800]
nodeList_jul_14 = [(jul_14[x]['Source'], jul_14[x]['Target'], jul_14[x]['Date']) for x in range(len(jul_14))]

aug_14 = [bombData[x] for x in bombData if 20140800 <= int(bombData[x]['Date']) < 20140900]
nodeList_aug_14 = [(aug_14[x]['Source'], aug_14[x]['Target'], aug_14[x]['Date']) for x in range(len(aug_14))]

sep_14 = [bombData[x] for x in bombData if 20140900 <= int(bombData[x]['Date']) < 20141000]
nodeList_sep_14 = [(sep_14[x]['Source'], sep_14[x]['Target'], sep_14[x]['Date']) for x in range(len(sep_14))]

oct_14 = [bombData[x] for x in bombData if 20141000 <= int(bombData[x]['Date']) < 20141100]
nodeList_oct_14 = [(oct_14[x]['Source'], oct_14[x]['Target'], oct_14[x]['Date']) for x in range(len(oct_14))]

nov_14 = [bombData[x] for x in bombData if 20141100 <= int(bombData[x]['Date']) < 20141200]
nodeList_nov_14 = [(nov_14[x]['Source'], nov_14[x]['Target'], nov_14[x]['Date']) for x in range(len(nov_14))]

dec_14 = [bombData[x] for x in bombData if 20141200 <= int(bombData[x]['Date']) < 20150100]
nodeList_dec_14 = [(dec_14[x]['Source'], dec_14[x]['Target'], dec_14[x]['Date']) for x in range(len(dec_14))]

jan_15 = [bombData[x] for x in bombData if 20150100 <= int(bombData[x]['Date']) < 20150200]
nodeList_jan_15 = [(jan_15[x]['Source'], jan_15[x]['Target'], jan_15[x]['Date']) for x in range(len(jan_15))]

feb_15 = [bombData[x] for x in bombData if 20150200 <= int(bombData[x]['Date']) < 20150300]
nodeList_feb_15 = [(feb_15[x]['Source'], feb_15[x]['Target'], feb_15[x]['Date']) for x in range(len(feb_15))]

mar_15 = [bombData[x] for x in bombData if 20150300 <= int(bombData[x]['Date']) < 20150400]
nodeList_mar_15 = [(mar_15[x]['Source'], mar_15[x]['Target'], mar_15[x]['Date']) for x in range(len(mar_15))]

apr_15 = [bombData[x] for x in bombData if 20150400 <= int(bombData[x]['Date']) < 20150500]
nodeList_apr_15 = [(apr_15[x]['Source'], apr_15[x]['Target'], apr_15[x]['Date']) for x in range(len(apr_15))]

may_15 = [bombData[x] for x in bombData if 20150500 <= int(bombData[x]['Date']) < 20150600]
nodeList_may_15 = [(may_15[x]['Source'], may_15[x]['Target'], may_15[x]['Date']) for x in range(len(may_15))]

jun_15 = [bombData[x] for x in bombData if 20150600 <= int(bombData[x]['Date']) < 20150700]
nodeList_jun_15 = [(jun_15[x]['Source'], jun_15[x]['Target'], jun_15[x]['Date']) for x in range(len(jun_15))]

jul_15 = [bombData[x] for x in bombData if 20150700 <= int(bombData[x]['Date']) < 20150800]
nodeList_jul_15 = [(jul_15[x]['Source'], jul_15[x]['Target'], jul_15[x]['Date']) for x in range(len(jul_15))]

aug_15 = [bombData[x] for x in bombData if 20150800 <= int(bombData[x]['Date']) < 20150900]
nodeList_aug_15 = [(aug_15[x]['Source'], aug_15[x]['Target'], aug_15[x]['Date']) for x in range(len(aug_15))]

sep_15 = [bombData[x] for x in bombData if 20150900 <= int(bombData[x]['Date']) < 20151000]
nodeList_sep_15 = [(sep_15[x]['Source'], sep_15[x]['Target'], sep_15[x]['Date']) for x in range(len(sep_15))]

oct_15 = [bombData[x] for x in bombData if 20151000 <= int(bombData[x]['Date']) < 20151100]
nodeList_oct_15 = [(oct_15[x]['Source'], oct_15[x]['Target'], oct_15[x]['Date']) for x in range(len(oct_15))]

nov_15 = [bombData[x] for x in bombData if 20151100 <= int(bombData[x]['Date']) < 20151200]
nodeList_nov_15 = [(nov_15[x]['Source'], nov_15[x]['Target'], nov_15[x]['Date']) for x in range(len(nov_15))]

dec_15 = [bombData[x] for x in bombData if 20151200 <= int(bombData[x]['Date']) < 20160100]
nodeList_dec_15 = [(dec_15[x]['Source'], dec_15[x]['Target'], dec_15[x]['Date']) for x in range(len(dec_15))]

jan_16 = [bombData[x] for x in bombData if 20160100 <= int(bombData[x]['Date']) < 20160200]
nodeList_jan_16 = [(jan_16[x]['Source'], jan_16[x]['Target'], jan_16[x]['Date']) for x in range(len(jan_16))]

feb_16 = [bombData[x] for x in bombData if 20160200 <= int(bombData[x]['Date']) < 20160300]
nodeList_feb_16 = [(feb_16[x]['Source'], feb_16[x]['Target'], feb_16[x]['Date']) for x in range(len(feb_16))]

mar_16 = [bombData[x] for x in bombData if 20160300 <= int(bombData[x]['Date']) < 20160400]
nodeList_mar_16 = [(mar_16[x]['Source'], mar_16[x]['Target'], mar_16[x]['Date']) for x in range(len(mar_16))]

apr_16 = [bombData[x] for x in bombData if 20160400 <= int(bombData[x]['Date']) < 20160500]
nodeList_apr_16 = [(apr_16[x]['Source'], apr_16[x]['Target'], apr_16[x]['Date']) for x in range(len(apr_16))]

may_16 = [bombData[x] for x in bombData if 20160500 <= int(bombData[x]['Date']) < 20160600]
nodeList_may_16 = [(may_16[x]['Source'], may_16[x]['Target'], may_16[x]['Date']) for x in range(len(may_16))]

jun_16 = [bombData[x] for x in bombData if 20160600 <= int(bombData[x]['Date']) < 20160700]
nodeList_jun_16 = [(jun_16[x]['Source'], jun_16[x]['Target'], jun_16[x]['Date']) for x in range(len(jun_16))]

jul_16 = [bombData[x] for x in bombData if 20160700 <= int(bombData[x]['Date']) < 20160800]
nodeList_jul_16 = [(jul_16[x]['Source'], jul_16[x]['Target'], jul_16[x]['Date']) for x in range(len(jul_16))]

aug_16 = [bombData[x] for x in bombData if 20160800 <= int(bombData[x]['Date']) < 20160900]
nodeList_aug_16 = [(aug_16[x]['Source'], aug_16[x]['Target'], aug_16[x]['Date']) for x in range(len(aug_16))]

sep_16 = [bombData[x] for x in bombData if 20160900 <= int(bombData[x]['Date']) < 20161000]
nodeList_sep_16 = [(sep_16[x]['Source'], sep_16[x]['Target'], sep_16[x]['Date']) for x in range(len(sep_16))]

oct_16 = [bombData[x] for x in bombData if 20161000 <= int(bombData[x]['Date']) < 20161100]
nodeList_oct_16 = [(oct_16[x]['Source'], oct_16[x]['Target'], oct_16[x]['Date']) for x in range(len(oct_16))]

nov_16 = [bombData[x] for x in bombData if 20161100 <= int(bombData[x]['Date']) < 20161200]
nodeList_nov_16 = [(nov_16[x]['Source'], nov_16[x]['Target'], nov_16[x]['Date']) for x in range(len(nov_16))]

dec_16 = [bombData[x] for x in bombData if 20161200 <= int(bombData[x]['Date']) < 20170100]
nodeList_dec_16 = [(dec_16[x]['Source'], dec_16[x]['Target'], dec_16[x]['Date']) for x in range(len(dec_16))]