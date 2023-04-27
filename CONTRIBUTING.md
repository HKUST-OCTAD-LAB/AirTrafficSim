# Contributing to airtrafficsim

The latest contributing guide is available in the documentation at: https://hkust-octad-lab.github.io/AirTrafficSim/development/guide.html

If you encounter any bugs, please report them in the [Issues board](https://github.com/HKUST-OCTAD-LAB/AirTrafficSim/issues). 

Please also feel free to contact us through the [discussin board](https://github.com/HKUST-OCTAD-LAB/AirTrafficSim/discussions) and/or raise any suggestion.

If you would like to contribute to AirTrafficSim, please fork this repository and create any pull requests. You may download AirTrafficSim with:

```
git clone https://github.com/HKUST-OCTAD-LAB/AirTrafficSim.git
conda env create -f environment.yml

cd AirTrafficSim
conda activate airtrafficsim
<!-- With UI -->
python -m airtrafficsim
<!-- Without UI -->
python -m airtrafficsim --headless <environment name>
```

Please also be reminded to unzip BADA 3.15 data files to [airtrafficsim_data/performance/BADA](data/performance/BADA/) and setup the API key for the weather database from ECMWF Climate Data Store following [this guide](https://cds.climate.copernicus.eu/api-how-to).


## Code of Conduct

We abide by the principles of openness, respect, and consideration of others
of the Python Software Foundation: https://www.python.org/psf/codeofconduct/.