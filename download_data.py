import os,sys
import subprocess
from extract_data import extractdata

# used for data urls
traindatalocation = {
    0:"hb437",
    1:"bhxpq",
    2:"eagwu",
    3:"uyj5e",
    4:"wbg5q",
    5:"qfv5k",
    6:"3k7p5"
}

validdatalocation = {
    7:"unj32",
    8:"e5vkw"
}

testdatalocation = {
    9:"zby9q"
}


# where to save the data
traindatadir = "../PilarData/Train/"

validdatadir = "../PilarData/Valid/"

testdatadir = "../PilarData/Test/"

labels = (
    "Electron",
    "Muon",
    "Gamma",
    "Pion",
    "Proton"
)

# Create datadir folders
for datadir in traindatadir, validdatadir, testdatadir:
    try:
        os.mkdir(datadir)
        print(datadir + " created")
    except FileExistsError:
        print(datadir + " already exists")



    # Create label folders    
    for label in labels:
        location = datadir + label
        try:
            os.mkdir(location)
            print(location + " created")
        except FileExistsError:
            print(location + " already exists")
    
# Download all data files, extract the clusters and save them, then delete the file    
for datafile in traindatalocation:
    dstring = "dlprod_512px_0"+str(datafile)+".root"
    dstringurl = "https://osf.io/"+traindatalocation[datafile]+"/download"
    subprocess.run(["wget","-O",dstring,dstringurl],cwd=traindatadir)
    extractdata(traindatadir,dstring)
    subprocess.run(["rm",dstring],cwd=traindatadir)

for datafile in validdatalocation:
    dstring = "dlprod_512px_0"+str(datafile)+".root"
    dstringurl = "https://osf.io/"+validdatalocation[datafile]+"/download"
    subprocess.run(["wget","-O",dstring,dstringurl],cwd=validdatadir)
    extractdata(validdatadir,dstring)
    subprocess.run(["rm",dstring],cwd=validdatadir)
    
for datafile in testdatalocation:
    dstring = "dlprod_512px_0"+str(datafile)+".root"
    dstringurl = "https://osf.io/"+testdatalocation[datafile]+"/download"
    subprocess.run(["wget","-O",dstring,dstringurl],cwd=testdatadir)
    extractdata(testdatadir,dstring)
    subprocess.run(["rm",dstring],cwd=testdatadir)
   

