from os import walk


def getSBMLFilesFromBiomodels(biomds = "C:/Users/Lucian/Desktop/temp-biomodels/final"):
    delays = ["BIOMD0000000024", "BIOMD0000000025", "BIOMD0000000034", "BIOMD0000000154", "BIOMD0000000155", "BIOMD0000000196", "BIOMD0000000841"]
    toleranceErrors = [
        "BIOMD0000000120",
        "BIOMD0000000152",
        "BIOMD0000000153",
        "BIOMD0000000250",
        "BIOMD0000000251",
        "BIOMD0000000404",
        "BIOMD0000000527",
        "BIOMD0000000540",
        "BIOMD0000000541",
        "BIOMD0000000583",
        "BIOMD0000000589",
        "BIOMD0000000589",
        "BIOMD0000000589",
        "BIOMD0000000589",
        "BIOMD0000000589",
        "BIOMD0000000589",
        "BIOMD0000000589",
        "BIOMD0000000609",
        "BIOMD0000000628",
        "BIOMD0000000634",
        "BIOMD0000000659",
        "BIOMD0000000696",
        "BIOMD0000000723",
        "BIOMD0000000732",
        "BIOMD0000000749",
        "BIOMD0000000760",
        "BIOMD0000000775",
        "BIOMD0000000856",
        "BIOMD0000000856",
        "BIOMD0000000883",
        "BIOMD0000000952",
        "BIOMD0000000968",
        "BIOMD0000001042",]
    bmfiles = []
    for root, __, files in walk(biomds):
        include = True
        for delay in delays:
            if delay in root:
                include = False
        for tolerr in toleranceErrors:
            if tolerr in root:
                include = False
        if include:
            bmfiles.append((root, files))
        
    sbmlfiles = []
    
    for (root, files) in bmfiles:
        
        for file in files:
            if ".xml" not in file:
                continue
            sbmlfiles.append(root + "/" + file)
    
    #If we only want a few files for testing.
    #sbmlfiles = sbmlfiles[:10]
    return sbmlfiles
