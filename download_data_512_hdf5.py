import os,sys
import subprocess
from extract_data_hdf5 import extractdata

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
traindatadir = "PilarDataTrain.h5"

validdatadir = "PilarDataValid.h5"

testdatadir = "PilarDataTest.h5"
    
# Download all data files, extract the clusters and save them, then delete the file    
for datafile in traindatalocation:
    dstring = "dlprod_512px_0"+str(datafile)+".root"
    dstringurl = "https://osf.io/"+traindatalocation[datafile]+"/download"
    subprocess.run(["wget","-O",dstring,dstringurl])
    extractdata(traindatadir,dstring)
    subprocess.run(["rm",dstring])

for datafile in validdatalocation:
    dstring = "dlprod_512px_0"+str(datafile)+".root"
    dstringurl = "https://osf.io/"+validdatalocation[datafile]+"/download"
    subprocess.run(["wget","-O",dstring,dstringurl])
    extractdata(validdatadir,dstring)
    subprocess.run(["rm",dstring])
    
for datafile in testdatalocation:
    dstring = "dlprod_512px_0"+str(datafile)+".root"
    dstringurl = "https://osf.io/"+testdatalocation[datafile]+"/download"
    subprocess.run(["wget","-O",dstring,dstringurl])
    extractdata(testdatadir,dstring)
    subprocess.run(["rm",dstring])
   

