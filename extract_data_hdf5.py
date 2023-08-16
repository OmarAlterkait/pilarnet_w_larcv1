from __future__ import print_function
import os, sys, time
import numpy as np
import ROOT as rt
from larcv import larcv
from tqdm import tqdm
from hdf5_utils import write_to_hdf5
import h5py

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
    11: "Electron+",
    -11: "Electron-",
    13: "Muon+",
    -13: "Muon-",
    22: "Gamma",
    211: "Pion+",
    -211: "Pion-",
    2212: "Proton",
    321: "other",
    1000010020: "other",
    1000020040: "other",
    1000010030: "other",
    1000020030: "other"
}


def main(argv, argc):  # use like python3 ExtractData.py "../datalocation/" "root file"
    extractdata(argv[1], argv[2])  # Extract data from root file
    return 0


def extractdata(datadirectory, filelocation):
    print(datadirectory)
    print(filelocation)
    event_min = GetMaxEvent(datadirectory)
    io = larcv.IOManager()
    io.add_in_file(filelocation)
    io.initialize()
    NEntries = io.get_n_entries()
    print("Handling file:" + filelocation)
    for entry in tqdm(range(NEntries)):
        GetEntry(io, entry, datadirectory, event_min)
    return 0


# for each entry get each cluster and save it to hdf5 file
def GetEntry(io, entry, datadirectory, event_min):
    io.read_entry(entry)
    ev_part = io.get_data(larcv.kProductParticle, "mcst")
    ev_cluster = io.get_data(larcv.kProductClusterVoxel3D, "mcst")
    meta = ev_cluster.meta()
    part_v = ev_part.as_vector()

    # Lists to store attributes for each cluster
    coordinate_arrays = []
    labels = []
    energy_deposits = []
    energy_inits = []
    poss = []
    moms = []
    charges = []
    group_names = []

    for icluster in range(ev_cluster.as_vector().size()):
        Cluster = GetCluster(ev_part, ev_cluster, meta, part_v, icluster)
        if Cluster is None:
            continue

        npcluster, npcharge, label, energy_deposit, energy_init, pos, mom = Cluster

        # skip non wanted particles
        if mctolabelname[label] == "other":
            continue

        # Append data to lists
        coordinate_arrays.append(npcluster)
        labels.append(label)
        energy_deposits.append(energy_deposit)
        energy_inits.append(energy_init)
        poss.append(pos)
        moms.append(mom)
        charges.append(npcharge)
        group_names.append(f"event_{entry+event_min}")

    # Form the attributes dictionary
    attributes = {
        "labels": labels,
        "energy_deposit": energy_deposits,
        "energy_init": energy_inits,
        "pos": poss,
        "mom": moms,
        "charge": charges
    }

    # Call the HDF5 writing function
    write_to_hdf5(coordinate_arrays, attributes, group_names, filename=f"{datadirectory}")

    io.clear_entry()
    return 0


def GetCluster(ev_part, ev_cluster, meta, part_v, icluster):
    cluster = ev_cluster.as_vector().at(icluster)  # cluster is a voxel set
    nvox = cluster.as_vector().size()
    if nvox < minvox:  # disregard clusters with less than minvox
        return None
    npcluster = np.zeros((nvox, 3))
    npcharge = np.zeros((nvox, 1))
    for ivox in range(nvox):
        vox = cluster.as_vector().at(ivox)
        # print(vox.value())
        px = meta.id_to_x_index(vox.id())
        py = meta.id_to_y_index(vox.id())
        pz = meta.id_to_z_index(vox.id())
        npcluster[ivox, 0] = px
        npcluster[ivox, 1] = py
        npcluster[ivox, 2] = pz
        npcharge[ivox] = vox.value()

    # PID
    if icluster < part_v.size():
        label = part_v.at(icluster).pdg_code()
        energy_deposit = part_v.at(icluster).energy_deposit()
        energy_init = part_v.at(icluster).energy_init()
        x = part_v.at(icluster).x()
        y = part_v.at(icluster).y()
        z = part_v.at(icluster).z()
        px = part_v.at(icluster).px()
        py = part_v.at(icluster).py()
        pz = part_v.at(icluster).pz()

        pos = np.array([x, y, z])
        mom = np.array([px, py, pz])
    else:
        label = 0  # the last cluster is noise
        return None  # remove noise
    return npcluster, npcharge, label, energy_deposit, energy_init, pos, mom


def GetMaxEvent(file_location):
    if not os.path.isfile(file_location):
        return 0
    with h5py.File(file_location, 'r') as f:
        keys = list(f.keys())
    maxvalue = max([int(keys[i][6:]) for i, w in enumerate(keys) if w.startswith("event_")])
    return maxvalue+1
        

if __name__ == "__main__":
    main(sys.argv, len(sys.argv))
