"""Navigation database"""
from pathlib import Path
import numpy as np
import pandas as pd

from utils.cal import Calculation


class Nav:
    """Nav class to handle navigation data from X-plane 11"""
    # https://developer.x-plane.com/docs/data-development-documentation/
    # https://developer.x-plane.com/article/navdata-in-x-plane-11/

    def __init__(self):        
        self.fix = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_fix.dat'), delimiter='\s+', skiprows=3, header=None).values
        """Fixes data https://developer.x-plane.com/wp-content/uploads/2019/01/XP-FIX1101-Spec.pdf"""  

        self.nav = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_nav.dat'), delimiter='\s+', skiprows=3, header=None, names=np.arange(0,18), low_memory=False).values  
        """Radio navigation data https://developer.x-plane.com/wp-content/uploads/2020/03/XP-NAV1150-Spec.pdf"""

        self.airway = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_awy.dat'), delimiter='\s+', skiprows=3, header=None).values
        """Airway data https://developer.x-plane.com/wp-content/uploads/2019/01/XP-AWY1101-Spec.pdf"""

        self.holding = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_hold.dat'), delimiter='\s+', skiprows=3, header=None).values
        """Holding data https://developer.x-plane.com/wp-content/uploads/2018/12/XP-HOLD1140-Spec.pdf"""

        self.min_off_route_alt = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_mora.dat'), delimiter='\s+', skiprows=3, header=None).values
        """Minimum off route grid altitudes https://developer.x-plane.com/wp-content/uploads/2020/03/XP-MORA1150-Spec.pdf"""

        self.min_sector_alt = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_msa.dat'), delimiter='\s+', skiprows=3, header=None, names=np.arange(0,23)).values
        """Minimum sector altitudes for navaids, fixes, airports and runway threshold https://developer.x-plane.com/wp-content/uploads/2020/03/XP-MSA1150-Spec.pdf"""


    def get_fix_coordinate(self, fix, lat, long):
        """
        Get nearest fix corrdinate

        Parameters
        ----------
        fix : String
            Name of the fix (max 5 chars)

        lat :  float
            Latitude

        long :  float
            Longitude

        Returns
        -------
        lat, Long: float, float
            Latitude and Longitude of the fix
        """
        # Find lat and long of all fixes that match the name
        fix_lat = np.extract(self.fix[:,2] == fix, self.fix[:,0]).astype(np.float)
        fix_long = np.extract(self.fix[:,2] == fix, self.fix[:,1]).astype(np.float)
        # Find index of minimum distance
        index = np.argmin(Calculation.cal_great_circle_distance(lat, long, fix_lat, fix_long))
        return fix_lat[index], fix_long[index]


    def get_procedure(self, ICAO):
        """Terminal procedures (SID/STAR/Approach/Runway) https://developer.x-plane.com/wp-content/uploads/2019/01/XP-CIFP1101-Spec.pdf""" 
        procedures = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/CIFP/'+ICAO+'.dat'), delimiter=',|:', header=None).values
 