# -*- coding: utf-8 -*-
"""
Created on Wed May  4 12:22:47 2022

@author: Lucian
"""

# import tellurium as te
import pandas
from typing import *
import pandas as pd
import roadrunner
from os import walk
import os
import glob
import time
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

roadrunner.Config.setValue(roadrunner.Config.LOADSBMLOPTIONS_RECOMPILE, True)


def writeTimesFor(sbmlfile, timedata, times):
    averageLL = np.average(timedata["LLJit"][sbmlfile])
    averageMC = np.average(timedata["MCJit"][sbmlfile])
    stdLL = np.std(timedata["LLJit"][sbmlfile])
    stdMC = np.std(timedata["MCJit"][sbmlfile])
    ratio = averageMC / averageLL
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
biomds = r"D:\roadrunner\temp-biomodels\final"
delays = ["BIOMD0000000024", "BIOMD0000000025", "BIOMD0000000034", "BIOMD0000000154", "BIOMD0000000155",
          "BIOMD0000000196", "BIOMD0000000841"]

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

sbml_ids = [os.path.splitext(os.path.split(i)[1])[0] for i in sbmlfiles]


# loadtime = {}
# loadtime["LLJit"] = {}
# loadtime["MCJit"] = {}
# for sbmlfile in sbmlfiles:
#     loadtime["LLJit"][sbmlfile] = pd.Series()
#     loadtime["MCJit"][sbmlfile] = pd.Series()
#
# simtime = {}
# simtime["LLJit"] = {}
# simtime["MCJit"] = {}
# for sbmlfile in sbmlfiles:
#     simtime["LLJit"][sbmlfile] = []
#     simtime["MCJit"][sbmlfile] = []

def collect_data_backend_file_repeat(n_repeats: int = 5, n_sbml_files: int = 0, pickle_file: Optional[str] = None):
    """Measure the time taken to load and simulate sbml models. Loops are structured
    so that all LLJit are run first and then all MCJit are run second.

    Args:
        n_repeats: number of repeats to collect
        n_sbml_files: how many sbml file to use. Default 0 means do all
        pickle_file: if not None, read from pickle file. If not exists, create it.

    Returns:

    """
    if pickle_file is not None:
        if os.path.isfile(pickle_file):
            return pd.read_pickle(pickle_file)

    if n_sbml_files == 0:
        n_sbml_files = len(sbmlfiles)

    dct = dict()

    for (backend, bstr) in [(roadrunner.Config.LLJIT, "LLJit"), (roadrunner.Config.MCJIT, "MCJit")]:
        roadrunner.Config.setValue(roadrunner.Config.LLVM_BACKEND, backend)
        dct[bstr] = {}
        for sbmlfile in sbmlfiles[:n_sbml_files]:
            dct[bstr][sbmlfile] = {}
            print(sbmlfile)
            for n in range(n_repeats):
                dct[bstr][sbmlfile][n] = {}
                # print("Repeat", n)
                try:
                    pre = time.perf_counter()
                    r = roadrunner.RoadRunner(sbmlfile)
                    post_load = time.perf_counter()
                    r.simulate(0, 100, 1000)
                    post_sim = time.perf_counter()
                    dct[bstr][sbmlfile][n]["loadtime"] = post_load - pre
                    dct[bstr][sbmlfile][n]["simtime"] = post_sim - pre
                    # loadtime[bstr][sbmlfile].append(post_load - pre)
                    # simtime[bstr][sbmlfile].append(post_sim - post_load)
                    # print("simtime[bstr][sbmlfile]: ", simtime[bstr][sbmlfile])
                    # print("loadtime[bstr][sbmlfile]: ", loadtime[bstr][sbmlfile])
                except Exception as e:
                    continue
                    # print(sbmlfile)
                    # print(e)
            dct[bstr][sbmlfile] = pd.DataFrame(dct[bstr][sbmlfile])
        dct[bstr] = pd.concat(dct[bstr])

    df = pd.concat(dct)
    df = pd.DataFrame(df.stack())

    df.index.names = ["jit", "sbml", "which", "repeat"]
    df.columns = ["time"]
    df = df.pivot_table(index=["jit", "sbml", "repeat"], columns="which", values="time")

    if pickle_file is not None:
        df.to_pickle(pickle_file)
    return df


