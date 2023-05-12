import os
import glob
import time
import pysces
import logging
from pysces.core2.PyscesCore2Interfaces import SbmlToCore
from get_biomodels import get_biomodels

raise ValueError("Give up. Takes too long. Too many errors.")
def get_biomodels_id(filename):
    return os.path.splitext(os.path.split(filename)[1])[0]

biomodels_folder = get_biomodels()
biomodels_files = glob.glob(os.path.join(biomodels_folder, "*.xml"))

pysces_folder = os.path.join(os.path.dirname(__file__), "pysces_models")
if not os.path.isdir(pysces_folder):
    os.makedirs(pysces_folder)

with open("pysces_data", "w") as f:
    for i in range(5):
        start = time.time()
        failures = 0
        for model_file in biomodels_files:
            try:
                pysces_fname = os.path.join(pysces_folder, get_biomodels_id(model_file))
                pysces.interface.convertSBML2PSC(model_file, sbmldir=None, pscfile=pysces_fname, pscdir=None)
                mod = pysces.model(pysces_fname)
                data = mod.doSim(100, 101)
                print(data)
            except Exception:
                failures += 1
                print(f"Model {model_file} failed")

        end = time.time() - start

        print(f"Took {end} seconds")
        print(f"Num failures {failures}")

        print(f"Took {end} seconds", file=f)
        print(f"Num failures {failures}", file=f)








