import argparse
from Beam.generate_OTR import generate_OTR

parser = argparse.ArgumentParser()
parser.add_argument("--doGeneration", help="generate photons", action="store_true")
parser.add_argument("--doPropagation", help="propagate photons to camera", action="store_true")
args = parser.parse_args()

if args.doGeneration:
    print("Generating Photons")
    generate_OTR()

if args.doPropagation:
    print("Propagating photons to camera")
