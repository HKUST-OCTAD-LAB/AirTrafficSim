# Contributing to airtrafficsim

The latest contributing guide is available in the documentation at: https://hkust-octad-lab.github.io/AirTrafficSim/development/guide.html

If you encounter any bugs, please report them in the [Issues board](https://github.com/HKUST-OCTAD-LAB/AirTrafficSim/issues).

Please also feel free to contact us through the [discussion board](https://github.com/HKUST-OCTAD-LAB/AirTrafficSim/discussions) and/or raise any suggestions.

The roadmap of AirTrafficSim can be found in the [project board](https://github.com/orgs/HKUST-OCTAD-LAB/projects/3). Feel free to include your contribution in the timeline.

If you would like to contribute to AirTrafficSim, please clone or fork this repository and create pull requests by creating a new channel in this repository such that the CI service can run automated tests and build tasks. You may download AirTrafficSim with:

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

Please also be reminded to unzip BADA 3.15 data files to [airtrafficsim/data/performance/BADA](airtrafficsim/data/performance/BADA/) and set up the API key for the weather database from ECMWF Climate Data Store following [this guide](https://cds.climate.copernicus.eu/api-how-to).


## Code of Conduct

We abide by the principles of openness, respect, and consideration of others
of the Python Software Foundation: https://www.python.org/psf/codeofconduct/.