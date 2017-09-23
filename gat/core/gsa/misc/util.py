from xml.dom import minidom

def getNameMapping(svg_file, idVar, nameVar):
    doc = minidom.parse(svg_file)
    ret = {path.getAttribute(idVar): path.getAttribute(nameVar) for path in
           doc.getElementsByTagName('path')}
    doc.unlink()
    return ret
