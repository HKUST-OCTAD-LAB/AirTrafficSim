"""Navigation database"""
from cProfile import run
import os
import csv
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
    if len(os.listdir(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/'))) <= 1:
        print("Unzipping X-plane navigation data.")
        ZipFile('data/nav/xplane_default_data.zip').extractall('data/nav/xplane/')

        print("Unpacking airport data (apt.dat). This will take a while...")
        airports = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/apt.dat'), delimiter='\s+', skiprows=3, header=None, names=np.arange(0,88), low_memory=False)
        airports = np.split(airports, np.where((airports[0] == 1) | (airports[0] == 16) | (airports[0] == 17))[0])[1:]
        Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/airports').mkdir(parents=True, exist_ok=True)
        writer = csv.writer(open(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/airports.csv'), 'w'))
        for airport in airports:  
            icao = airport.iloc[0,4]
            alt = airport.iloc[0,1]
            airport.to_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/airports', icao+'.csv'))
            # Land runway
            if 100 in airport[0].values:
                tmp = airport[airport[0] == 100].iloc[:, 8:]
                runway = []
                for i, val in tmp.iterrows():
                    runway.append(val[pd.isna(val) == False].values.reshape((-1,9))[:,:3])
                runway = np.concatenate((runway), axis=0)
            # Water runway
            elif 101 in airport[0].values:
                tmp = airport[airport[0] == 101].iloc[:, 3:]
                runway = []
                for i, val in tmp.iterrows():
                    runway.append(val[pd.isna(val) == False].values.reshape((-1,3)))
                runway = np.concatenate((runway), axis=0)
            # Helipad
            elif 102 in airport[0].values:
                runway = airport[airport[0] == 102].iloc[:, 1:4].values

            # Write to airport.csv
            if runway.ndim > 1:
                writer.writerows(np.column_stack((np.full(runway.shape[0], icao), runway, np.full(runway.shape[0], alt))))
            else:
                writer.writerow(np.append(icao, runway, alt))
        
        del airports

    print("Reading NAV data...")
    
    fix = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_fix.dat'), delimiter='\s+', skiprows=3, header=None)
    """Fixes data https://developer.x-plane.com/wp-content/uploads/2019/01/XP-FIX1101-Spec.pdf"""   
    nav = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_nav.dat'), delimiter='\s+', skiprows=3, header=None, names=np.arange(0,18), low_memory=False).apply(pd.to_numeric, errors='ignore')  
    """Radio navigation data https://developer.x-plane.com/wp-content/uploads/2020/03/XP-NAV1150-Spec.pdf"""
    airway = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_awy.dat'), delimiter='\s+', skiprows=3, header=None)
    """Airway data https://developer.x-plane.com/wp-content/uploads/2019/01/XP-AWY1101-Spec.pdf"""
    holding = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_hold.dat'), delimiter='\s+', skiprows=3, header=None)
    """Holding data https://developer.x-plane.com/wp-content/uploads/2018/12/XP-HOLD1140-Spec.pdf"""
    # min_off_route_alt = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_mora.dat'), delimiter='\s+', skiprows=3, header=None)
    # """Minimum off route grid altitudes https://developer.x-plane.com/wp-content/uploads/2020/03/XP-MORA1150-Spec.pdf"""
    # min_sector_alt = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_msa.dat'), delimiter='\s+', skiprows=3, header=None, names=np.arange(0,23))
    # """Minimum sector altitudes for navaids, fixes, airports and runway threshold https://developer.x-plane.com/wp-content/uploads/2020/03/XP-MSA1150-Spec.pdf"""
    airports = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/airports.csv'), header=None)
    """Airports data (extracted to contain only runway coordinates) https://developer.x-plane.com/article/airport-data-apt-dat-file-format-specification/"""

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
        # Find lat and long of all navaids that match the name
        nav_lat = np.extract(Nav.nav.values[:,7] == fix_name, Nav.nav.values[:,1]).astype(np.float)
        nav_long = np.extract(Nav.nav.values[:,7] == fix_name, Nav.nav.values[:,2]).astype(np.float)
        # Combine fix and nav
        wp_lat = np.append(fix_lat, nav_lat)
        wp_long = np.append(fix_long, nav_long)
        # Find index of minimum distance
        index = np.argmin(Calculation.cal_great_circle_distance(lat, long, wp_lat, wp_long))
        return wp_lat[index], wp_long[index]

    
    @staticmethod
    def get_fix_in_area(lat1, long1, lat2, long2):
        """
        Get all fix within area

        Parameters
        ----------
        lat1 : float
            Latitude 1 of area
        long1 : float
            Longitude 1 of area
        lat2 : float
            Latitude 2 of area
        long2 : float
            Longitude 2 of area

        Returns
        -------
        [lat, long, name] : [float[], float[], string[]]
            Latitude, Longitude, Name array of all fixes in the area
        """
        fix = Nav.fix[(Nav.fix.iloc[:,0].between(lat1, lat2)) & (Nav.fix.iloc[:,1].between(long1, long2))].iloc[:,0:3].values
        nav = Nav.nav[(Nav.nav.iloc[:,1].between(lat1, lat2)) & (Nav.nav.iloc[:,2].between(long1, long2))].iloc[:,[1,2,7]].values
        return np.vstack((fix, nav))
    
    @staticmethod
    def get_runway_coordinate(airport, runway):
        """
        Get runway coordinate

        Parameters
        ----------
        airport : string
            ICAO code of the airport

        runway: string
            Runway name (RW07L).

        Returns
        -------
        (lat, Long, alt): (float, float, float)
            Latitude, Longitude, and Altitude of the runway end
        """
        tmp = Nav.airports[(Nav.airports[0] == airport) & (Nav.airports[1].str.contains(runway))]
        return tmp.iloc[0,2], tmp.iloc[0,3], tmp.iloc[0,4]


    @staticmethod
    def find_closest_airport_runway(lat, long):
        """
        Find closest runway and airport given lat long.

        Parameters
        ----------
        lat : float
            Latitude
        long : float
            Longitude
        alt : float
            Altitude

        Returns
        -------
        Airport : string
            ICAO code of airport
        Runway : string
            Runway Name
        """
        tmp = Nav.airports[(Nav.airports.iloc[:,2].between(lat-0.1, lat+0.1)) & (Nav.airports.iloc[:,3].between(long-0.1, long+0.1))]
        dist = Calculation.cal_great_circle_distance(tmp.iloc[:,2], tmp.iloc[:,3], lat, long)
        return tmp.iloc[np.argmin(dist)].tolist()


    @staticmethod
    def get_instrument_procedures(airport, procedure_type):
        """
        Get instrument procedures of a airport.

        Parameters
        ----------
        airport : string
            ICAO code of the airport
        
        procedure_type : string
            Procedure type (SID/STAR/APPCH)

        Returns
        -------
        procedure_names : string []
            Names of all procedures of the airport
        """
        procedures = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/CIFP/'+airport+'.dat'), header=None)
        return procedures[procedures[0].str.contains(procedure_type)][2].unique()



    @staticmethod
    def get_procedure(airport, runway, procedure, appch="", iaf=""):
        """
        Get standard procedure

        Parameters
        ----------
        airport : string
            ICAO code of the airport

        runway: string
            Runway name (RW07L) for SID/STAR.

        procedure : string
            Procedure name of SID/STAR/APPCH (XXXX7A)
            For Approach: ILS = I07C, Localliser = L25L, RNAV = R25LY/Z

        appch : string
            Approach procedure type (A = initial approach, I = ILS, "" = None)

        iaf : string
            Initial approach fix (Please provide when appch = A)

        Return
        ------
        Waypoint names : string []
            Waypoint names array

        Altitude restriction type : float []
            Altitude restriction type (+, =, -)

        Altitude restriction : float []
            Altitude restriction 1 

        Altitude restriction : float []
            Altitude restriction 2

        Speed restriction type : float []
            Speed restriction type (+, =, -)

        Speed restriction : float []
            Speed restriction

        Note
        ----
            Terminal procedures (SID/STAR/Approach/Runway) https://developer.x-plane.com/wp-content/uploads/2019/01/XP-CIFP1101-Spec.pd f
            https://wiki.flightgear.org/User:Www2/XP11_Data_Specification
        """ 
        procedures = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/CIFP/'+airport+'.dat'), header=None)

        if appch == "":
            # SID/STAR
            procedure_df = procedures[(procedures[2] == procedure) & (procedures[3].str.contains(runway))]
            if procedure_df.empty:
                procedure_df = procedures[procedures[2] == procedure]
        elif appch == "A":
            # Initial Approach
            procedure_df = procedures[(procedures[1] == appch) & (procedures[2] == procedure) & (procedures[3] == iaf)]
        elif appch == "I":
            # Final Approach
            procedure_df = procedures[(procedures[1] == appch) & (procedures[2] == procedure)]
        
        # Remove missed approach waypoints
        index = procedure_df[procedure_df[8].str.contains('M')].index
        if len(index) > 0:
            procedure_df=procedure_df.loc[:index[0]-1, :]
            
        alt_restriction_1 = []
        alt_restriction_2 = []
        speed_restriction = []

        for val in procedure_df[23].values:
            if "FL" in val:
                alt_restriction_1.append(float(val.replace("FL", ""))*100.0)
            else:
                if val == "     ":
                    alt_restriction_1.append(-1)
                else:
                    alt_restriction_1.append(float(val))
        
        for val in procedure_df[24].values:
            if "FL" in val:
                alt_restriction_2.append(float(val.replace("FL", ""))*100.0)
            else:
                if val == "     ":
                    alt_restriction_2.append(-1)
                else:
                    alt_restriction_2.append(float(val))
        
        for val in procedure_df[27].values:
                if val == "   ":
                    speed_restriction.append(-1)
                else:
                    speed_restriction.append(float(val))


        return procedure_df[4].values.tolist(), procedure_df[22].values.tolist(), alt_restriction_1, alt_restriction_2, procedure_df[26].values.tolist(), speed_restriction


 