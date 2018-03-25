import rpy2.robjects as robjects
import pandas as pd
from rpy2.robjects import pandas2ri
import warnings
from rpy2.rinterface import RRuntimeWarning
import ntpath


#Assume they pass in a csv, first column is text, the group metadata is in second column

def textnetAllText(csvPath, textColumnName = '', groupVarColumnName=''):
    warnings.filterwarnings("ignore", category=RRuntimeWarning)
    pandas2ri.activate()
    head, tail = ntpath.split(csvPath)
    filename = tail or ntpath.basename(head)
    filename=filename[0:filename.index(".")]
    rstring = '''
        function(dataSet, filename){
            sink("/dev/null")
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
            dataSet[,1] <- as.character(dataSet[,1])
            p <- names(dataSet)
            dataSet_text_data <- prep_text(dataSet, textvar=p[1], groupvar=p[2], node_type="groups", remove_stop_words=TRUE, stem=TRUE)
            dataSet_text_data_nouns <- prep_text_noun_phrases(dataSet, p[2], p[1], node_type="groups", top_phrases=TRUE)
            dataSet_text_network <- create_textnet(dataSet_text_data, node_type="groups")
            dataSet_communities <- text_communities(dataSet_text_network)
            top_words_modularity_classes <- interpret(dataSet_text_network, dataSet_text_data)
            text_centrality <- centrality(dataSet_text_network)
            visualize(dataSet_text_network, .50, label_degree_cut=3)
            visualize_d3js(dataSet_text_network, .50)
            vis <- visualize_d3js(dataSet_text_network, 
                                  prune_cut=.50,
                                  height=1000,
                                  width=1400,
                                  bound=FALSE,
                                  zoom=TRUE,
                                  charge=-30)
            saveWidget(vis, paste(filename, "_", "textnet.html", sep=""))
            }
    '''
    rfunc = robjects.r(rstring)
    robjects.r['options'](warn=-1)
    dataList = pd.read_csv(csvPath)
    if textColumnName!='' and groupVarColumnName!='':
        dataList = dataList[[textColumnName, groupVarColumnName]]
    rfunc(dataList, filename)

textnetAllText("/home/cheesecake/Downloads/State-of-the-Union-Addresses.csv", 'Text', 'President')