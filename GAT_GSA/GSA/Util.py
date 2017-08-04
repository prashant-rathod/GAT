from xml.dom import minidom

def getNames(svg_file):
    doc = minidom.parse(svg_file)
    path_strings = [path.getAttribute('data-name-engli') for path in doc.getElementsByTagName('path')]
    print(path_strings)
    doc.unlink()
    return path_strings
