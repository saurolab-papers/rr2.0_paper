# -*- coding: utf-8 -*-
"""
Created on Wed May  4 12:22:47 2022

@author: Lucian
"""

# import tellurium as te
import roadrunner
import time
import numpy as np
from scriptLib import getSBMLFilesFromBiomodels

nrepeats= 5


def writeTimesFor(sbmlfile, timedata, times):
    averageLL = np.average(timedata["LLJit"][sbmlfile])
    averageMC = np.average(timedata["MCJit"][sbmlfile])
    stdLL = np.std(timedata["LLJit"][sbmlfile])
    stdMC = np.std(timedata["MCJit"][sbmlfile])
    ratio = averageMC/averageLL
    times.write(", ")
    times.write(str(averageLL))
    times.write(", ")
    times.write(str(stdLL))
    times.write(", ")
    times.write(str(averageMC))
    times.write(", ")
    times.write(str(stdMC))
    times.write(", ")
    times.write(str(ratio))

def writeFullCSV(filename):
    times = open(filename, "w")
    times.write("File")
    times.write(", ")
    times.write("LLJit load")
    times.write(", ")
    times.write("err LLJit load")
    times.write(", ")
    times.write("MCJit load")
    times.write(", ")
    times.write("err MCJit load")
    times.write(", ")
    times.write("MC/LL load")
    times.write(", ")
    times.write("LLJit sim")
    times.write(", ")
    times.write("err LLJit sim")
    times.write(", ")
    times.write("MCJit sim")
    times.write(", ")
    times.write("err MCJit sim")
    times.write(", ")
    times.write("MC/LL sim")
    times.write("\n")
    for sbmlfile in loadtime[bstr]:
        times.write(sbmlfile)
        
        writeTimesFor(sbmlfile, loadtime, times)
        writeTimesFor(sbmlfile, simtime, times)

        times.write("\n")
    times.close()



sbmlfiles = getSBMLFilesFromBiomodels()
sbmlfiles = sbmlfiles[:10]

loadtime = {}
loadtime["LLJit"] = {}
loadtime["MCJit"] = {}
for sbmlfile in sbmlfiles:
    loadtime["LLJit"][sbmlfile] = []
    loadtime["MCJit"][sbmlfile] = []

simtime = {}
simtime["LLJit"] = {}
simtime["MCJit"] = {}


#Run everything, looping over the backend last:
for sbmlfile in sbmlfiles:
    simtime["LLJit"][sbmlfile] = []
    simtime["MCJit"][sbmlfile] = []


for n in range(nrepeats):
    print("Repeat", n)
    for sbmlfile in sbmlfiles:
        # print(sbmlfile)
        for (backend, bstr) in [(roadrunner.Config.LLJIT, "LLJit"), (roadrunner.Config.MCJIT, "MCJit")]:
            roadrunner.Config.setValue(roadrunner.Config.LLVM_BACKEND, backend)
            try:
                pre = time.perf_counter()
                r = roadrunner.RoadRunner(sbmlfile)
                post_load = time.perf_counter()
                r.simulate(0, 100, 1000)
                post_sim = time.perf_counter()
                loadtime[bstr][sbmlfile].append(post_load - pre)
                simtime[bstr][sbmlfile].append(post_sim - post_load)
            except Exception as e:
                print(sbmlfile)
                print(e)

writeFullCSV("individual_times_backend_changing.csv") 

#Run everything, looping over the backend first:
for sbmlfile in sbmlfiles:
    simtime["LLJit"][sbmlfile] = []
    simtime["MCJit"][sbmlfile] = []


for (backend, bstr) in [(roadrunner.Config.LLJIT, "LLJit"), (roadrunner.Config.MCJIT, "MCJit")]:
    roadrunner.Config.setValue(roadrunner.Config.LLVM_BACKEND, backend)
    for n in range(nrepeats):
        print("Repeat", n)
        for sbmlfile in sbmlfiles:
            # print(sbmlfile)
            try:
                pre = time.perf_counter()
                r = roadrunner.RoadRunner(sbmlfile)
                post_load = time.perf_counter()
                # r.integrator.relative_tolerance = 1e-18
                # r.integrator.absolute_tolerance = 1e-22
                r.simulate(0, 100, 1000)
                post_sim = time.perf_counter()
                loadtime[bstr][sbmlfile].append(post_load - pre)
                simtime[bstr][sbmlfile].append(post_sim - post_load)
            except Exception as e:
                print(sbmlfile)
                print(e)

writeFullCSV("individual_times_backend_constant.csv") 

#Run everything, looping over the backend last:
for sbmlfile in sbmlfiles:
    simtime["LLJit"][sbmlfile] = []
    simtime["MCJit"][sbmlfile] = []


for n in range(nrepeats):
    print("Repeat", n)
    for sbmlfile in sbmlfiles:
        # print(sbmlfile)
        for (backend, bstr) in [(roadrunner.Config.LLJIT, "LLJit"), (roadrunner.Config.MCJIT, "MCJit")]:
            roadrunner.Config.setValue(roadrunner.Config.LLVM_BACKEND, backend)
            try:
                pre = time.perf_counter()
                r = roadrunner.RoadRunner(sbmlfile)
                post_load = time.perf_counter()
                r.simulate(0, 100, 1000)
                post_sim = time.perf_counter()
                loadtime[bstr][sbmlfile].append(post_load - pre)
                simtime[bstr][sbmlfile].append(post_sim - post_load)
            except Exception as e:
                print(sbmlfile)
                print(e)

writeFullCSV("individual_times_backend_changing_postscript.csv") 


      