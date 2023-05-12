import logging

from basico import *
import os
import glob
import time
from testfixtures import LogCapture

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

print(len(biomodels_files))

for i in range(5):
    start = time.time()
    failures = 0
    for model_file in biomodels_files:
        try:
            with LogCapture(level=logging.ERROR) as l:
                # print(model_file)
                model = load_model(model_file)
                result = run_time_course(duration=100)
                remove_datamodel(model)
                remove_user_defined_functions()
            failures += len(l)
        except Exception:
            failures += 1
            print(f"Model {model_file} failed")

    end = time.time() - start

    print(f"Took {end} seconds")
    print(f"failures: {failures}")





"""
failures: 18
Took 163.52652502059937 seconds
Took 166.3809893131256 seconds
Took 164.32222771644592 seconds
Took 166.5122001171112 seconds
Took 157.41164374351501 seconds


"""



