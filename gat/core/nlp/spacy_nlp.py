################ SpaCy NLP ##########################
# INPUT: (text, language)                           #
# OUTPUT: annotated words                           #
# Function : calls syntaxNet on the text, reformats #
#            output to be usable in other programs  #
#####################################################
import multiprocessing
import spacy
import textacy
from collections import defaultdict
from networkx.readwrite import json_graph
from gat.dao import dao

########### SpaCy Pre-Processing Methods #############

def loadModel(language):
	#Only loads english.
	#Loads SpaCy language model. Separate because computationally expensive.
	return dao.spacy_load_en()

def pipeline(model, texts):
	#Builds an efficient pipeline for tagging, dependency parsing, and NER. Linear time with number of words in text.
	#Also, automatically threads where possible to improve performance further. Batch size can be tweaked further.
	pipe = iter(texts)
	docs = []
	for doc in model.pipe(texts, batch_size = 10000, n_threads = multiprocessing.cpu_count()):
		docs.append(doc)
	return docs

########## Named entity helper methods ###############

def entityVariants(entities):
	#Input: Named entities
	#Output: Sets of variants
	ids = set()
	for ent in entities:
		ids.add(ent.text)
	variants = textacy.keyterms.aggregate_term_variants(ids, acro_defs=None, fuzzy_dedupe=True)
	variants = [v for v in variants if len(v) > 1]
	return variants

def combineVariants(entities, variants):
	# Input: entity variants, an entity-keyed dictionary
	# Output: The dictionary from before with all entity variants combined
	for v in variants:
		var = []
		while len(v) > 0: var.append(v.pop())
		combine = var[1:]
		entities = [e for e in entities if e.text not in combine]
	return entities

def formatEntity(entity):
	#Input: entity
	#Output: better formatted entity
	entity = entity.text.lower().rstrip('-').rstrip('#').rstrip('of')
	entity = entity.strip().replace('\n', ' ').strip("’").replace('\t', ' ')
	return entity

def formatStr(str):
	#Input: entity
	#Output: better formatted entity
	str = str.lower().rstrip('-').rstrip('#').rstrip('of')
	str = str.strip().replace('\n', ' ').strip("’").replace('\t', ' ')
	return str

def subVerbObj(docs):
	#Input: spacy parsed docs
	#Output: (subject, verb, object) tuples. Can be phrases
	#Switched from manual to textacy. Consider switching back if flexibility demands later
	SVO = []
	for doc in docs:
		SVO.append(textacy.extract.subject_verb_object_triples(doc))
	return SVO

####################### Named Entity Functions ###################3

def namedEntities(docs, remove_dup=False):
	#Input: Spacy parsed docs
	#Output: list of relevant named entities. Contains duplicates and variants
	entities = list()
	for doc in docs:
		#Simpler way to extract named entities than namedEntities function
		ent = textacy.extract.named_entities(doc,  exclude_types= "NUMERIC", drop_determiners=True)
		entities += ent
	#Filter entities
	entities = [e for e in entities if len(e) > 1 or (e.label_ not in ['GPE', 'ORG', 'NORP'] and len(e.text) > 4)]
	return entities

def largestForm(entity, entities):
	for ent in entities:
		if entity.text != ent.text and entity.text in ent.text:
			return largestForm(ent, entities)
	return entity

class entityUses():
	def __init__(self, entity):
		self.name = formatEntity(entity)
		self.uses = [entity.sent]
		self.label = entity.label_

	def combine(self, entity2):
		for use in entity2.uses:
			self.uses.append(use)

