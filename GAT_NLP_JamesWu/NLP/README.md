# NLP
Natural Language Processing Container for the Geospatial Analysis Toolkit (GAT)

Laboratory for Unconventional Conflict Analysis and Simulation (LUCAS) associated with Duke University

Functions:
scraper.py uses the newspaper package and news urls to scape raw text and track metadata
language_detector.py uses nltk stopwords to identify the language of scraped/parsed text
parser.py uses the nltk and sklearn packages to parse texts with part of speech (POS) tagging, noun phrase chunking, and name entity recognition (NER). Also includes classifiers for gender and sentiment analysis.

The NLP container provides data for the geospatial and social network analysis containers.
