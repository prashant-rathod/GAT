import rpy2.robjects

rpy2.robjects.r(
    '''
    dyn.load('/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64/server/libjvm.so')
    library(devtools)
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
library(sotu)
library(rJava)
sotu <- data.frame(cbind(sotu_text, sotu_meta), stringsAsFactors=FALSE)
sotu$sotu_text <- as.character(sotu$sotu_text)
sotu <- sotu[1:20,]
sotu_text <- sotu_text[1:20]
sotu_text_data <- prep_text(sotu, textvar="sotu_text", groupvar="president", node_type="groups", remove_stop_words=TRUE, stem=TRUE)
sotu_text_data_nouns <- prep_text_noun_phrases(sotu, "president", "sotu_text", node_type="groups", top_phrases=TRUE)
sotu_text_network <- create_textnet(sotu_text_data, node_type="groups")
sotu_communities <- text_communities(sotu_text_network)
top_words_modularity_classes <- interpret(sotu_text_network, sotu_text_data)
text_centrality <- centrality(sotu_text_network)
visualize(sotu_text_network, .50, label_degree_cut=3)
visualize_d3js(sotu_text_network, .50)
    '''
)