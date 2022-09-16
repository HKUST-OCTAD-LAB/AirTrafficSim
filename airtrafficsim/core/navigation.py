import numpy as np
import pandas as pd
from pathlib import Path
from zipfile import ZipFile
import csv

from airtrafficsim.utils.calculation import Cal


class Nav:
    """
    Nav class to provide navigation data from x-plane 11.

    Attributes
    ----------
    Nav.fix : pandas.dataframe
        Fixes data https://developer.x-plane.com/wp-content/uploads/2019/01/XP-FIX1101-Spec.pdf

    Nav.nav : pandas.dataframe
        Radio navigation aid data https://developer.x-plane.com/wp-content/uploads/2020/03/XP-NAV1150-Spec.pdf

    Nav.airway : pandas.dataframe
        Airway data https://developer.x-plane.com/wp-content/uploads/2019/01/XP-AWY1101-Spec.pdf

    Nav.holding : pandas.dataframe
        Holding procedures data https://developer.x-plane.com/wp-content/uploads/2018/12/XP-HOLD1140-Spec.pdf

    Nav.min_off_route_alt : pandas.dataframe
        Minimum off route grid altitudes https://developer.x-plane.com/wp-content/uploads/2020/03/XP-MORA1150-Spec.pdf

    Nav.min_sector_alt : pandas.dataframe
        Minimum sector altitudes for navaids, fixes, airports and runway threshold https://developer.x-plane.com/wp-content/uploads/2020/03/XP-MSA1150-Spec.pdf

    Nav.airports : pandas.dataframe
        Airports data (extracted to contain only runway coordinates) https://developer.x-plane.com/article/airport-data-apt-dat-file-format-specification/

    Notes
    -----
    https://developer.x-plane.com/docs/data-development-documentation/

    https://developer.x-plane.com/article/navdata-in-x-plane-11/
    """

    # Install navigation data
    if not Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/').is_dir():
        # Create directories
        Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/airports').mkdir(parents=True)

        # Unzip files
        print("Unzipping X-plane navigation data.")
        ZipFile('data/nav/xplane_default_data.zip').extractall('data/nav/xplane/')

        # Extract apt.dat to runways.csv and individual csv in xplane/airports/
        print("Unpacking airport data (apt.dat). This will take a while...")
        airport = []
        icao = ""
        runways = []
        with open(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/apt.dat'), 'r') as file:
            # Skip 3 lines
            next(file)
            next(file)
            next(file)
            # Loop through all files
            for line in file:
                row = line.split()
                if row:
                    # If row code equals to airport
                    if row[0] in ("1", "16", "17", "99"):
                        # Write previous airport
                        if not icao == "":
                            print("\r"+"Extracting information from airport "+icao, end="", flush=True)
                            with open(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/airports', icao+'.csv'), 'w') as f:
                                f.writelines(airport)
                        # Reset if not the end
                        if not row[0] == "99":
                            icao = row[4]
                            airport = []
                    # If row code equals to land runway
                    if row[0] == "100":
                        if row[0] == "1000":
                            print("\n"+row[0])
                        for i in range(8, len(row), 9):
                            runways.append([icao]+row[i:i+4])
                    # If row code equals to water runway
                    if row[0] == "101":
                        for i in range(3, len(row), 3):
                            runways.append([icao]+row[i:i+4])
                    # If row code equals to helipad runway
                    if row[0] == "102":
                        runways.append([icao]+row[1:5])
                    # Add data line to cache
                    airport.append(line)

        # Write saved runway data to airports.csv
        print("\nExporting airport runways data.")
        with open(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/airports.csv'), 'w') as f:
            writer = csv.writer(f)
            writer.writerows(runways)
        del airport
        del icao
        del runways

    # Static variables
    print("Reading NAV data...")
    fix = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_fix.dat'), delimiter='\s+', skiprows=3, header=None)
    """Fixes data https://developer.x-plane.com/wp-content/uploads/2019/01/XP-FIX1101-Spec.pdf"""
    nav = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_nav.dat'), delimiter='\s+', skiprows=3, header=None, names=np.arange(0,18), low_memory=False).apply(pd.to_numeric, errors='ignore')
    """Radio navigation data https://developer.x-plane.com/wp-content/uploads/2020/03/XP-NAV1150-Spec.pdf"""
    airway = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_awy.dat'), delimiter='\s+', skiprows=3, header=None)
    """Airway data https://developer.x-plane.com/wp-content/uploads/2019/01/XP-AWY1101-Spec.pdf"""
    holding = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_hold.dat'), delimiter='\s+', skiprows=3, header=None)
    """Holding data https://developer.x-plane.com/wp-content/uploads/2018/12/XP-HOLD1140-Spec.pdf"""
    min_off_route_alt = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_mora.dat'), delimiter='\s+', skiprows=3, header=None)
    """Minimum off route grid altitudes https://developer.x-plane.com/wp-content/uploads/2020/03/XP-MORA1150-Spec.pdf"""
    min_sector_alt = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/earth_msa.dat'), delimiter='\s+', skiprows=3, header=None, names=np.arange(0,26))
    """Minimum sector altitudes for navaids, fixes, airports and runway threshold https://developer.x-plane.com/wp-content/uploads/2020/03/XP-MSA1150-Spec.pdf"""
    airports = pd.read_csv(Path(__file__).parent.parent.parent.resolve().joinpath('./data/nav/xplane/airports.csv'), header=None)
    """Airports data (extracted to contain only runway coordinates) https://developer.x-plane.com/article/airport-data-apt-dat-file-format-specification/"""

    @staticmethod
    def get_wp_coord(name, lat, long):
        """
        Get the nearest waypoint (fix and navaid) coordinate given name.

        Parameters
        ----------
        name : String
            ICAO name of the waypoint (max 5 chars)

        lat : float
            Latitude of current position

        long : float
            Longitude of current position

        Returns
        -------
        lat, Long: float, float
            Latitude and Longitude of the waypoint
        """
        # Find lat and long of all fixes that match the name
        mask = Nav.fix[2].to_numpy() == name
        fix_lat = Nav.fix[0].to_numpy()[mask]
        fix_long = Nav.fix[1].to_numpy()[mask]
        # Find lat and long of all navaids that match the name
        mask = Nav.nav[7].to_numpy() == name
        nav_lat = Nav.nav[1].to_numpy()[mask]
        nav_long = Nav.nav[2].to_numpy()[mask]
        # Combine fix and nav
        wp_lat = np.append(fix_lat, nav_lat)
        wp_long = np.append(fix_long, nav_long)
        # Find index of minimum distance
        index = np.argmin(Cal.cal_great_circle_dist(lat, long, wp_lat, wp_long), axis=0)
        return wp_lat[index], wp_long[index]
    
    @staticmethod
    def get_wp_in_area(lat1, long1, lat2, long2):
        """
        Get all waypoints(fix, navaids) within area

        Parameters
        ----------
        lat1 : float
            Latitude 1 of area (South)
        long1 : float
            Longitude 1 of area (West)
        lat2 : float
            Latitude 2 of area (North)
        long2 : float
            Longitude 2 of area (East)

        Returns
        -------
        [lat, long, name] : [float[], float[], string[]]
            [Latitude, Longitude, Name] array of all waypoints in the area
        """
        if lat1 < lat2 and long1 < long2:
            # If normal condition
            fix = Nav.fix[(Nav.fix.iloc[:,0].between(lat1, lat2)) & (Nav.fix.iloc[:,1].between(long1, long2))].iloc[:,0:3].to_numpy()
            nav = Nav.nav[(Nav.nav.iloc[:,1].between(lat1, lat2)) & (Nav.nav.iloc[:,2].between(long1, long2))].iloc[:,[1,2,7]].to_numpy()
        elif lat1 < lat2 and long1 > long2:
            # If long1 = 170 and long2 = -170
            fix = Nav.fix[(Nav.fix.iloc[:,0].between(lat1, lat2)) & (Nav.fix.iloc[:,1].between(long1, 180.0) | Nav.fix.iloc[:,1].between(-180.0, long2))].iloc[:,0:3].to_numpy()
            nav = Nav.nav[(Nav.nav.iloc[:,1].between(lat1, lat2)) & (Nav.nav.iloc[:,2].between(long1, 180.0) | Nav.nav.iloc[:,2].between(-180.0, long2))].iloc[:,[1,2,7]].to_numpy()
        elif lat1 > lat2 and long1 < long2:
            # If lat1 = 80 and lat2 = -80
            fix = Nav.fix[(Nav.fix.iloc[:,0].between(lat1, 90.0) | Nav.fix.iloc[:,0].between(lat1, -90.0)) & (Nav.fix.iloc[:,1].between(long1, long2))].iloc[:,0:3].to_numpy()
            nav = Nav.nav[(Nav.nav.iloc[:,1].between(lat1, 90.0) | Nav.nav.iloc[:,1].between(lat1, -90.0)) & (Nav.nav.iloc[:,2].between(long1, long2))].iloc[:,[1,2,7]].to_numpy()
        else:
            # If lat1 = 80 and lat2 = -80 and if long1 = 170 and long2 = -170
            fix = Nav.fix[(Nav.fix.iloc[:,0].between(lat1, 90.0) | Nav.fix.iloc[:,0].between(lat1, -90.0)) & (Nav.fix.iloc[:,1].between(long1, 180.0) | Nav.fix.iloc[:,1].between(-180.0, long2))].iloc[:,0:3].to_numpy()
            nav = Nav.nav[(Nav.nav.iloc[:,1].between(lat1, 90.0) | Nav.nav.iloc[:,1].between(lat1, -90.0)) & (Nav.nav.iloc[:,2].between(long1, 180.0) | Nav.nav.iloc[:,2].between(-180.0, long2))].iloc[:,[1,2,7]].to_numpy()
        return np.vstack((fix, nav))
    
    @staticmethod
    def get_runway_coord(airport, runway):
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
        airport = Nav.airports[(Nav.airports[0].to_numpy() == airport)]
        return tuple(airport[airport[1].str.contains(runway)].iloc[0,2:5])

    @staticmethod
    def find_closest_airport_runway(lat, long):
        """
        Find the closest runway and airport given lat long.

        Parameters
        ----------
        lat : float
            Latitude
        long : float
            Longitude

        Returns
        -------
        Airport : string
            ICAO code of airport
        Runway : string
            Runway Name
        """
        tmp = Nav.airports[(Nav.airports.iloc[:,2].between(lat-0.1, lat+0.1)) & (Nav.airports.iloc[:,3].between(long-0.1, long+0.1))]
        dist = Cal.cal_great_circle_dist(tmp.iloc[:, 2].to_numpy(), tmp.iloc[:, 3].to_numpy(), lat, long)
        return tmp.iloc[np.argmin(dist)].tolist()

    @staticmethod
    def get_airport_procedures(airport, procedure_type):
        """
        Get instrument procedures of an airport.

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
        Get the details of standard instrument procedure

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

        Returns
        -------
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

        # Assume a lowest alt restriction
        alt_restriction = np.where(np.array(alt_restriction_2) != -1, np.minimum(alt_restriction_1, alt_restriction_2), alt_restriction_1)

        return procedure_df[4].values.tolist(), procedure_df[22].values.tolist(), alt_restriction, procedure_df[26].values.tolist(), speed_restriction

    @staticmethod
    def get_holding_procedure(fix, region):
        """
        Get holding procedure.

        Parameters
        ----------
        fix : string
            Fix name
        region : string
            ICAO region

        Returns
        -------
        [inbound holding course, legtime, leg length, direction, min alt, max alt, speed] : []

        Note
        ----
        https://developer.x-plane.com/wp-content/uploads/2018/12/XP-HOLD1140-Spec.pdf
        """
        holding = Nav.holding[(Nav.holding[1] == region) & (Nav.holding[0] == fix)]
        return holding.iloc[0,:].tolist()


 