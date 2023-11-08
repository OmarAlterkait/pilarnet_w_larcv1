import h5py
import numpy as np


def write_to_hdf5(coordinate_arrays, attributes, groups, filename="data.h5"):
    with h5py.File(filename, 'a') as f:
        # Combine datasets and their properties into one dictionary
        datasets = {
            "coordinates": {"dtype": np.int16, "initial_shape": (0, 3)},
            "start_indices": {"dtype": np.int64, "initial_shape": (0,)},
            "end_indices": {"dtype": np.int64, "initial_shape": (0,)},
            "labels": {"dtype": np.int16, "initial_shape": (0,)},
            "energy_deposit": {"dtype": np.float16, "initial_shape": (0,)},
            "energy_init": {"dtype": np.float16, "initial_shape": (0,)},
            "pos": {"dtype": np.float16, "initial_shape": (0, 3)},
            "mom": {"dtype": np.float16, "initial_shape": (0, 3)},
            "charge": {"dtype": np.float16, "initial_shape": (0,)}
        }

        # Check datasets existence or create them with initial shape
        for name, props in datasets.items():
            if name not in f:
                shape = props["initial_shape"]
                maxshape = (None,) + shape[1:]
                f.create_dataset(name, shape=shape, maxshape=maxshape, dtype=props["dtype"], compression="gzip", chunks=True)

        # References to datasets
        dset_references = {name: f[name] for name in datasets}

        # Extract attributes
        labels = attributes["labels"]
        energy_deposit = attributes["energy_deposit"]
        energy_init = attributes["energy_init"]
        pos = attributes["pos"]
        mom = attributes["mom"]
        charge = attributes["charge"]

        # Calculate new start and end indices
        current_length = len(dset_references["coordinates"])
        new_start_indices = np.cumsum([0] + [len(arr) for arr in coordinate_arrays[:-1]]) + current_length
        new_end_indices = np.cumsum([len(arr) for arr in coordinate_arrays]) + current_length

        # Resize datasets
        total_new_coords = sum([len(arr) for arr in coordinate_arrays])
        dset_references["coordinates"].resize((current_length + total_new_coords, 3))
        dset_references["charge"].resize((current_length + total_new_coords,))
        for name, data in zip(["start_indices", "end_indices", "labels", "energy_deposit", "energy_init"],
                              [coordinate_arrays, coordinate_arrays, labels, energy_deposit, energy_init]):
            dset_references[name].resize((len(dset_references[name]) + len(data),))
        for name, data in zip(["pos", "mom"], [pos, mom]):
            dset_references[name].resize((len(dset_references[name]) + len(data), 3))

        # Write data using defined dtypes
        dset_references["coordinates"][-total_new_coords:] = np.concatenate(coordinate_arrays, axis=0).astype(datasets["coordinates"]["dtype"])
        dset_references["charge"][-total_new_coords:] = np.concatenate(charge, axis=0).flatten().astype(datasets["charge"]["dtype"])
        dset_references["start_indices"][-len(coordinate_arrays):] = new_start_indices.astype(datasets["start_indices"]["dtype"])
        dset_references["end_indices"][-len(coordinate_arrays):] = new_end_indices.astype(datasets["end_indices"]["dtype"])
        dset_references["labels"][-len(labels):] = np.array(labels, dtype=datasets["labels"]["dtype"])
        dset_references["energy_deposit"][-len(energy_deposit):] = np.array(energy_deposit, dtype=datasets["energy_deposit"]["dtype"])
        dset_references["energy_init"][-len(energy_init):] = np.array(energy_init, dtype=datasets["energy_init"]["dtype"])
        dset_references["pos"][-len(pos):] = np.vstack(pos).astype(datasets["pos"]["dtype"])
        dset_references["mom"][-len(mom):] = np.vstack(mom).astype(datasets["mom"]["dtype"])

        # Update group indices
        for idx, group_name in enumerate(groups, start=len(dset_references["start_indices"]) - len(coordinate_arrays)):
            grp = f.require_group(group_name)
            if 'indices' not in grp:
                grp.create_dataset('indices', shape=(0,), maxshape=(None,), dtype=np.int32, compression="gzip")
            grp['indices'].resize((len(grp['indices']) + 1,))
            grp['indices'][-1] = idx


def read_from_hdf5_given_group(filename="data.h5", group_name="group0"):
    with h5py.File(filename, 'r') as f:
        if group_name not in f:
            print(f"No group named {group_name} found in the HDF5 file.")
            return

        grp = f[group_name]
        datasets = ["coordinates", "start_indices", "end_indices", "labels", "energy_deposit", "energy_init", "pos", "mom", "charge"]
        dset_references = {name: f[name] for name in datasets}

        group_indices = grp['indices'][:]

        print(f"Reading data for group: {group_name}")

        for idx in group_indices:
            start, end = int(dset_references["start_indices"][idx]), int(dset_references["end_indices"][idx])
            print(f"Reading data for index: {idx}")
            print("Coordinates:")
            print(dset_references["coordinates"][start:end])

            print("Charge:")
            print(dset_references["charge"][start:end])

            # Fetch data from the datasets using the index
            for name in ["labels", "energy_deposit", "energy_init", "pos", "mom"]:
                print(f"{name.capitalize()}: {dset_references[name][idx]}")
            print('-' * 50)


def read_from_hdf5_given_index(filename="data.h5", index=0):
    with h5py.File(filename, 'r') as f:
        datasets = ["coordinates", "labels", "energy_deposit", "energy_init", "pos", "mom", "start_indices",
                    "end_indices", "charge"] 
        dset_references = {name: f[name] for name in datasets}

        start, end = int(dset_references["start_indices"][index]), int(dset_references["end_indices"][index])

        print(f"Reading data for index: {index}")
        print("Coordinates:")
        print(dset_references["coordinates"][start:end])

        print("Charge:")
        print(dset_references["charge"][start:end])

        # Fetch data from the datasets using the index
        for name in ["labels", "energy_deposit", "energy_init", "pos", "mom"]:  # Added charge
            print(f"{name.capitalize()}: {dset_references[name][index]}")
        print('-' * 50)


if __name__ == "__main__":
    # example usage of reading an entire event
    read_from_hdf5_given_group("../PilarData/PilarDataTrain.h5", "event_1")

    # example usage of reading a single particle
    read_from_hdf5_given_index("../PilarData/PilarDataTrain.h5", 100)


