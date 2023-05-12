from basico import *
import os
import glob
import time
import multiprocessing as mp

try:
    from roadrunner.tests.download_biomodels import download_biomodels
except ImportError:
    raise ImportError("Do a `pip install libroadrunner==2.2.0`")

biomodels_folder = os.path.join(os.path.dirname(__file__), "biomodels")

if not os.path.isdir(biomodels_folder):
    biomodels_folder = download_biomodels(os.path.dirname(__file__))

if not os.path.isdir(biomodels_folder):
    raise NotADirectoryError(biomodels_folder)

biomodels_files = glob.glob(os.path.join(biomodels_folder, "*.xml"))


def worker(model_file: str):
    try:
        # print(model_file)
        model = load_model(model_file)
        result = run_time_course(duration=100)
        remove_datamodel(model)
        remove_user_defined_functions()
    except Exception:
        print(f"Model {model_file} failed")


if __name__ == "__main__":
    for i in range(5):
        start = time.time()
        # in roadrunner, the pool spin-up time is included.
        # So we do the same here.
        p = mp.Pool(12)
        result = p.map(worker, (i for i in biomodels_files))
        end = time.time() - start
        print(f"Took {end} seconds")
        del p

"""
Took 64.14727401733398 seconds
Took 72.06279230117798 seconds
Took 64.87428712844849 seconds
Took 66.1524133682251 seconds
Took 72.38302445411682 seconds


"""
