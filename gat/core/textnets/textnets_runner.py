import rpy2.robjects as robjects
import pandas as pd
from rpy2.robjects import pandas2ri

#Assume they pass in a csv, first column is text, the group metadata is in second column

pandas2ri.activate()
def textnetAllText(csvPath, textColumnName = '', groupVarColumnName=''):
    rstring = '''
        function(sotu){
            dyn.load('/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64/server/libjvm.so')
            library(textnets)
            library(dplyr)
            library(tidytext)
            library(stringr)
            library(SnowballC)
            library(reshape2)
            library(phrasemachine)
            library(igraph)
            library(ggraph)
            library(networkD3)
            library(htmlwidgets)
            library(rJava)
            sotu[,1] <- as.character(sotu[,1])
            p <- names(sotu)
            sotu_text_data <- prep_text(sotu, textvar=p[1], groupvar=p[2], node_type="groups", remove_stop_words=TRUE, stem=TRUE)
            sotu_text_data_nouns <- prep_text_noun_phrases(sotu, p[2], p[1], node_type="groups", top_phrases=TRUE)
            sotu_text_network <- create_textnet(sotu_text_data, node_type="groups")
            sotu_communities <- text_communities(sotu_text_network)
            top_words_modularity_classes <- interpret(sotu_text_network, sotu_text_data)
            text_centrality <- centrality(sotu_text_network)
            visualize(sotu_text_network, .50, label_degree_cut=3)
            visualize_d3js(sotu_text_network, .50)
            vis <- visualize_d3js(sotu_text_network, 
                                  prune_cut=.50,
                                  height=1000,
                                  width=1400,
                                  bound=FALSE,
                                  zoom=TRUE,
                                  charge=-30)
            saveWidget(vis, "sotu_textnet.html")
            }
    '''
    rfunc = robjects.r(rstring)
    dataList = pd.read_csv(csvPath)
    if textColumnName!='' and groupVarColumnName!='':
        dataList = dataList[[textColumnName, groupVarColumnName]]
    rfunc(dataList)

#textnetAllText("/home/cheesecake/Downloads/State-of-the-Union-Addresses.csv", 'Text', 'Age')