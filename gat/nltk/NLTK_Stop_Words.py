from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize.moses import MosesDetokenizer


def stop_word_filter(text_file):
    """
    Returns a string that's a shortened version of the input without any stop words
    :param text_file: name of text file with article
    :type text_file: string
    """
    with open(text_file) as f:
        content = f.readlines()
    article_string = ""
    for x in content:
        article_string += x.strip('')
    stop_words = set(stopwords.words('english'))  # TODO: enable automatic language change
    word_tokens = word_tokenize(article_string)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    detokenizer = MosesDetokenizer()
    filtered_article = detokenizer.detokenize(filtered_sentence, return_str=True)
    return filtered_article


print(stop_word_filter("sample.txt"))
