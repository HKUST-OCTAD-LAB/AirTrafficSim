# Development guide

AirTrafficSim is published on [GitHub](https://github.com/HKUST-OCTAD-LAB/AirTrafficSim) under [GPL-3.0 license](https://github.com/HKUST-OCTAD-LAB/AirTrafficSim/blob/main/LICENSE). We welcome everyone interested to contribute to this project by reporting bugs, providing suggestions, and participating in development.

## Progress

You may check out what are the planned and ongoing development of AirTrafficSim by visiting our [project board](https://github.com/orgs/HKUST-OCTAD-LAB/projects/3/views/2).

## Bugs and issues

For any bugs and issues found, please feel free to raise a new issue in the [Issue board](https://github.com/HKUST-OCTAD-LAB/AirTrafficSim/issues).

## Suggestions and ideas

For any features suggestion or any ideas in general, please feel free to raise a new discussion in the [Discussion board](https://github.com/HKUST-OCTAD-LAB/AirTrafficSim/discussions).

## Code development

We welcome everyone to contribute to the development of AirTrafficSim. You can open a new item in the [Projects board](https://github.com/HKUST-OCTAD-LAB/AirTrafficSim/discussions) to share your goal. Then, clone or fork this repository to develop your feature. When your work is completed, please push your work to a new channel in the [AirTrafficSim repository](https://github.com/HKUST-OCTAD-LAB/AirTrafficSim) and create a pull request such that the CI service can run automated tests and build tasks. After review, your work and branch will be merged into the main branch where everyone will be able to use your new feature.

You may download AirTrafficSim with:

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

```{important}
Please also be reminded to unzip BADA 3.15 data files to `airtrafficsim/data/performance/BADA` and set up the API key for the weather database from ECMWF Climate Data Store following [this guide](https://cds.climate.copernicus.eu/api-how-to).
```

You can update AirTrafficSim with the newest changes by executing the following command.

``` bash
git pull
```

```{tip}
You may git commit and/or push your local changes first before pulling new remote changes to avoid overwriting your changes.
```