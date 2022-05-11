# -*- coding: utf-8 -*-
"""
Created on Wed May  4 12:22:47 2022

@author: Lucian
"""

import roadrunner
import time
from scriptLib import getSBMLFilesFromBiomodels, saveTimeVecs

roadrunner.Config.setValue(roadrunner.Config.LOADSBMLOPTIONS_RECOMPILE, True)
nrepeats = 10
ncores = 24
onlySomeSBML = False

def runMapExperiment(sbmlfiles, nrepeats, ncores):
    timevecs = {}
    timevecs["LLJit"] = {}
    timevecs["MCJit"] = {}
    threadrange = range(ncores-1)
    for nthread in threadrange:
        timevecs["LLJit"][nthread] = []
        timevecs["MCJit"][nthread] = []
    for repeat in range(nrepeats):
        for nthreads in threadrange:
            for (backend, bstr) in [(roadrunner.Config.LLJIT, "LLJit"), (roadrunner.Config.MCJIT, "MCJit")]:
                roadrunner.Config.setValue(roadrunner.Config.LLVM_BACKEND, backend)
                print("Starting run with", nthreads, "threads, repeat", repeat+1, "backend", bstr)
                start = time.perf_counter()
                roadrunner.RoadRunnerMap(sbmlfiles, nthreads+1)
                end = time.perf_counter()
                timevecs[bstr][nthreads].append(end-start)
                print("Total time:", end-start)
    return timevecs, threadrange

if __name__ == '__main__':
    sbmlfiles = getSBMLFilesFromBiomodels(biomds = "../temp-biomodels/final")
    if (onlySomeSBML):
        sbmlfiles = sbmlfiles[:50]
    print("Run RoadRunnerMap experiment:")
    (timevecs, threadrange) = runMapExperiment(sbmlfiles, nrepeats, ncores)
    saveTimeVecs(timevecs, threadrange, "fig1_rrmap.csv")
