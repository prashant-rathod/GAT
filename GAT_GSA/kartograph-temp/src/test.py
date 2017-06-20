from kartograph import Kartograph

config = {
    "layers": {
        "mylayer": {
            "src": "us_income/us48.shp",
            "labeling": {
                "key": "NAME_1"
            },
            "attributes": "all"
        }
    },
    "proj": {
        "id": "mercator"
    }
}

K = Kartograph()
K.generate(config, outfile='mymap.svg')
