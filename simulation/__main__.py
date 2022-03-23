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
    if sys.argv[1] == 'run':
        if len(os.listdir('data/nav/xplane/')) <= 1:
                print("\n Unzipping X-plane navigation data.")
                ZipFile('data/nav/xplane_default_data.zip').extractall('data/nav/xplane/')

        if len(os.listdir('data/BADA/')) <= 1 :
                raise IOError("BADA folder is empty. Remember to put the BADA performance data into /data/BADA/.")
        
        if len(sys.argv) > 2 and sys.argv[2] == '--headless':
            Env = getattr(import_module('env.'+sys.argv[3]), sys.argv[3])
            env = Env()
            env.run()
        else:
            server.run_server()
 
    
else:
    print('simulation')