def improvesUsages(docs):
	entUses = defaultdict()
	entities = namedEntities(docs)
	# Must be done here because all code isn't refactored yet to use entityUses classs
	variants = entityVariants(entities)
	heads = []
	children = []
	#Longest variant is chosen as the one to collapse all others into. Build list of longest variants and list of rest.
	for v in entityVariants(entities):
		var = []
		while (len(v) > 0): var.append(formatStr(v.pop()))
		long = var[0]
		for v in var[1:]:
			if len(v) > len(long): long = v
		var.remove(long)
		heads.append(long)
		children.append([v for v in var])
	#Build entityUses classes
	entities = [entityUses(e) for e in entities]
	#Collapse all entities into their largest found form.
	#Is there a better way? This is simple, but doesn't guarantee best result.
	removals = []
	for e in entities:
		if e.name in heads: head = True
		else: 				head = False
		for elt in removals:
			entities.remove(elt)
		removals = []
		for e2 in entities:
			# If e is head, collapse children. Remove children as you go for efficiency
			if not e == e2:
				if head:
					if e2.name in children:
						children.remove(e2.name)
						e.combine(e2)
						removals.append(e2)

				#Collapse substrings into e
				if e2.name in e.name:
					e.combine(e2)
					removals.append(e2)

	#Now that we have better (more collapsed, less junky) entities, build dict
	for e in entities:
		if not e.label in entUses.keys():
			entUses[e.label] = defaultdict(list)
		entUses[e.label][e.name] = e.uses
	return entUses



def entityUsages(docs):
	#Input: docs
	#Ouput: Nested Dictionary of entities (combined where necessary) with all usages
	#  		dict[label][entity] is key format
	entityUsage = defaultdict()
	entities = namedEntities(docs)
	for e in entities:
		key = largestForm(e, entities)
		if not e.label_ in entityUsage.keys():
			entityUsage[e.label_] = defaultdict(list)
		entityUsage[e.label_][formatEntity(key)].append(e.sent)
	for v in entityVariants(entities):
		var = []
		while (len(v) > 0): var.append(formatStr(v.pop()))
		combine = var[1:]
		for name in combine:
			for key in entityUsage.keys():
				if var[0] in entityUsage[key].keys():
					if name in entityUsage[key].keys():
						entityUsage[key][var[0]] += entityUsage[key].pop(name)
					else:
						for key2 in entityUsage.keys():
							if name in entityUsage[key2].keys(): entityUsage[key][var[0]] += entityUsage[key2].pop(name)
	return entityUsage

def crossEntityUsages(docs, central_type = None):
	#Input: sets of sentences by named entity (dictionary)
	#Output: non-zero set intersections by named entity pairs (nested dictionary)
	entityUsage = improvesUsages(docs)
	multidict = defaultdict()
	#Consider changing this loop if performance is an issue
	#Only takes ~1/3 second on example so fine for now
	#Despite nasty looping, it's actually O(sentences^2)
	if not central_type: type = entityUsage.keys()
	else: type = [central_type]
	# Check if they have concurrent usage, not including themselves, over all other keys
	for label in type:
		for key, sentences in entityUsage[label].items():
			for label2 in entityUsage.keys():
				for key2, compare in entityUsage[label2].items():
					for sent in compare:
						if sent in sentences and key2 != key:
							#Build dictionary entry
							if key not in multidict.keys(): multidict[key] = defaultdict(defaultdict)
							if label2 not in multidict[key].keys(): multidict[key][label2] = defaultdict(list)
							if key2 not in multidict[key][label2].keys(): multidict[key][label2][key2] = [sent]
							else:  multidict[key][label2][key2].append(sent)
	return multidict

#TODO: Write a function to take a custom entity list and search the docs for it

##################### Graph Functions ################################

def entityGraph(docs):
	#Input: spacy parsed docs
	#Output: network of Named entities built by collocation within text. Edges weighted by frequency.
	entities = namedEntities(docs)
	variants = entityVariants(entities)
	ids = []
	ids = [formatEntity(e) for e in entities if formatEntity(e) not in ids]
	for v in variants:
		var = []
		while len(v) > 1: var.append(v.pop())
		for v in var:
			if v in ids: ids.remove(v)
	graph = textacy.network.terms_to_semantic_network(ids)
	return graph


def graphJson(graph):
	serializable = json_graph.node_link_data(graph)
	return serializable
