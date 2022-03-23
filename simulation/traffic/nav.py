"""Navigation database"""
import os
from zipfile import ZipFile
from pathlib import Path
import numpy as np
import pandas as pd

from utils.cal import Calculation


class Nav:
    """Nav class to handle navigation data from X-plane 11"""
    # https://developer.x-plane.com/docs/data-development-documentation/
    # https://developer.x-plane.com/article/navdata-in-x-plane-11/
    #         
    if len(os.listdir('data/nav/xplane/')) <= 1:
                print("Unzipping X-plane navigation data.")
                ZipFile('data/nav/xplane_default_data.zip').extractall('data/nav/xplane/')
    
    fix = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_fix.dat'), delimiter='\s+', skiprows=3, header=None)
    """Fixes data https://developer.x-plane.com/wp-content/uploads/2019/01/XP-FIX1101-Spec.pdf"""  
    nav = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_nav.dat'), delimiter='\s+', skiprows=3, header=None, names=np.arange(0,18), low_memory=False)  
    """Radio navigation data https://developer.x-plane.com/wp-content/uploads/2020/03/XP-NAV1150-Spec.pdf"""
    airway = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_awy.dat'), delimiter='\s+', skiprows=3, header=None)
    """Airway data https://developer.x-plane.com/wp-content/uploads/2019/01/XP-AWY1101-Spec.pdf"""
    holding = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_hold.dat'), delimiter='\s+', skiprows=3, header=None)
    """Holding data https://developer.x-plane.com/wp-content/uploads/2018/12/XP-HOLD1140-Spec.pdf"""
    min_off_route_alt = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_mora.dat'), delimiter='\s+', skiprows=3, header=None)
    """Minimum off route grid altitudes https://developer.x-plane.com/wp-content/uploads/2020/03/XP-MORA1150-Spec.pdf"""
    min_sector_alt = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_msa.dat'), delimiter='\s+', skiprows=3, header=None, names=np.arange(0,23))
    """Minimum sector altitudes for navaids, fixes, airports and runway threshold https://developer.x-plane.com/wp-content/uploads/2020/03/XP-MSA1150-Spec.pdf"""


    @staticmethod
    def get_fix_coordinate(fix_name, lat, long):
        """
        Get nearest fix corrdinate

        Parameters
        ----------
        fix_name : String
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
        fix_lat = np.extract(Nav.fix.values[:,2] == fix_name, Nav.fix.values[:,0]).astype(np.float)
        fix_long = np.extract(Nav.fix.values[:,2] == fix_name, Nav.fix.values[:,1]).astype(np.float)
        # Find index of minimum distance
        index = np.argmin(Calculation.cal_great_circle_distance(lat, long, fix_lat, fix_long))
        return fix_lat[index], fix_long[index]

    
    @staticmethod
    def get_fix_in_area(lat1, long1, lat2, long2):
        """
        Get all fix within area

        Parameters
        ----------
        lat1 : float
            Latitude 1 of camera
        long1 : float
            Longitude 1 of camera
        lat2 : float
            Latitude 2 of camera
        long2 : float
            Longitude 2 of camera
        """
        return Nav.fix[(Nav.fix.iloc[:,0].between(lat1, lat2)) & (Nav.fix.iloc[:,1].between(long1, long2))].iloc[:,0:3].values


    @staticmethod
    def get_procedure(ICAO):
        """Terminal procedures (SID/STAR/Approach/Runway) https://developer.x-plane.com/wp-content/uploads/2019/01/XP-CIFP1101-Spec.pdf""" 
        procedures = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/CIFP/'+ICAO+'.dat'), delimiter=',|:', header=None).values
 