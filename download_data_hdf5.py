import os,sys
import subprocess
from extract_data_hdf5 import extractdata

# used for data urls
traindatalocation = {
    0: "yhrcf",
    1: "834pv",
    2: "9ep7r",
    3: "audqr",
    4: "wzrt2",
    5: "rt89a",
    6: "23hk6",
    7: "ujfwh",
    8: "fy5es",
    9: "9y57j",
    10: "vu2mn",
    11: "xbsev",
    12: "xa2mk",
    13: "s98ja",
    14: "7epq2",
}

validdatalocation = {
    15: "8cb4r",
    16: "s4xyu",
    17: "p7bjn"
}

testdatalocation = {
    18: "h7pb8",
    19: "wmt8e"
}


# where to save the data
traindatadir = "PilarDataTrain.h5"

validdatadir = "PilarDataValid.h5"

testdatadir = "PilarDataTest.h5"
    
# Download all data files, extract the clusters and save them, then delete the file    
for datafile in traindatalocation:
    dstring = "dlprod_768px_0"+str(datafile)+".root"
    dstringurl = "https://osf.io/"+traindatalocation[datafile]+"/download"
    subprocess.run(["wget","-O",dstring,dstringurl])
    extractdata(traindatadir,dstring)
    subprocess.run(["rm",dstring])

for datafile in validdatalocation:
    dstring = "dlprod_768px_0"+str(datafile)+".root"
    dstringurl = "https://osf.io/"+validdatalocation[datafile]+"/download"
    subprocess.run(["wget","-O",dstring,dstringurl])
    extractdata(validdatadir,dstring)
    subprocess.run(["rm",dstring])
    
for datafile in testdatalocation:
    dstring = "dlprod_768px_0"+str(datafile)+".root"
    dstringurl = "https://osf.io/"+testdatalocation[datafile]+"/download"
    subprocess.run(["wget","-O",dstring,dstringurl])
    extractdata(testdatadir,dstring)
    subprocess.run(["rm",dstring])
   