def collect_data_file_backend_repeat(n_repeats: int = 5, n_sbml_files: int = 0, pickle_file: Optional[str] = None):
    """Measure the time taken to load and simulate sbml models. Loops are structured
    so that for each sbml file we run the LLJit followed by MCJit.

    Args:
        n_repeats: number of repeats to collect
        n_sbml_files: how many sbml file to use. Default 0 means do all
        pickle_file: if not None, read from pickle file. If not exists, create it.

    Returns:

    """
    if pickle_file is not None:
        if os.path.isfile(pickle_file):
            return pd.read_pickle(pickle_file)

    if n_sbml_files == 0:
        n_sbml_files = len(sbmlfiles)

    dct = dict()

    for sbmlfile in sbmlfiles[:n_sbml_files]:
        print(sbmlfile)
        dct[sbmlfile] = {}
        for (backend, bstr) in [(roadrunner.Config.LLJIT, "LLJit"), (roadrunner.Config.MCJIT, "MCJit")]:
            roadrunner.Config.setValue(roadrunner.Config.LLVM_BACKEND, backend)
            dct[sbmlfile][bstr] = {}
            for n in range(n_repeats):
                dct[sbmlfile][bstr][n] = {}
                # print("Repeat", n)
                try:
                    pre = time.perf_counter()
                    r = roadrunner.RoadRunner(sbmlfile)
                    post_load = time.perf_counter()
                    r.simulate(0, 100, 1000)
                    post_sim = time.perf_counter()
                    dct[sbmlfile][bstr][n]["loadtime"] = post_load - pre
                    dct[sbmlfile][bstr][n]["simtime"] = post_sim - pre
                    # loadtime[bstr][sbmlfile].append(post_load - pre)
                    # simtime[bstr][sbmlfile].append(post_sim - post_load)
                    # print("simtime[bstr][sbmlfile]: ", simtime[bstr][sbmlfile])
                    # print("loadtime[bstr][sbmlfile]: ", loadtime[bstr][sbmlfile])
                except Exception as e:
                    continue
                    # print(sbmlfile)
                    # print(e)
            dct[sbmlfile][bstr] = pd.DataFrame(dct[sbmlfile][bstr])
        dct[sbmlfile] = pd.concat(dct[sbmlfile])

    df = pd.concat(dct)
    df = pd.DataFrame(df.stack())
    print(df)

    df.index.names = ["sbml", "jit", "which", "repeat"]
    df.columns = ["time"]
    df = df.pivot_table(index=["jit", "sbml", "repeat"], columns="which", values="time")

    if pickle_file is not None:
        df.to_pickle(pickle_file)
    return df

def collect_data_repeat_file_backend(n_repeats: int = 5, n_sbml_files: int = 0, pickle_file: Optional[str] = None):
    """Measure the time taken to load and simulate sbml models. Loops are structured
    so that for each sbml file we run the LLJit followed by MCJit.

    Args:
        n_repeats: number of repeats to collect
        n_sbml_files: how many sbml file to use. Default 0 means do all
        pickle_file: if not None, read from pickle file. If not exists, create it.

    Returns:

    """
    if pickle_file is not None:
        if os.path.isfile(pickle_file):
            return pd.read_pickle(pickle_file)

    if n_sbml_files == 0:
        n_sbml_files = len(sbmlfiles)

    dct = dict()

    for n in range(n_repeats):
        dct[n] = {}
        for sbmlfile in sbmlfiles[:n_sbml_files]:
            print("sbmlfile: ", sbmlfile)
            dct[n][sbmlfile] = {}
            for (backend, bstr) in [(roadrunner.Config.LLJIT, "LLJit"), (roadrunner.Config.MCJIT, "MCJit")]:
                roadrunner.Config.setValue(roadrunner.Config.LLVM_BACKEND, backend)
                dct[n][sbmlfile][bstr] = {}
                # print("Repeat", n)
                try:
                    pre = time.perf_counter()
                    r = roadrunner.RoadRunner(sbmlfile)
                    post_load = time.perf_counter()
                    r.simulate(0, 100, 1000)
                    post_sim = time.perf_counter()
                    dct[n][sbmlfile][bstr]["loadtime"] = post_load - pre
                    dct[n][sbmlfile][bstr]["simtime"] = post_sim - pre
                    # loadtime[bstr][sbmlfile].append(post_load - pre)
                    # simtime[bstr][sbmlfile].append(post_sim - post_load)
                    # print("simtime[bstr][sbmlfile]: ", simtime[bstr][sbmlfile])
                    # print("loadtime[bstr][sbmlfile]: ", loadtime[bstr][sbmlfile])
                except Exception as e:
                    continue
                    # print(sbmlfile)
                    # print(e)
            dct[n][sbmlfile] = pd.DataFrame(dct[n][sbmlfile])
        dct[n] = pd.concat(dct[n])

    df = pd.concat(dct)
    df = pd.DataFrame(df.stack())

    df.index.names = ["repeat", "sbml", "which", "jit"]
    df.columns = ["time"]
    df = df.pivot_table(index=["jit", "sbml", "repeat"], columns="which", values="time")

    if pickle_file is not None:
        df.to_pickle(pickle_file)
    return df


