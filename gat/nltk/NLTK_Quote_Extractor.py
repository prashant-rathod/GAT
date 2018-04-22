from nltk.tokenize import sent_tokenize


def quote_extractor(text_file):
    """
    Returns a list of all quotes and who said them.
    :param text_file: name of text file with article
    """
    with open(text_file) as f:
        content = f.readlines()
    article_string = ""
    for x in content:
        article_string += x.strip('')
    sent_tokens = sent_tokenize(article_string)
    # TODO: sometimes the speaker is vague, eg. "he said", so the function should be able to keep track of pronoun references
    quotes = []
    for token in sent_tokens:
        if "“" in token:
            quotes.append(token)
    return quotes


print(quote_extractor("sample.txt"))
