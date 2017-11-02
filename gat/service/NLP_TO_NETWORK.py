#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 15:32:16 2017

@author: ruobingwang
"""
import pandas as pd
import networkx as nx
import itertools
import matplotlib

# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as colorlib
import matplotlib.cm as cmx
import numpy as np
from gat.service import file_io
from gat.service.SVO_SENT_MODULE_spacy import SVOSENT




def txt_to_data(txt_name):
    svo_sent = SVOSENT()
    with open(txt_name, 'r') as myfile:
        article = myfile.read().replace('\n', '')
    result = svo_sent.svo_senti_from_article(article)[['Subjects', 'Objects', 'Predicates', 'compound']]
    subjects = result['Subjects']
    objects = result['Objects']
    sentiment = result['compound']
    verbs = result['Predicates'].apply(lambda x: ','.join(x))
    all_combination = []
    for i in range(len(result)):
        if len(subjects[i]) != 0 and len(objects[i]) != 0 and len(verbs[i]) != 0:
            combine = list(itertools.product(subjects[i], objects[i]))
            #            for i in range(len(combine)):
            #                combine[i]=sorted(combine[i])
            all_combination.append(combine)
    dflist = []
    for i in range(len(all_combination)):
        df = pd.DataFrame(all_combination[i], columns=['name1', 'name2'])
        df['sentiment'] = sentiment[i]
        df['verbs'] = verbs[i]
        dflist.append(df)
    final = pd.concat(dflist)

    def concat(x):
        return ','.join(set(','.join(x).split(',')))

    final = final.groupby(['name1', 'name2']).agg({'sentiment': 'mean',
                                                   'verbs': concat
                                                   })
    # final=final.reset_index()  # for tony's seperate sheet
    final['edges'] = final.index
    final.index = range(len(final))
    return final


def relationship_mining(txt_name):
    data = txt_to_data(txt_name)
    G = nx.DiGraph()
    for i in range(len(data)):
        G.add_edge(*data['edges'][i], verbs=data['verbs'][i])
    plt.figure(figsize=(40, 40))
    pos = nx.spring_layout(G)
    nx.draw(G, with_labels=True, pos=pos, node_size=500, font_size=24)
    nx.draw_networkx_edge_labels(G, pos=pos,
                                 edge_labels=nx.get_edge_attributes(G, 'verbs'), font_size=18, font_color='b')
    filename = 'new_nlp_relationship_example'
    filename = 'out/nlp/' + filename + '.png'
    plt.savefig(filename)
    return filename


def sentiment_mining(txt_name):
    data = txt_to_data(txt_name)

    G = nx.DiGraph()
    G.add_edges_from(data['edges'])
    pos = nx.spring_layout(G)
    colors = data['sentiment']
    cmap = plt.cm.jet
    vmin = -1
    vmax = 1
    plt.figure(figsize=(50, 40))
    nx.draw(G, pos=pos, node_size=500, font_size=24, edge_color=colors, width=4, edge_cmap=cmap, with_labels=True,
            vmin=vmin, vmax=vmax, arrows=False)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=colorlib.Normalize(vmin=-1, vmax=1))
    sm._A = []
    cb = plt.colorbar(sm, shrink=0.4)
    cb.set_label(label='sentiment', weight='bold', size=24)
    cb.ax.tick_params(labelsize=24)
    filename = 'new_nlp_sentiment_example'
    filename = 'out/nlp/' + filename + '.png'
    plt.savefig(filename)
    return filename
