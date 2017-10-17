from xml.dom import minidom

def getNameMapping(svg_file, idVar, nameVar):
    doc = minidom.parse(svg_file)
    # ret = {path.getAttribute('data-id-1') : path.getAttribute('data-name-engli') for path in doc.getElementsByTagName('path')}
    ret = {path.getAttribute(idVar): path.getAttribute(nameVar) for path in
           doc.getElementsByTagName('path')}
    doc.unlink()
    return ret