def plot_mcjit_over_lljit(data: pd.DataFrame, label):
    """Divide MCJit by LLJit gives us speed up (>1) or slowdown (<1) by LLJit over MCJit

    Examples
    ---------
    LLJit
    sbml                                               repeat
    D:\roadrunner\temp-biomodels\final\BIOMD0000000... 0       0.029918  0.030700
                                                       1       0.020862  0.021687
                                                       2       0.022913  0.023697
                                                       3       0.020498  0.021232
                                                       4       0.021235  0.022075
    MCJit
    D:\roadrunner\temp-biomodels\final\BIOMD0000000... 0       0.090949  0.091757
                                                       1       0.080610  0.081414
                                                       2       0.089672  0.090426
                                                       3       0.077763  0.078521
                                                       4       0.078367  0.079244

    MCJit    / LLJit
    0.090949 / 0.029918 = 3.03994250953 times speed up using LLJit compared to MCJit

    (right?)

    """


    ratio = data.loc["MCJit"] / data.loc["LLJit"]
    # ratio = data.loc["LLJit"] / data.loc["MCJit"]
    stats: pd.DataFrame = ratio.groupby(level=["sbml"]).aggregate(np.mean)
    # plt.bar(range(stats.shape[0]), stats["loadtime"])

    plt.figure()
    sns.displot(stats["loadtime"])
    plt.title(f"Loadtimes (MCJit / LLJit) {label}")
    fname = os.path.join(os.path.dirname(__file__), f"loadtimes_{label}.png")
    plt.savefig(fname, dpi=250, bbox_inches="tight")

    plt.figure()
    sns.displot(stats["simtime"])
    plt.title(f"Simulation Times (MCJit / LLJit) {label}")
    fname = os.path.join(os.path.dirname(__file__), f"simtimes_{label}.png")
    plt.savefig(fname, dpi=250, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    # Note: These have already been run on my 8 core dell xps, i9.
    #  Passing in the PICKLE_* variable to collect_data_* functions will just load
    #  saved data from file.
    PICKLE_DATA_NO_SWITCHING = os.path.join(os.path.dirname(__file__), "rr_load_times_backend_file_repeat.pickle")
    PICKLE_DATA_SWITCHING = os.path.join(os.path.dirname(__file__), "rr_load_times_file_backend_repeat.pickle")
    PICKLE_DATA_SWITCHING_REPEAT_FIRST = os.path.join(os.path.dirname(__file__),
                                                      "rr_load_times_repeat_file_backend.pickle")
    file_backend_repeat_data = collect_data_file_backend_repeat(n_sbml_files=0, pickle_file=PICKLE_DATA_SWITCHING)
    backend_file_repeat_data = collect_data_backend_file_repeat(pickle_file=PICKLE_DATA_NO_SWITCHING)

    # data where repeat/file/backends are looped over
    repeat_file_backend_data = collect_data_repeat_file_backend(n_sbml_files=0, pickle_file=PICKLE_DATA_SWITCHING_REPEAT_FIRST)

    print(repeat_file_backend_data)

    plot_mcjit_over_lljit(backend_file_repeat_data, label="backend_file_repeat")
    plot_mcjit_over_lljit(file_backend_repeat_data, label="file_backend_repeat")
    plot_mcjit_over_lljit(repeat_file_backend_data, label="repeats_files_backends")

    print(backend_file_repeat_data - file_backend_repeat_data)

    # print(no_switch_data)
    # print(switch_data)

    #

    # can we plot the ratio of MCJit to LLJit times?
    # no_switch_data["MCJit/LLJit"] = no_switch_data.loc["MCJit"] / no_switch_data.loc["LLJit"]
    # mc_over_ll = no_switch_data.loc["MCJit"] / no_switch_data.loc["LLJit"]

    # print(no_switch_data)

    # # groupby everything but the repeat so we can aggregate the repeat. (do a loop on data.groupby to see)
    # print(no_switch_data.groupby(level=["jit", "sbml"]).aggregate([np.mean, np.std]))

# print(dct)
# import pandas as pd
#
# print(pd.DataFrame.from_dict(dct))
# load_df = pd.DataFrame.from_dict(loadtime)
# print(load_df)
# times = open("individual_times.csv", "w")
# times.write("File")
# times.write(", ")
# times.write("LLJit load")
# times.write(", ")
# times.write("err LLJit load")
# times.write(", ")
# times.write("MCJit load")
# times.write(", ")
# times.write("err MCJit load")
# times.write(", ")
# times.write("MC/LL load")
# times.write(", ")
# times.write("LLJit sim")
# times.write(", ")
# times.write("err LLJit sim")
# times.write(", ")
# times.write("MCJit sim")
# times.write(", ")
# times.write("err MCJit sim")
# times.write(", ")
# times.write("MC/LL sim")
# times.write("\n")
# averages = {}
# stdevs = {}
# totalsLL = np.zeros(10)
# totalsMC = np.zeros(10)
# for sbmlfile in loadtime[bstr]:
#     times.write(sbmlfile)
#
#     writeTimesFor(sbmlfile, loadtime, times)
#     writeTimesFor(sbmlfile, simtime, times)
#
#     times.write("\n")
# times.close()
#
# print(totalsLL)
# print(totalsMC)
# print("Average LL:", np.average(totalsLL))
# print("Average MC:", np.average(totalsMC))
# print("Std LL:", np.std(totalsLL))
# print("Std MC:", np.std(totalsMC))
#
# #
