import os
import glob
import time
import sys
import multiprocessing
from roadrunner.roadrunner import RoadRunner, Config
try:
    from get_biomodels import get_biomodels
except ImportError:
    def get_biomodels():
        return os.path.join(os.path.dirname(__file__), "biomodels")
# Config.setValue(Config.LLVM_BACKEND, Config.LLJIT)
# Config.setValue(Config.LLVM_BACKEND, Config.MCJIT)

# we have to disable to model caching so that repeats are independent
Config.setValue(Config.LOADSBMLOPTIONS_RECOMPILE, True)

if __name__ == "__main__":

    biomodels_folder = get_biomodels()

    biomodels_files = glob.glob(os.path.join(biomodels_folder, "*.xml"))

    for i in range(5):
        start = time.time()
        dct = dict()
        failure_counts = 0
        for model_file in biomodels_files:
            # print(model_file)
            try:
                # extract biomodels id
                biomodels_id = os.path.splitext(os.path.split(model_file)[1])[0]
                dct[biomodels_id] = RoadRunner(model_file)
                res = dct[biomodels_id].simulate(0, 100, 101)
                # print(res)
            except Exception:
                failure_counts += 1
                print(f"Model {model_file} failed")

        end = time.time() - start

        print("Took: ", end, "seconds")
        print(failure_counts)

"""
All errors are ignored
MCJit Serial
failures: 20
    Took:  134.4723436832428 seconds
    Took:  136.3477861881256 seconds
    Took:  142.4529595375061 seconds
    Took:  137.06864976882935 seconds
    Took:  144.9366843700409 seconds

LLJit Serial
    model failures: 20
    Took:  48.510576009750366 seconds
    Took:  38.56596040725708 seconds
    Took:  38.06661581993103 seconds
    Took:  38.09479331970215 seconds
    Took:  38.26501393318176 seconds

RoadRunner v2.0.0
Took:  148.05567336082458 seconds
Took:  161.6247260570526 seconds
Took:  154.80478954315186 seconds
Took:  157.07073497772217 seconds
Took:  155.3123631477356 seconds

RoadRunner v1.6.1
Took:  142.58917140960693 seconds
Took:  151.32360291481018 seconds
Took:  149.48247933387756 seconds
Took:  150.19932913780212 seconds
Took:  156.40406203269958 seconds

1.5.6.1

"""