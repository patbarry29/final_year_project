# Terrain-aware simulator for evaluating flight plans for Unmanned Aerial Vehicles
This is the code for my final year project. To run this code, the following packages will have to be installed:
 - gdal for Python - A useful guide for [macOS](https://gist.github.com/kelvinn/f14f0fc24445a7994368f984c3e37724), [Windows](https://pypi.org/project/GDAL/) and [Unix](https://mothergeo-py.readthedocs.io/en/latest/development/how-to/gdal-ubuntu-pkg.html)
 - haversine - can be installed through pip, [guide](https://pypi.org/project/haversine/)
 - scipy - can be installed through pip, [guide](https://scipy.org/install/)

The following packages are also required, but most likely already installed:
 - matplotlib
 - pathlib
 - numpy, [guide](https://numpy.org/install/)

To compare all algorithms using numerical results, run compare_all_algs.py.
To compare the flight paths plotted on a terrain map, run ColourMapSeveral.py.  
All terrain files are contained within the ireland folder, while all Python files are stored in the code folder.
