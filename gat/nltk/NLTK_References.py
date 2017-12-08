

def reference_extractor(text_file):
    """
    Returns a list of all references used in the article
    :param text_file: name of text file with article
    """
    with open(text_file) as f:
        content = f.readlines()
    content = [x.strip('\n') for x in content]
    is_bibliography = False
    references = []
    buzzwords = ["bibliography",  "citations", "references"]
    for line in content:
        if is_bibliography:
            references.append(line)
        if line.lower() in buzzwords:
            is_bibliography = True
    if len(references) == 0:
        return "No references found."
    return references


print(reference_extractor("sample.txt"))
