import sys
import os
import numpy as np
import pandas as pd
from zipfile import ZipFile
from pathlib import Path
from importlib import import_module

import server.server as server


if len(sys.argv) > 1:
    if sys.argv[1] == 'run':
        if len(os.listdir('data/BADA/')) <= 1 :
                raise IOError("BADA folder is empty. Remember to put the BADA performance data into /data/BADA/.")
        
        if len(sys.argv) > 2 and sys.argv[2] == '--headless':
            Env = getattr(import_module('env.'+sys.argv[3]), sys.argv[3])
            env = Env()
            env.run()
        else:
            server.run_server()
 