import logging

from basico import *
import os
import glob
import time
import sbmltoodepy
import sys
from importlib import import_module
import multiprocessing
from tqdm import tqdm
from testfixtures import LogCapture

raise ValueError("This tool is not suitable for solving the biomodels problem. "
                 "Uses odeint from scipy which repeatedly fails and takes a very long time "
                 "to do so. ")


def get_biomodels() -> str:
    """get curated section of biomodels locally.

    returns (str) biomodels folder path
    """

    try:
        from roadrunner.tests.download_biomodels import download_biomodels
    except ImportError:
        raise ImportError("Do a `pip install libroadrunner==2.2.0`")

    biomodels_folder = os.path.join(os.path.dirname(__file__), "biomodels")

    if not os.path.isdir(biomodels_folder):
        biomodels_folder = download_biomodels(os.path.dirname(__file__))

    if not os.path.isdir(biomodels_folder):
        raise NotADirectoryError(biomodels_folder)
    return biomodels_folder

def make_sbmltoodepy_folder():
    sbmltoodepy_folder = os.path.join(os.path.dirname(__file__), "sbmtoodepy")
    if not os.path.isdir(sbmltoodepy_folder):
        os.makedirs(sbmltoodepy_folder)

    sys.path += [
        sbmltoodepy_folder
    ]

    sbmltoodepy_init = os.path.join(sbmltoodepy_folder, "__init__.py")
    if not os.path.isfile(sbmltoodepy_init):
        with open(sbmltoodepy_init, 'w') as f:
            f.write("")
    if not os.path.isfile(sbmltoodepy_init):
        raise FileNotFoundError(sbmltoodepy_init)
    return sbmltoodepy_folder




def simulate(modelInstance):
    """Simulate the model instance.

    Other tools need to write the data to a results collection
    object. In sbmltoodepy, we need to do this manually but it still
    must be done to try to make things a little fairer.

    """
    species_names = list(modelInstance.s.keys())
    num_species = len(modelInstance.s)
    results = np.zeros((101, num_species+1))
    results[0] = modelInstance.time

    # init conc
    for i, species_name in enumerate(species_names):
        results[0, i+1] = modelInstance.s[species_name].concentration

    timeinterval = 1
    for time_point in range(100):
        modelInstance.RunSimulation(timeinterval)
        results[time_point+1, 0] = modelInstance.time
        for i, species_name in enumerate(species_names):
            results[time_point+1, i+1] = modelInstance.s[species_name].concentration

    return results


if __name__ == "__main__":
    biomodels_folder = get_biomodels()
    biomodels_files = glob.glob(os.path.join(biomodels_folder, "*.xml"))
    sbmltoodepy_folder = make_sbmltoodepy_folder()

    # pool = multiprocessing.pool.Pool(processes=8)


    # with open(os.path.join(os.path.dirname(__file__), "sbmltoodepy_times.txt"), 'w') as f:
    # with LogCapture(level=logging.WARN) as l:
        # for i in range(5):
    failures = 0
    start = time.time()
    for model_file in tqdm(biomodels_files[1:2]):
        try:
            # extract biomodels id
            biomodels_id = os.path.splitext(os.path.split(model_file)[1])[0]
            # create filename for python class
            fname = os.path.join(sbmltoodepy_folder, biomodels_id + ".py")
            # create python class using tool
            sbmltoodepy.ParseAndCreateModel(
                model_file,
                jsonFilePath=None,
                outputFilePath=fname,
                className=biomodels_id
            )
            # dynamically import it
            biomodels_model_module = import_module(name=biomodels_id)
            # extract the module
            model_class = getattr(biomodels_model_module, biomodels_id)
            # instantiate it
            model = model_class()
            results = simulate(model)
            # failures += len(l)
        except Exception:
            failures += 1
            print(f"Model {model_file} failed")

    end = time.time() - start

    print("Took: ", end, "seconds")
    print(failures)

"""
All errors are ignored
Took:  567.827169418335 seconds
Took:  628.3424892425537 seconds
Took:  564.9794456958771 seconds
Took:  531.3768444061279 seconds
Took:  566.8011341094971 seconds
"""