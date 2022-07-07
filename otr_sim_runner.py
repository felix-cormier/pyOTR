import argparse
from Beam.generate_OTR import generate_OTR
from OTR.pyOTR import pyOTR

parser = argparse.ArgumentParser()
parser.add_argument("--doGeneration", help="generate photons", action="store_true")
parser.add_argument("--doPropagation", help="propagate photons to camera", action="store_true")
args = parser.parse_args()

if args.doGeneration and args.doPropagation:
    print("Generating and Propagating Photons")
    X,V, generator_options = generate_OTR()
    pyOTR(X, V, generator_options)

elif args.doGeneration:
    print("Generating Photons")
    generate_OTR()

elif args.doPropagation:
    print("Propagating photons to camera")
