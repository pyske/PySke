
# PySke : Library of skeletons on distributed data structure in Python

Version 0.1alpha

- [INSTALLATION]
- [DEVELOPERS]
- [COPYRIGHT]

## INSTALLATION

This installation have been tested on Ubuntu 18.04.1 and macOS 10.14.01
Python version: 3.7.0

### Install MPI

- On Linux:
```
sudo apt-get install libcr-dev mpich2 mpich2-doc
```
- On macOS:
```
curl https://www.open-mpi.org/software/ompi/v3.0/downloads/openmpi-3.0.1.tar.gz -o openmpi-3.0.1.tar.gz
tar zxvf openmpi-13.0.1.tar.gz
cd openmpi-13.0.1
./configure --prefix=/usr/local
make all
sudo make install
```

### Install packages

1. Download get-pip.py: https://bootstrap.pypa.io/get-pip.py
- On Linux: 
```
wget https://bootstrap.pypa.io/get-pip.py
```
- On macOS: 
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```

2. Execute the python script get-pip.py
```
python3 get-pip.py
```

The installation of ```pip``` for python 3 needs to have the package ```launchpadlib```. It can be installed by:
```
pip install launchpadlib
```

To use the ```pip``` command, ```pip``` for python 2 must be installed. 
```
python get-pip.py
```

3. Install the necessary packages
```
pip3 install mpi4py
```
/!/ mpi4py necessists to get mpi (for C).

## DEVELOPERS
DEVELOPED BY
- Jolan Philippe (Northern Arizona University, Flagstaff, AZ, USA)
- Frédéric Loulergue (Northern Arizona University, Flagstaff, AZ, USA)

## COPYRIGHT
PySke is released into the public domain by the copyright holders.

This README file was originally written by [Jolan Philippe](https://github.com/JolanPhilippe) and is likewise released into the public domain.
