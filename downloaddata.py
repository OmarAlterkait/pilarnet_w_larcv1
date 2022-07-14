import os,sys
import subprocess
#from extractdata import extractdata

# used for data urls
datalocation = {
    0:"hb437",
    1:"bhxpq",
    2:"eagwu",
    3:"uyj5e",
    4:"wbg5q",
    5:"qfv5k",
    6:"3k7p5",
    7:"unj32",
    8:"e5vkw",
    9:"zby9q"
}

# where to save the data
datadir = "../data3d1/"

labels = (
    "Electron",
    "Muon",
    "Gamma",
    "Pion",
    "Proton"
)

# Create datadir folder
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
for datafile in datalocation:
    dstring = "dlprod_512px_0"+str(datafile)+".root"
    dstringurl = "https://osf.io/"+datalocation[datafile]+"/download"
    subprocess.run(["wget","-O",dstring,dstringurl],cwd=datadir)
    extractdata(datadir,dstring)
    subprocess.run(["rm",dstring],cwd=datadir)
    
   

