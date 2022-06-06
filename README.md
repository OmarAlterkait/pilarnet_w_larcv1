# pilarnet_w_larcv1

# To start:

Initialize the submodule pointing to `larcv` (specifically LArCV1).

    git submodule init
    git submodule update


# Dependencies

Just ROOT. Make sure you have ROOT environment variables setup. This is usually calling `thisroot.sh`.

Go into the larcv folder and make a build folder

    cd larcv
    mkdir build

Setup the build

    cd build
    cmake -DUSE_PYTHON3=ON ../

Run the build

    make install -j4

You should be able to run the example notebook now.