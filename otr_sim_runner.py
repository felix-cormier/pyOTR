import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--doGeneration", help="generate photons", action="store_true")
parser.add_argument("--doPropagation", help="propagate photons to camera", action="store_true")
args = parser.parse_args()