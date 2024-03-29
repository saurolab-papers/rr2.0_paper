# -*- coding: utf-8 -*-
"""
Created on Wed May  4 12:22:47 2022

@author: Lucian
"""

import roadrunner
import time
import concurrent.futures
from scriptLib import getSBMLFilesFromBiomodels, saveTimeVecs

roadrunner.Config.setValue(roadrunner.Config.LOADSBMLOPTIONS_RECOMPILE, True)
nrepeats = 10
ncores = 24
onlySomeSBML = False

badtol = open("badtol.txt", "w")

def loadOnly(sbmlfile):
    roadrunner.Config.setValue(roadrunner.Config.LOADSBMLOPTIONS_RECOMPILE, True)
    roadrunner.RoadRunner(sbmlfile)
    
def loadAndSimulate(sbmlfile):
    roadrunner.Config.setValue(roadrunner.Config.LOADSBMLOPTIONS_RECOMPILE, True)
    try:
        r = roadrunner.RoadRunner(sbmlfile)
        r.simulate(0, 500, 50000)
    except Exception as e:
        print(sbmlfile)
        badtol.write(sbmlfile + "\n")
        print(e)
        raise Exception(sbmlfile + ": " + e.what())

    
def runExperiment(sbmlfiles, nrepeats, ncores, function, allcores):
    timevecs = {}
    timevecs["LLJit"] = {}
    timevecs["MCJit"] = {}
    if allcores:
        threadrange = range(ncores)
    else:
        if ncores < 1:
            threadrange = [0]
        elif ncores < 2:
            threadrange = [0, 1]
        else:
            threadrange = [0, 1, ncores-1]
    for nthread in threadrange:
        timevecs["LLJit"][nthread] = []
        timevecs["MCJit"][nthread] = []
    for repeat in range(nrepeats):
        for nthreads in threadrange:
            for (backend, bstr) in [(roadrunner.Config.LLJIT, "LLJit"), (roadrunner.Config.MCJIT, "MCJit")]:
                roadrunner.Config.setValue(roadrunner.Config.LLVM_BACKEND, backend)
                if nthreads > 0:
                    print("Starting run with", nthreads, "threads, repeat", repeat+1, "backend", bstr)
                    start = time.perf_counter()
                    with concurrent.futures.ProcessPoolExecutor(max_workers=nthreads) as executor:
                        executor.map(function, sbmlfiles)
                else:
                    print("Starting non-parallel run.  Repeat", repeat+1, "backend", bstr)
                    start = time.perf_counter()
                    for sbmlfile in sbmlfiles:
                        function(sbmlfile)
                    
                end = time.perf_counter()
                timevecs[bstr][nthreads].append(end-start)
                print("Total time:", end-start)
    return timevecs, threadrange

if __name__ == '__main__':
    sbmlfiles = getSBMLFilesFromBiomodels(biomds = "../temp-biomodels/final")
    if (onlySomeSBML):
        sbmlfiles = sbmlfiles[:50]
    print("Total number of model files:", len(sbmlfiles))
    print("Just load files:")
    (timevecs, threadrange) = runExperiment(sbmlfiles, nrepeats, ncores, loadOnly, True)
    saveTimeVecs(timevecs, threadrange, "fig1_only_load.csv", ["LLJit", "MCJit"])
    print("Load and simulate files:")
    (timevecs, threadrange) = runExperiment(sbmlfiles, nrepeats, ncores, loadAndSimulate, False)
    saveTimeVecs(timevecs, threadrange, "fig2_load_and_sim.csv", ["LLJit", "MCJit"])
