from basico import *
import os
import glob
import time
import sbmltoodepy
import sys
from importlib import import_module
import multiprocessing
import numpy as np
from roadrunner.roadrunner import RoadRunner, Config, RoadRunnerMap
from get_biomodels import get_biomodels

# Config.setValue(Config.LLVM_BACKEND, Config.LLJIT)
Config.setValue(Config.LLVM_BACKEND, Config.MCJIT)

# we have to disable to model caching so that repeats are independent
Config.setValue(Config.LOADSBMLOPTIONS_RECOMPILE, True)

if __name__ == "__main__":
    biomodels_folder = get_biomodels()
    biomodels_files = glob.glob(os.path.join(biomodels_folder, "*.xml"))

    times = []
    for i in range(5):
        start = time.time()
        rrm = RoadRunnerMap(biomodels_files, 12)
        for k, v in rrm.items():
            try:
                v.simulate(0, 100, 101)
            except Exception:
                continue

        end = time.time() - start
        del rrm
        times.append(end)
        print("Took: ", end, "seconds")
    print(f"average: {np.average(times)}")
    print(f"stdev: {np.std(times)}")

"""
All errors are ignored
LLJit with RoadRunnerMap. 12 Threads. 
    Took:  22.109879732131958 seconds
    Took:  25.4362735748291 seconds
    Took:  25.90856647491455 seconds
    Took:  24.670109033584595 seconds
    Took:  25.258594512939453 seconds
        average: 24.676684665679932
        stdev: 1.343254106934861

MCJit with RoadRunnerMap. 12 Threads. 
    Took:  30.22196316719055 seconds
    Took:  34.92194080352783 seconds
    Took:  35.245986461639404 seconds
    Took:  40.70267629623413 seconds
    Took:  32.46453833580017 seconds
        average: 34.71142101287842
        stdev: 3.5051086198394623

    
"""