from osgeo import ogr
from xml.dom import minidom
import csv

#RUN WITH PYTHON 2.7
'''
TODO: 
read csv, obtain location, 
match to location in shp file, 
add a new column to shapeiles (starter code below), 
write values for all locations given in csv <- this is the only part we don't know how to do 

location_names contains the names of all the locations inside of the shapefile.
'''

def add_data(shp_path, csv_path, shp_name):
    driver = ogr.GetDriverByName('ESRI Shapefile')
    dataSource = driver.Open(shp_path, 1) #1 is read/write

    # read csv file, first parse all the info into a dict
    field_names = []
    csv_dict = {}
    with open(csv_path, 'rU') as f:
        reader = csv.reader(f)
        # put all the data into a dict
        first_line = True
        for row in reader:
            if first_line:
                for items in row:
                    field_names.append(items)
                first_line = False;
            else:
                # create a dict for each name
                csv_dict[row[0]] = {}
                for i in range(len(field_names)):
                    csv_dict[row[0]][field_names[i]] = row[i]

    print(csv_dict)

    # read svg file
    # doc = minidom.parse(svg_path)
    # location_names = [path.getAttribute(svg_name) for path in doc.getElementsByTagName('path')]
    # doc.unlink()s
    # print(location_names)

    # read shp file
    layer = dataSource.GetLayer()
    # define floating point field named DistFld and 16-character string field named Name:

    # print layer.GetFeatureCount() # number of records
    created = True
    for feature in layer:
        name = feature.GetField(shp_name)

        for field in field_names[1:]:
            # create fields
            if not created:
                fldDef = ogr.FieldDefn(field, ogr.OFTInteger)
                layer.CreateField(fldDef)

            if csv_dict[name][field] != '':
                layer.SetFeature(feature)
                feature.SetField(field, int(csv_dict[name][field]))

        created = True

    dataSource.Destroy()

add_data(None, 'gsa_test/IRQ_adm1.shp', 'gsa_test/IRQcasualties.csv', "NAME_1", "data-name-1")

