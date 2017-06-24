from kartograph import Kartograph

config = {
            "layers": {
                "mylayer": {
                    "src": "/home/nikita/Projects/pysaltest/src/TM_WORLD_BORDERS-0.3.shp",
                    "attributes": "all"
                }
            },
            "proj": {
                "id": "mercator" 
            }
        }

K = Kartograph()
K.generate(config, outfile='/home/nikita/Projects/GAT/mymap.svg')
