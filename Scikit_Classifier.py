categories = ['PublicStatement','Appeal','ExpressIntent','ExpressIntenttoCooperate','ExpressIntenttobuildInfrastructure',
'Consult','Engageindiplomaticcooperation','Engageinmaterialcooperation','Provideaid','Yield','Investigate','Demand',
'Disapprove','Reject','Threaten','Protest','Exhibitforceposture','Reducerelations','Coerce','Assault','Fight',
'Useunconventionalmassviolence','Usesocialfollowing','Controlinformation','Buildenergyinfrastructure',
'Buildsocialinfrastructure','Buildpoliticalinfrastructure','Buildmilitaryinfrastructure','Buildinformationinfrastructure',
'Buildeconomicinfrastructure','Gathermineformaterials','Changeprice','Governmentfunds'
]
    
import sklearn
from sklearn import datasets
twenty_train = sklearn.datasets.load_files("./", description=None, categories=categories, load_content=True, shuffle=True, encoding="utf-8", decode_error='strict', random_state=42)
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
text_clf = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('clf', MultinomialNB()), ])
text_clf = text_clf.fit(twenty_train.data, twenty_train.target)
import numpy as np
twenty_test = sklearn.datasets.load_files("./", description=None, categories=categories, load_content=True, shuffle=True, encoding="utf-8", decode_error='strict', random_state=42)
docs_test = twenty_test.data
predicted = text_clf.predict(docs_test)
np.mean(predicted == twenty_test.target)