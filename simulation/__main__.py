import sys
import os
import subprocess
from zipfile import ZipFile
from contextlib import contextmanager
from importlib import import_module

import server.server as server

@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


if len(sys.argv) > 1:
    if sys.argv[1] == '--headless':
        Env = getattr(import_module('env.'+sys.argv[2]), sys.argv[2])
        env = Env()
        env.run()

    if sys.argv[1] == 'run':
        server.run_server()

    if sys.argv[1] == 'install':
        if os.path.isdir('client/build'):
            print("AirTrafficSim has been installed before.")
        
        else:
            print("Installing AirTrafficSim.")

            print("\nInstalling yarn")
            subprocess.call('npm install -g yarn', shell=True)

            print("\nInstalling client: \n")
            with cd('client'):
                subprocess.call('yarn install', shell=True)
            
            print("\nInstalling server: \n")
            with cd('server'):
                subprocess.call('npm install', shell=True)

            try:
                with open('client/.env', 'x') as f:
                    print('\nEnter Cesium Ion token:')
                    x = input()
                    f.write('REACT_APP_CESIUMION_ACCESS_TOKEN='+x)
            except FileExistsError:
                print(".env with Cesium Ion token secret has been created before.")

            print("\nBuilding client: \n")
            with cd('client'):
                subprocess.call('yarn build', shell=True)
            
            try:
                import numpy
            except ImportError:
                print ("\nInstalling numpy")
                subprocess.call('conda install numpy', shell=True)

            try:
                import pandas
            except ImportError:
                print ("\nInstalling pandas")
                subprocess.call('conda install pandas', shell=True)

            if len(os.listdir('data/nav/xplane/')) <= 1:
                print("\n Unzipping X-plane navigation data.")
                ZipFile('data/nav/xplane_default_data.zip').extractall('data/nav/xplane/')

            print("\nInstallation completed.\nExecute \"python simulation run\" to start the simulation.")

            if len(os.listdir('data/BADA/')) <= 1 :
                print("\nBADA folder is empty. Remember to put the BADA performance data into /data/BADA/\n")
 
    
else:
    print('simulation')