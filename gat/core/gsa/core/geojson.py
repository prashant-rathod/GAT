import shapefile
from json import dumps

def convert(inputpath):
    # read the shapefile
    # reader = shapefile.Reader("network/street_crimes.shp")
    reader = shapefile.Reader(inputpath)
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    for sr in reader.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", \
                           geometry=geom, properties=atr))

        # write the GeoJSON file

    #geojson = open("../../../../static/mygeodata/pyshp-demo.json", "w")
    geojson = open("static/mygeodata/demo.json", "w")
    geojson.write(dumps({"type": "FeatureCollection", \
                         "features": buffer}, indent=2) + "\n")
    geojson.close()