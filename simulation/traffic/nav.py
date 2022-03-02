"""Navigation database"""

from pathlib import Path
import numpy as np

class Nav:
    """Nav class to handle navigation data from X-plane 11"""
    # https://developer.x-plane.com/docs/data-development-documentation/
    # https://developer.x-plane.com/article/navdata-in-x-plane-11/

    def __init__(self):

        self.fix = np.genfromtxt(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_fix.dat'), delimiter=[13,15,7,5,3,8],
                    dtype="f8, f8, U5, U4, U2, i4", names = ['Lat', 'Long', 'ID', 'TMA', 'Region', 'Type'], 
                    autostrip=True, skip_header=3, skip_footer=1)
        """Fixes data https://developer.x-plane.com/wp-content/uploads/2019/01/XP-FIX1101-Spec.pdf"""  
        
        self.nav = np.genfromtxt(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_nav.dat'), 
                usecols=np.arange(1,12), autostrip=True, skip_header=3, skip_footer=1)          #TODO: Some row may have column > 12 (info important?)
        """Radio navigation data https://developer.x-plane.com/wp-content/uploads/2020/03/XP-NAV1150-Spec.pdf"""

        self.airway = np.genfromtxt(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_awy.dat'), 
                dtype="U5, U2, i4, U5, U2, i4, U1, i4, i4, i4, U30", names = ['WP_ID_start', 'Region_start', 'WP_type_start', 'WP_ID_end', 'Region_end', 'WP_type_end', 'Direction', 'High_Low', 'Base_alt', 'Top_alt', 'Names'], 
                autostrip=True, skip_header=3, skip_footer=1)
        """Airway data https://developer.x-plane.com/wp-content/uploads/2019/01/XP-AWY1101-Spec.pdf"""

        self.holding = np.genfromtxt(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_hold.dat'), 
                dtype="U5, U2, U4, i4, f8, f8, f8, U1, i4, i4, i4", names = ['WP_ID', 'Region', 'TMA', 'WP_type', 'Course', 'Time', 'Length', 'Direction', 'Min_alt', 'Max_alt', 'Speed_limit'], 
                autostrip=True, skip_header=3, skip_footer=1)
        """Holding data https://developer.x-plane.com/wp-content/uploads/2018/12/XP-HOLD1140-Spec.pdf"""

        # self.min_off_route_alt = np.genfromtxt(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_mora.dat'),
        #             autostrip=True, skip_header=3, skip_footer=1)
        # """Minimum off route grid altitudes https://developer.x-plane.com/wp-content/uploads/2020/03/XP-MORA1150-Spec.pdf"""

        # TODO: Handle variable column
        # self.min_sector_alt = np.genfromtxt(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_msa.dat'), 
        #         autostrip=True, skip_header=3, skip_footer=1)
        # """Minimum sector altitudes for navaids, fixes, airports and runway threshold https://developer.x-plane.com/wp-content/uploads/2020/03/XP-MSA1150-Spec.pdf"""


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
        fix_lat = np.extract(self.fix['ID'] == fix, self.fix['Lat'])
        fix_long = np.extract(self.fix['ID'] == fix, self.fix['Long'])
        # Find index of minimum distance https://en.wikipedia.org/wiki/Haversine_formula
        index = np.argmin(2.0 * np.arcsin(np.sqrt(np.sin(np.deg2rad(fix_lat - lat)/2.0)**2.0 + np.cos(np.deg2rad(lat)) * np.cos(np.deg2rad(fix_lat)) * np.sin(np.deg2rad(fix_long - long)/2.0)**2.0)))
        return fix_lat[index], fix_long[index]


    def get_procedure(self, ICAO):
        """Terminal procedures (SID/STAR/Approach/Runway) https://developer.x-plane.com/wp-content/uploads/2019/01/XP-CIFP1101-Spec.pdf""" 
        # procedures = np.genfromtxt(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/CIFP/'+ICAO+'.dat'), delimiter=',')
