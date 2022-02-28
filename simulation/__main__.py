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

            print("Installing client.")
            with cd('client'):
                subprocess.call('yarn install', shell=True)
            
            print("Installing server.")
            with cd('server'):
                subprocess.call('npm install', shell=True)

            try:
                with open('client/.env', 'x') as f:
                    print('Enter Cesium Ion token:')
                    x = input()
                    f.write('REACT_APP_CESIUMION_ACCESS_TOKEN='+x)
            except FileExistsError:
                print(".env with Cesium Ion token secret has been created before.")

            print("Building client.")
            with cd('client'):
                subprocess.call('yarn build', shell=True)
            
            try:
                import numpy
            except ImportError:
                print ("numpy is not installed")

            if not os.listdir('data/BADA/') :
                print("BADA folder is empty. Remember to put the BADA performance data into /data/BADA/")

            print("Installation completed.\n Execute \"python simulation run\" to start the simulation.")
      
    
else:
    print('simulation')