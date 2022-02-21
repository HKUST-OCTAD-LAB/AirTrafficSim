import sys
import os
from env import Environment

if len(sys.argv) > 1:
    if sys.argv[1] == '--headless':
        # os.remove("/home/kyfrankie/OpenUTMsim/server/data/simulation.csv")  #TODO: change to relative path
        env = Environment()
        for i in range (500):
            env.step()
    
else:
    print('simulation')