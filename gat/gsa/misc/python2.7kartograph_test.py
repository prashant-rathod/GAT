#!/usr/bin/python2.7
from kartograph import Kartograph

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-source")
parser.add_argument("-proj")
parser.add_argument("-outfile")
args = parser.parse_args()

print(args)
config = {
            "layers": {
                "mylayer": {
                    "src": args.source, 
                    "attributes": "all"
                }
            },
            "proj": {
                "id": args.proj 
            }
        }

K = Kartograph()
K.generate(config, outfile=args.outfile)
