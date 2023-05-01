# Test development

AirTrafficSim is set up with an automated CI workflow to run testing and building tasks when a pull request is created to merge a commit to the main channel. The test cases are stored in the `tests` folder and we welcome everyone to contribute to the development of unit and integration tests of AirTrafficSim.

## Installation

AirTrafficSim uses [pytest](https://docs.pytest.org/en/7.3.x/) and [Coverage.py](https://coverage.readthedocs.io/en/7.2.5/) as the test suits. The following commands will install the dependencies for testing:

```bash
conda activate airtrafficsim
conda install -c conda-forge pytest coverage
```

## Running tests

To run the test cases and generate coverage reports, please run the following commands at the root directory `AirTrafficSim/`.

```bash
conda activate airtrafficsim
cd AirTrafficSim
coverage run -m pytest
coverage report
```