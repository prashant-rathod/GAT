####################################
######## Stopwords Analysis ########
####################################
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords

"""
Calculates the unique stopword frequency of inputted text and returns a language/# stopwords dictionary
INPUT:
	text: raw text input (string)
OUTPUT:
	language_frequencies: dictionary with languages and unique stopwords in text {language: # stop words}
"""
def calculate_stopword_frequencies(text):
	language_frequencies = {}
	tokens = wordpunct_tokenize(text)
	words = [word.lower() for word in tokens]
	for language in stopwords.fileids():
		unique_stopwords = set(stopwords.words(language))
		unique_words = set(words)
		common_elements = unique_words.intersection(unique_stopwords)
		language_frequencies[language] = len(common_elements) 
	return language_frequencies

"""
Return the most likely language from the language frequencies dictionary
INPUT:
	text: raw text input (string)
OUTPUT:
	language_guess: the language with the highest unique stopword frequency 
	(i.e. the detected language for the text)
"""
def stopword_detect_language(text):
	freqs = calculate_stopword_frequencies(text)
	language_guess = max(freqs, key=freqs.get)
	return language_guess
	
if __name__=='__main__':
	text = '''A la tribune le ton était donc revanchard. 
	Au fil des discours, les noms des personnalités honnis ont été copieusement sifflés: 
	François Bayrou, bien sûr, Christiane Taubira, mais aussi Nicolas Dupont-Aignan, 
	l'ancien UMP qui a rallié Marine Le Pen pour le second tour de la présidentielle. 
	Mais personne n'a osé lancé les noms d'Edouard Philippe, de Bruno Le Maire ou de
	Gérald Darmanin qui ont accepté de gouverner avec le nouveau président de la République.'''
	text2 = '''Resmi ziyaret kapsamında Riyad'da temaslarına devam eden Trump ile  Selman arasında 
	Yemame Sarayı'nda ikili görüşme ve heyetlerarası görüşme  gerçekleştirildi.
	Görüşmelerde ABD ile stratejik ve köklü ilişkilerinin  çeşitlendirilerek tüm alanlara
	yayılması ve geliştirilmesi, bölgesel konular,  Ortadoğu'daki ve uluslararası gelişmelerin yanı sıra 
	bölgede barış ve istikrarın  artırılması için atılması gereken adımlar ele alındı.
	Görüşme sonrasında Kral Selman bin Abdulaziz ile ABD Başkanı Donald  Trump arasında 
	"ortak stratejik vizyon anlaşması" imzalandı.'''
	language = stopword_detect_language(text)
	print (language) #french
	language2 = stopword_detect_language(text2)
	print (language2) #turkey