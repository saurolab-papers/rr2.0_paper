# -*- coding: utf-8 -*-
"""
Created on Wed May  4 12:22:47 2022

@author: Lucian
"""

# import tellurium as te
import roadrunner
from os import walk
import time
import numpy as np

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


biomds = "C:/Users/Lucian/Desktop/temp-biomodels/final"
delays = ["BIOMD0000000024", "BIOMD0000000025", "BIOMD0000000034", "BIOMD0000000154", "BIOMD0000000155", "BIOMD0000000196", "BIOMD0000000841"]

bmfiles = []
for root, __, files in walk(biomds):
    include = True
    for delay in delays:
        if delay in root:
            include = False
    if include:
        bmfiles.append((root, files))
    
sbmlfiles = []

for (root, files) in bmfiles:
    
    for file in files:
        if ".xml" not in file:
            continue
        sbmlfiles.append(root + "/" + file)

loadtime = {}
loadtime["LLJit"] = {}
loadtime["MCJit"] = {}
for sbmlfile in sbmlfiles:
    loadtime["LLJit"][sbmlfile] = []
    loadtime["MCJit"][sbmlfile] = []

simtime = {}
simtime["LLJit"] = {}
simtime["MCJit"] = {}
for sbmlfile in sbmlfiles:
    simtime["LLJit"][sbmlfile] = []
    simtime["MCJit"][sbmlfile] = []

for (backend, bstr) in [(roadrunner.Config.LLJIT, "LLJit"), (roadrunner.Config.MCJIT, "MCJit")]:
    roadrunner.Config.setValue(roadrunner.Config.LLVM_BACKEND, backend)
    for n in range(5):
        print("Repeat", n)
        for sbmlfile in sbmlfiles:
            # print(sbmlfile)
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

times = open("individual_times.csv", "w")
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
averages = {}
stdevs = {}
totalsLL = np.zeros(10)
totalsMC = np.zeros(10)
for sbmlfile in loadtime[bstr]:
    times.write(sbmlfile)
    
    writeTimesFor(sbmlfile, loadtime, times)
    writeTimesFor(sbmlfile, simtime, times)

    times.write("\n")
times.close()

print(totalsLL)
print(totalsMC)
print("Average LL:", np.average(totalsLL))
print("Average MC:", np.average(totalsMC))
print("Std LL:", np.std(totalsLL))
print("Std MC:", np.std(totalsMC))
     
      