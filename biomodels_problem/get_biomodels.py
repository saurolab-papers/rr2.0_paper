import os
import time
import glob
import zipfile


def get_biomodels() -> str:
    """get curated section of biomodels locally.

    returns (str) biomodels folder path
    """
    biomodels_folder = os.path.join(os.path.dirname(__file__), "biomodels")
    if os.path.isdir(biomodels_folder):
        return biomodels_folder

    try:
        from roadrunner.tests.download_biomodels import download_biomodels
    except ImportError:
        raise ImportError("Do a `pip install libroadrunner==2.2.0`")


    biomodels_zip = download_biomodels(os.path.dirname(__file__))

    with zipfile.ZipFile(biomodels_zip, 'r') as zip_ref:
        zip_ref.extractall(biomodels_folder)

    if not os.path.isdir(biomodels_folder):
        raise NotADirectoryError(biomodels_folder)
    return biomodels_folder



