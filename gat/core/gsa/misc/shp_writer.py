from osgeo import ogr
from xml.dom import minidom
#RUN WITH PYTHON 2.7
'''
TODO: 
read csv, obtain location, 
match to location in shp file, 
add a new column to shapeiles (starter code below), 
write values for all locations given in csv <- this is the only part we don't know how to do 

location_names contains the names of all the locations inside of the shapefile.
'''

def add_data(field_name, data_values, shp_path, svg_path, idVar, nameVar):
    driver = ogr.GetDriverByName('ESRI Shapefile')
    dataSource = driver.Open(shp_path, 1) #1 is read/write
    print(dataSource)


    doc = minidom.parse(svg_path)
    location_names = [path.getAttribute(nameVar) for path in doc.getElementsByTagName('path')]
    doc.unlink()

    print(location_names)
    
    #define floating point field named DistFld and 16-character string field named Name:
    fldDef = ogr.FieldDefn('DistFld', ogr.OFTReal)
    fldDef2 = ogr.FieldDefn(field_name, ogr.OFTString)
    fldDef2.SetWidth(16) #16 char string width

    #get layer and add the 2 fields:
    layer = dataSource.GetLayer()
    layer.CreateField(fldDef)
    layer.CreateField(fldDef2)

    # print(dir(layer))

add_data("TEST", None, 'static/sample/gsa/IRQ_adm1.shp', 'out/gsa/mymap.svg', "data-id-1", "data-name-1")

