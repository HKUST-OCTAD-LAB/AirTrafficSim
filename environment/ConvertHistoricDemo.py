from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import numpy as np
import csv

from airtrafficsim.core.environment import Environment
from airtrafficsim.core.aircraft import Aircraft
from airtrafficsim.core.navigation import Nav
from airtrafficsim.utils.enums import APLateralMode, Config, FlightPhase
from airtrafficsim.utils.calculation import Cal
from airtrafficsim.utils.route_detection import rdp, detect_sid_star

class ConvertHistoricDemo(Environment):

    def __init__(self):
        # Initialize environment super class
        super().__init__(file_name = Path(__file__).name.removesuffix('.py'), #File name (do not change)
                        start_time = datetime.fromisoformat('2018-05-01T00:00:00'),
                        end_time = 3600,
                        # end_time = 86400,
                        weather_mode = "",
                        performance_mode = "BADA" 
                        )

        self.historic_data_path = Path(__file__).parent.parent.resolve().joinpath('data/flight_data/2018-05-01/')

        # Detect arrival route, position, and time for all aircraft in a day
        print("Analyzing flight data")
        target = ["KA379","CI919","TG608","CX3293","HX305","CX837","KA951","LX138","KE617","5J112","CX764","KA693","HX265","KA641","7C2107","KA903","KA634","CI601","NH821","CX879","TR974","QF97","AK138","CX178","HX217","CA101","TG600","CI641","HX730","HX221","3V51","KA221","CX391","UO559","KC929","KA637","CX549","CX14","5J240","CX632","UO823","BX391","UO625","KA937","BR857","5X64","CX505","KA495","CX918","KA863","UO707","KA901","LD783","SA286","KA111","MU2901","KA437","UO623","CX798","LD209","EK384","HX61","SQ872","EK9820","CX610","TW117","ZH9091","CI923","KA997","CX654","KA761","HX453","HX146","SQ1","CX738","CV740","KA887","PR312","HX3579","CX53","AI314","EK9882","RS531","UO603","KE603","HX162","QR8404","MU595","CX784","KA343","CX581","5J272","KA811","KA805","CX652","HX693","KA663","3U8617","HX609","MU721","CX831","8K525","CX198","LH8454","VS206","CX252","HX539","CA105","CI927","CI679","CX873","CX439","ZH9095","SQ2","AK239","KA961","FD515","LD217","Z21264","KA621","KA233","CI933","CX912","OZ721","LH796","MF381","HX607","KA455","RH372","KA897","CX618","CX170","KA893","CX728","CX926","CX885","CX234","TG606","KA891","KA732","5J150","CX616","KA875","KA877","AK130","ZH9093","CX465","HX363","KE601","CX716","CX288","CX3273","HX671","C8673","QF29","CX710","UO627","AE1819","CX776","KA153","KA381","HX6353","KA491","CI935","KA905","CX35","KA813","CX908","CX3291","HX762","VN598","RJ182","CX811","CX934","KA311","CX660","AA193","CX110","MU733","CX2091","HX6318","KA871","CX292","AE1831","HX619","CX712","5J110","MM67","SQ868","HX708","HX129","PO956","MU765","CX531","NH811","BR855","TR980","UO871","KA857","HX768","TK70","KA453","SK963","HX6652","QR818","EK386","KA643","GK63","5X4","CI903","BR827","CX595","FM849","HX285","VA87","KA692","CA117","CX851","CX539","CX156","KA841","HX247","FD524","BR809","QR816","CX2099","CX485","PR310","KA603","UO621","LD326","SQ866","CI5821","FD504","CX95","JL735","CX260","CX698","UO227","HX553","KE607","HX313","QF117","TH3507","3S514","CI929","LH730","CX254","KA993","5J114","CX569","CA103","CX754","NZ89","CA411","CX419","HX156","CX807","UO689","9C8921","KA883","5Y8027","KA617","LD129","AK237","UO849","KA265","9C8715","HX81","UO651","KA615","TG602","CX473","KA855","CX55","UO639","HX231","BR6537","AI315","CX415","UO754","GK23","MU505","CX889","QF127","HX629","BR891","FX5392","KA483","AA125","CX3218","9W78","CX407","EY834","KA294","KA457","CA107","HX499","UA179","HX766","HX69","OM297","OZ745","KA795","KA781","CX676","CX881","CX467","KA789","UO647","HX283","CX662","CX411","PO969","KA809","VJ876","CX883","KA703","KA251","3K697","KA943","CX451","MU723","EK380","KA825","CX100","LD842","BA27","SU212","KA397","GA876","CX902","OS67","UO764","CZ3075","CA115","UO674","FD508","CX748","CX463","CX382","FD502","MF8015","OZ969","CX702","PR306","TG638","MH432","HX647","CA419","ZE931","HX780","BR851","CI915","HX28","TR978","HX9486","CI921","UO863","CX694","UA895","MU509","CX650","UO851","MU725","CX708","HX235","CX93","PR300","MU501","CX565","9W76","HX633","UO275","FX9171","KA623","KA831","UO591","KA734","CK263","EK9822","UA869","KL887","QR8424","CX734","UO899","CX845","LD456","CZ310","SQ890","AK136","CX521","MF8017","LD681","AF188","CX354","CX216","UO697","CX369","5J120","CA109","CX714","PG873","KZ203","MM63","BR871","AE1841","CX636","CX138","CX99","CX899","BR6521","KA209","RH569","LD205","CI5835","K4247","KA745","CX403","KA451","CX270","KA213","CX443","GA856","UO687","CX829","ET609","CX331","MH78","LQ970","HX6653","9S275","CX22","CX507","RA409"]
        # Set up arrival data
        arrival_procedures = Nav.get_airport_procedures("VHHH", "STAR")
        # Get all arrival route and related waypoints
        arrival_waypoints = []
        arrivals_dict={}
        for star in arrival_procedures:
            wp = Nav.get_procedure("VHHH", "", star)[0]
            wp = [ele for ele in wp if ele.strip()]
            arrival_waypoints.extend(wp)
            arrivals_dict[star] = wp
        arrival_waypoints = np.unique(arrival_waypoints)
        # Get coordinate of all arrival waypoints
        arrival_waypoints_coord_dict = {}
        for wp in arrival_waypoints:
            coord = Nav.get_wp_coord(wp, 22.3080, 113.9185)
            arrival_waypoints_coord_dict[wp] = list(coord)

        # Set up approach data
        approach_procedures = Nav.get_airport_procedures("VHHH", "APPCH")
        ils = [str for str in approach_procedures if "I" in str]
        ils_runway = [str.replace('I', '') for str in approach_procedures if "I" in str]
        # Runway without ils
        missed_procedure = [] 
        for procedure in approach_procedures:
            hv_runway = [runway for runway in ils_runway if runway in procedure]
            if len(hv_runway) == 0:
                missed_procedure.append(procedure)
        approach_procedures = ils + missed_procedure

        # Get all arrival route and related waypoints
        approach_waypoints = []
        approach_dict={}
        for approach in approach_procedures:
            wp = Nav.get_procedure("VHHH", "", approach)[0]
            wp = [ele for ele in wp if ele.strip() and "RW" not in ele]
            approach_waypoints.extend(wp)
            approach_dict[approach] = wp
        approach_waypoints = np.unique(approach_waypoints)

        # Get coordinate of all arrival waypoints
        approach_waypoints_coord_dict = {}
        for wp in approach_waypoints:
            coord = Nav.get_wp_coord(wp, 22.3080, 113.9185)
            approach_waypoints_coord_dict[wp] = list(coord)

        self.call_sign = []
        self.type = []
        self.star = []
        self.approach = []
        self.position = []
        self.speed = []
        self.start_alt = []
        self.heading = []
        self.time = []
        
        for file in self.historic_data_path.iterdir():
            if file.name.removesuffix('.csv') in target:
                self.call_sign.append(file.name.removesuffix('.csv'))
                
                df = pd.read_csv(file)
                traj = df[['lat', 'long']].to_numpy()
                simplified = np.array(rdp(traj, 0.005))   

                self.type.append(df['Aircraft_model'].iloc[0])

                arrival_result, arrival_trajectory  = detect_sid_star(simplified, arrivals_dict, arrival_waypoints_coord_dict)
                self.star.append(arrival_result)
                
                approach_result, approach_trajectory = detect_sid_star(simplified, approach_dict, approach_waypoints_coord_dict)
                self.approach.append(approach_result)

                index = np.where(Cal.cal_great_circle_dist(traj[:, 0], traj[:, 1], 22.3193, 114.1694) < 150)[0][0]
                self.position.append(traj[index])
                self.speed.append(df['gspeed'].iloc[index])
                self.start_alt.append(df['alt'].iloc[index])
                self.heading.append(df['hangle'].iloc[index])
                self.time.append(df['timestamp'].iloc[index])

                print(file.name.removesuffix('.csv'), arrival_result, approach_result)
        
        print("Finished analyzing data")


        self.aircraft_list = {}
        self.time = np.array(self.time)

        self.start_time = datetime.fromtimestamp(np.min(self.time))


    def should_end(self):
        return False

    def atc_command(self):
        # User algorithm
        time = self.start_time + timedelta(seconds=self.global_time)
        time = int(time.timestamp())
        index = np.where(self.time == time)[0]

        # Add aircraft
        for i in index:
            self.aircraft_list[self.call_sign[i]] = Aircraft(self.traffic, call_sign=self.call_sign[i], aircraft_type=self.type[i], flight_phase=FlightPhase.CRUISE, configuration=Config.CLEAN,
                                                             lat=self.position[i][0], long=self.position[i][1], alt=self.start_alt[i], heading=self.heading[i], cas=self.speed[i], fuel_weight=10000.0, payload_weight=12000.0,
                                                             arrival_airport="VHHH", arrival_runway="07R", star = self.star[i], approach = self.approach[i], cruise_alt=37000)

        # Delete aircraft
        index = self.traffic.index[self.traffic.ap.hv_next_wp == False]
        for i in index:
            self.traffic.del_aircraft(i)

        # Holding and vectoring
        if "TH3507" in self.aircraft_list:
            # self.aircraft_list["TH3507"].set_vectoring(60, 195, "GUAVA")
            if self.global_time == 100:
                self.aircraft_list["TH3507"].set_holding(2, "BETTY", "VH")
        

        