import os
import glob
import time
import itertools
import multiprocessing
from multiprocessing import Process, Manager
from roadrunner.roadrunner import RoadRunner, Config
import get_biomodels


# Config.setValue(Config.LLVM_BACKEND, Config.LLJIT)
Config.setValue(Config.LLVM_BACKEND, Config.MCJIT)


def worker(fname: str, results):
    try:
        r = RoadRunner(fname)
        r.simulate(0, 100, 101)
        results[r.getModelName()] = r
    except Exception:
        # print(f"failed: {fname}")
        pass


if __name__ == "__main__":
    biomodels_folder = get_biomodels.get_biomodels()
    biomodels_files = glob.glob(os.path.join(biomodels_folder, "*.xml"))

    for i in range(5):
        start = time.time()
        manager = Manager()
        results = manager.dict()
        with multiprocessing.Pool(12) as p:
            starmap_arguments = itertools.product(biomodels_files, [results])
            p.starmap(worker, starmap_arguments)

        end = time.time() - start
        print("Took: ", end, "seconds")

"""
All errors are ignored
MCJit:
Took:  52.699562311172485 seconds
Took:  60.58261823654175 seconds
Took:  53.97505736351013 seconds
Took:  56.386879682540894 seconds
Took:  53.52746891975403 seconds

LLJit:
Took:  34.580451250076294 seconds
Took:  33.66169810295105 seconds
Took:  30.164960622787476 seconds
Took:  32.074339151382446 seconds
Took:  32.43431615829468 seconds

"""
