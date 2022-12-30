import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="airtrafficsim",
    version="1.0.0",
    author="kyfrankie",
    author_email="kyfrankie@gmail.com",
    description="Web-based air traffic simulation platform",
    url="https://github.com/harrylui1995/AirTrafficSim",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ),
)