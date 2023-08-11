from __future__ import print_function
import os,sys, time
import numpy as np
import ROOT as rt
from larcv import larcv
from tqdm import tqdm

# min voxel cutoff
minvox = 10


# count for number of data files already in folder
labelcount = {
    "Electron": 0,
    "Muon": 0,
    "Gamma": 0,
    "Pion": 0,
    "Proton": 0
}

# pdg number to label
mctolabelname = {
    11: "Electron",
    -11: "Electron",
    13: "Muon",
    -13: "Muon",
    22: "Gamma",
    211: "Pion",
    -211: "Pion",
    2212: "Proton",
    321: "other",
    1000010020: "other",
    1000020040: "other",
    1000010030: "other",
    1000020030: "other"
}


def main(argv,argc): #use like python3 ExtractData.py "../datalocation/" "root file"
    extractdata(argv[1], argv[2]) #Extract data from root file
    return 0


def extractdata(datadirectory,file):
    print(datadirectory)
    print(file)
    UpdateLabelCount(datadirectory)
    io = larcv.IOManager()
    io.add_in_file( datadirectory +file)
    io.initialize()
    NEntries = io.get_n_entries()
    print("Handling file:"+ file)
    for entry in tqdm(range(NEntries)):
        GetEntry(io, entry, datadirectory)
    for i in labelcount:
        print(file,":",i,"%06d"%labelcount[i])
    return 0

# for each entry get each cluster and save it as a .npy file
def GetEntry(io, entry, datadirectory):    
    io.read_entry(entry)
    ev_part    = io.get_data( larcv.kProductParticle, "mcst" )
    ev_cluster = io.get_data( larcv.kProductClusterVoxel3D, "mcst")
    meta = ev_cluster.meta()
    part_v = ev_part.as_vector()

    for icluster in range(ev_cluster.as_vector().size()):
        Cluster = GetCluster(ev_part, ev_cluster, meta, part_v, icluster) 
        if Cluster == 1: 
            continue
            
        npcluster, npcharge, pdg = Cluster
        npc = np.hstack((npcluster,npcharge))
        npc = npc.astype("float16")
        
        labelname = mctolabelname[pdg]
        
        if labelname != "other": # save all non other clusters
            with open(datadirectory+labelname+'/%06d.npy'%(labelcount[labelname]), 'wb') as f:
                np.save(f, npc)
            labelcount[labelname] = labelcount.get(labelname, 0) + 1
    io.clear_entry()
    return 0
            
def GetCluster(ev_part, ev_cluster, meta, part_v, icluster):
    cluster = ev_cluster.as_vector().at(icluster) # cluster is a voxel set
    nvox = cluster.as_vector().size()
    if nvox < minvox: # disregard clusters with less than minvox
        return 1
    npcluster = np.zeros( (nvox,3) )
    npcharge = np.zeros((nvox,1))
    for ivox in range(nvox):
        vox = cluster.as_vector().at(ivox)
        #print(vox.value())
        px = meta.id_to_x_index( vox.id() )
        py = meta.id_to_y_index( vox.id() )
        pz = meta.id_to_z_index( vox.id() )
        npcluster[ivox,0] = px
        npcluster[ivox,1] = py
        npcluster[ivox,2] = pz
        npcharge[ivox] = vox.value()

    # PID
    if icluster<part_v.size():
        pdg = part_v.at(icluster).pdg_code()
    else:
        pdg = 0 # the last cluster is noise
        return 1 # remove noise
    return npcluster, npcharge, pdg
    
    
def UpdateLabelCount(datadirectory):
    for i in labelcount:
        labelcount[i] = len(os.listdir(datadirectory+i))
    return 0
        
        
if __name__ == "__main__":
    main(sys.argv, len(sys.argv))