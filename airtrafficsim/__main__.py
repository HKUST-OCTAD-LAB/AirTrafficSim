import sys
import os
import argparse
from pathlib import Path
from importlib import import_module
from zipfile import ZipFile

import airtrafficsim.server.server as server

def main():
    # Unpack client
    if not Path(__file__).parent.resolve().joinpath('./data/client/build/').is_dir():
        print("Unzipping client.")
        ZipFile(Path(__file__).parent.resolve().joinpath('./data/client/build.zip')
                ).extractall(Path(__file__).parent.resolve().joinpath('./data/client/'))

    # Create a parser for command line arguments
    parser = argparse.ArgumentParser(
        prog='AirTrafficSim',
        description='Command line interfaces of AirTrafficSim.'
    )
    parser.add_argument('--init',
                        type=Path,
                        help='Create a symbloic link to the data folder: airtrafficsim init <path to a folder>.')
    parser.add_argument('--headless',
                        type=str,
                        help='Run user defined environment without UI: airtrafficsim --headless <env name>.')
    
    args = parser.parse_args()

    if args.init:
        # Create a symbolic link to the data folder
        if Path.cwd().joinpath(args.init).is_dir():
            Path.cwd().joinpath(args.init).resolve().joinpath('airtrafficsim_data').symlink_to(Path(__file__).parent.resolve().joinpath('./data'), target_is_directory=True)
        else:
            raise IOError("The path you provided does not exist. Please provide a valid path.")
    else:
        # Give error if BADA data is missing TODO: To be removed when OpenAP is implemented
        if len(list(Path(__file__).parent.resolve().joinpath('./data/performance/BADA/').glob('*'))) <= 1:
            raise IOError(
                "BADA folder is empty. Remember to put the BADA performance data into /data/performance/BADA/.")
        if args.headless:
            # Run user defined environment without UI
            Env = getattr(import_module('airtrafficsim.data.environment.' +
                        sys.argv[2], '...'), sys.argv[2])
            env = Env()
            env.run()
        else:
            # Run AirTrafficSim with UI
            server.run_server()


if __name__ == "__main__":
    main()
