import sys
import os
import subprocess
from contextlib import contextmanager

from env import Environment

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
        env = Environment()
        for i in range (1000):
            env.step()

    if sys.argv[1] == 'run':
        with cd('server'):
            subprocess.call('npm start', shell=True)

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
                    print('\nEnter Cesium Ion token"')
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
                print ("\nnumpy is not installed")

            print("\nInstallation completed.\nExecute \"python simulation run\" to start the simulation.")

            if len(os.listdir('data/BADA/')) <= 1 :
                print("\nBADA folder is empty. Remember to put the BADA performance data into /data/BADA/\n")
      
    
else:
    print('simulation')