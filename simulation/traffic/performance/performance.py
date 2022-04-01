"""Aircraft performance class calculation using BADA 3.15"""
from pathlib import Path
import numpy as np
import os

from utils.enums import AP_speed_mode, Flight_phase, Engine_type, Configuration, Vertical_mode

class Performance:
    """
    Performance class 

    Attributes
    ----------
    See __init__()

    Methods
    -------
    __init__:

    add_aircraft_performance:

    Notes
    -----
    
    """


    def __init__(self, N=1000):
        """
        Initialize BADA performance parameters 

        Parameters
        ----------
        N: int
            Number of aircrafts. Maximum size of performance array (pre-initialize to eliminate inefficient append)
            TODO: Revise the initial estimate
        """
        # ----------------------------  Operations Performance File (OPF) section 3.11 -----------------------------------------
        # Aircraft type
        self.__n_eng = np.zeros([N])
        """Number of engines"""
        self.__engine_type = np.zeros([N])
        """engine type [Engine_type enum]"""
        self.__wake_category = np.zeros([N])                    
        """wake category [Wake_category enum]"""

        # Mass
        self.__m_ref = np.zeros([N])                            
        """reference mass [tones]"""
        self.__m_min = np.zeros([N])                            
        """minimum mass [tones]"""
        self.__m_max = np.zeros([N])                            
        """maximum mass [tones]"""
        self.__m_pyld = np.zeros([N])                           
        """maximum payload mass [tones]"""

        # Flight envelope
        self.__v_mo = np.zeros([N])                             
        """maximum operating speed [knots (CAS)]"""
        self.__m_mo = np.zeros([N])                            
        """maximum operating Mach number [dimensionless]"""
        self.__h_mo = np.zeros([N])                             
        """maximum opearting altitude [feet]"""
        self.__h_max = np.zeros([N])                            
        """maximum altitude at MTOW and ISA [feet]"""
        self.__g_w = np.zeros([N])                              
        """weight gradient on maximum altitude [feet/kg]"""
        self.__g_t = np.zeros([N])                              
        """temperature gradient on maximum altitude [feet/K]"""

        # Aerodynamics
        self.__S = np.zeros([N])                                
        """reference wing surface area [m^2]"""
        self.__c_d0_cr = np.zeros([N])                          
        """parasitic drag coefficient (cruise) [dimensionless]"""
        self.__c_d2_cr = np.zeros([N])                          
        """induced drag coefficient (cruise) [dimensionless]"""
        self.__c_d0_ap = np.zeros([N])                          
        """parasitic drag coefficient (approach) [dimensionless]"""
        self.__c_d2_ap = np.zeros([N])                          
        """induced drag coefficient (approach) [dimensionless]"""
        self.__c_d0_ld = np.zeros([N])                          
        """parasitic drag coefficient (landing) [dimensionless]"""
        self.__c_d2_ld = np.zeros([N])                          
        """induced drag coefficient (landing) [dimensionless]"""
        self.__c_d0_ldg = np.zeros([N])                         
        """parasite darg coefficient (landing gear) [dimensionless]"""
        self.__v_stall_to = np.zeros([N])                       
        """stall speed (TO) [knots (CAS)]"""
        self.__v_stall_ic = np.zeros([N])                       
        """stall speed (IC) [knots (CAS)]"""
        self.__v_stall_cr = np.zeros([N])                       
        """stall speed (CR) [knots (CAS)]"""
        self.__v_stall_ap = np.zeros([N])                       
        """stall speed (AP) [knots (CAS)]"""
        self.__v_stall_ld = np.zeros([N])                       
        """stall speed (LD) [knots (CAS)]"""
        self.__c_lbo = np.zeros([N])                            
        """buffet onset lift coefficient (jet and TBP only) [dimensionless]"""
        self.__k = np.zeros([N])                                
        """buffeting gradient (Jet & TBP only) [dimensionless]"""

        # Engine thrust
        self.__c_tc_1 = np.zeros([N])                           
        """1st maximum climb thrust coefficient [Newton (jet/piston) knot-Newton (turboprop)]"""
        self.__c_tc_2 = np.zeros([N])                           
        """2nd maximum climb thrust coefficient [feet]"""
        self.__c_tc_3 = np.zeros([N])                           
        """3rd maximum climb thrust coefficient [1/feet^2 (jet) Newton (turboprop) knot-Newton (piston)]"""
        self.__c_tc_4 = np.zeros([N])                           
        """1st thrust temperature coefficient [K]"""
        self.__c_tc_5 = np.zeros([N])                           
        """2nd thrust temperature coefficient [1/K]"""
        self.__c_tdes_low = np.zeros([N])                       
        """low altitude descent thrust coefficient [dimensionless]"""
        self.__c_tdes_high = np.zeros([N])                      
        """high altitude descent thrust coefficient [dimensionless]"""
        self.__h_p_des = np.zeros([N])                          
        """transition altitude for calculation of descent thrust [feet]"""
        self.__c_tdes_app = np.zeros([N])                       
        """approach thrust coefficient [dimensionless]"""
        self.__c_tdes_ld = np.zeros([N])                        
        """landing thrust coefficient [dimensionless]"""
        self.__v_des_ref = np.zeros([N])                        
        """reference descent speed [knots (CAS)]"""
        self.__m_des_ref = np.zeros([N])                        
        """reference descent Mach number [dimensionless]"""

        # Fuel flow
        self.__c_f1 = np.zeros([N])                             
        """1st thrust specific fuel consumption coefficient [kg/(min*kN) (jet) kg/(min*kN*knot) (turboprop) kg/min (piston)]"""
        self.__c_f2 = np.zeros([N])                             
        """2nd thrust specific fuel consumption coefficient [knots]"""
        self.__c_f3 = np.zeros([N])                             
        """1st descent fuel flow coefficient [kg/min]"""
        self.__c_f4 = np.zeros([N])                             
        """2nd descent fuel flow coefficient [feet]"""
        self.__c_fcr = np.zeros([N])                            
        """cruise fuel flow correction coefficient [dimensionless]"""

        # Ground movement
        self.__tol = np.zeros([N])                              
        """take-off length [m]"""
        self.__ldl = np.zeros([N])                              
        """landing length [m]"""
        self.__span = np.zeros([N])                             
        """wingspan [m]"""
        self.__length = np.zeros([N])                           
        """length [m]"""


        # ----------------------------  Airline Procedure Models (APF) section 4 -----------------------------------------
        # Climb
        self.__v_cl_1 = np.zeros([N])                           
        """standard climb CAS [knots] between 1,500/6,000 and 10,000 ft"""
        self.__v_cl_2 = np.zeros([N])                           
        """standard climb CAS [knots] between 10,000 ft and Mach transition altitude"""
        self.__m_cl = np.zeros([N])                             
        """standard climb Mach number above Mach transition altitude"""

        # Cruise
        self.__v_cr_1 = np.zeros([N])                           
        """standard cruise CAS [knots] between 3,000 and 10,000 ft"""
        self.__v_cr_2 = np.zeros([N])                           
        """standard cruise CAS [knots] between 10,000 ft and Mach transition altitude"""
        self.__m_cr = np.zeros([N])                             
        """standard cruise Mach number above Mach transition altitude"""

        # Descent
        self.__v_des_1 = np.zeros([N])                          
        """standard descent CAS [knots] between 3,000/6,000 and 10,000 ft"""
        self.__v_des_2 = np.zeros([N])                          
        """standard descent CAS [knots] between 10,000 ft and Mach transition altitude"""
        self.__m_des = np.zeros([N])                            
        """standard descent Mach number above Mach transition altitude"""

        # Speed schedule
        self.__climb_schedule = np.zeros([N, 8])                
        """Standard climb CAS schedule [knots*8] (section 4.1)"""
        self.__cruise_schedule = np.zeros([N, 5])
        """Standard cruise CAS schedule [knots*5] (section 4.2)"""
        self.__descent_schedule = np.zeros([N,8])
        """Standard descent CAS schedule [knots*8] (section 4.3)"""


        # ----------------------------  Global Aircraft Parameters (GPF) section 5 -----------------------------------------
        # Read data from GPF file (section 6.8)
        # 'CD', 1X, A15, 1X, A7, 1X, A16, 1x, A29, 1X, E10.5
        if Path(__file__).parent.parent.parent.parent.resolve().joinpath('./data/BADA/BADA.GPF').is_file():
            GPF = np.genfromtxt(Path(__file__).parent.parent.parent.parent.resolve().joinpath('./data/BADA/BADA.GPF'), delimiter=[3,16,8,17,29,12], dtype="U2,U15,U7,U16,U29,f8", comments="CC", autostrip=True, skip_footer=1)

             # Maximum acceleration
            self.__A_L_MAX_CIV = GPF[0][5]                          
            """Maximum longitudinal acceleration for civil flights [2 ft/s^2]"""
            self.__A_N_MAX_CIV = GPF[1][5]                          
            """Maximum normal acceleration for civil flights [5 ft/s^2]"""

            # Bank angles
            self.__PHI_NORM_CIV_TOLD = GPF[2][5]                    
            """Nominal bank angles fpr civil flight during TO and LD [15 deg]"""
            self.__PHI_NORM_CIV_OTHERS = GPF[3][5]                  
            """Nominal bank angles for civil flight during all other phases [30 deg]"""
            self.__PHI_NORM_MIL = GPF[4][5]                         
            """Nominal bank angles for military flight (all phases) [50 deg]"""
            self.__PHI_MAX_CIV_TOLD = GPF[5][5]                     
            """Maximum bank angles for civil flight during TO and LD [25 deg]"""
            self.__PHI_MAX_CIV_HOLD = GPF[6][5]                     
            """Maximum bank angles for civil flight during HOLD [35 deg]"""
            self.__PHI_MAX_CIV_OTHERS = GPF[7][5]                   
            """Maximum bank angles for civil flight during all other phases [45 deg]"""
            self.__PHI_MAX_MIL = GPF[8][5]                          
            """Maximum bank angles for military flight (all phases) [70 deg]"""

            # Expedited descent (drag multiplication factor during expedited descent to simulate use of spoilers)
            self.__C_DES_EXP = GPF[9][5]                            
            """Expedited descent factor [1.6]"""

            # Thrust factors
            self.__C_TCR = GPF[11][5]                               
            """Maximum cruise thrust coefficient [0.95] (postition different between GPF and user menu)"""
            self.__C_TH_TO = GPF[10][5]                             
            """Take-off thrust coefficient [1.2] (no longer used since BADA 3.0) (postition different between GPF and user menu)"""

            # Configuration altitude threshold
            self.__H_MAX_TO = GPF[12][5]                            
            """Maximum altitude threshold for take-off [400 ft]"""
            self.__H_MAX_IC = GPF[13][5]                            
            """Maximum altitude threshold for initial climb [2,000 ft]"""
            self.__H_MAX_AP = GPF[14][5]                            
            """Maximum altitude threshold for approach [8,000 ft]"""
            self.__H_MAX_LD = GPF[15][5]                            
            """Maximum altitude threshold for landing [3,000 ft]"""

            # Minimum speed coefficient
            self.__C_V_MIN = GPF[16][5]                             
            """Minimum speed coefficient (all other phases) [1.3]"""
            self.__C_V_MIN_TO = GPF[17][5]                          
            """Minimum speed coefficient for take-off [1.2]"""

            # Speed schedules
            self.__V_D_CL_1 = GPF[18][5]                            
            """Climb speed increment below 1,500 ft (jet) [5 knot CAS]"""
            self.__V_D_CL_2 = GPF[19][5]                            
            """Climb speed increment below 3,000 ft (jet) [10 knot CAS]"""
            self.__V_D_CL_3 = GPF[20][5]                            
            """Climb speed increment below 4,000 ft (jet) [30 knot CAS]"""
            self.__V_D_CL_4 = GPF[21][5]                            
            """Climb speed increment below 5,000 ft (jet) [60 knot CAS]"""
            self.__V_D_CL_5 = GPF[22][5]                            
            """Climb speed increment below 6,000 ft (jet) [80 knot CAS]"""
            self.__V_D_CL_6 = GPF[23][5]                            
            """Climb speed increment below 500 ft (turbo/piston) [20 knot CAS]"""
            self.__V_D_CL_7 = GPF[24][5]                            
            """Climb speed increment below 1,000 ft (turbo/piston) [30 knot CAS]"""
            self.__V_D_CL_8 = GPF[25][5]                            
            """ Climb speed increment below 1,500 ft (turbo/piston) [35 knot CAS]"""
            self.__V_D_DSE_1 = GPF[26][5]                           
            """Descent speed increment below 1,000 ft (jet/turboprop) [5 knot CAS]"""
            self.__V_D_DSE_2 = GPF[27][5]                           
            """Descent speed increment below 1,500 ft (jet/turboprop) [10 knot CAS]"""
            self.__V_D_DSE_3 = GPF[28][5]                           
            """Descent speed increment below 2,000 ft (jet/turboprop) [20 knot CAS]"""
            self.__V_D_DSE_4 = GPF[29][5]                           
            """Descent speed increment below 3,000 ft (jet/turboprop) [50 knot CAS]"""
            self.__V_D_DSE_5 = GPF[30][5]                           
            """Descent speed increment below 500 ft (piston) [5 knot CAS]"""
            self.__V_D_DSE_6 = GPF[31][5]                           
            """Descent speed increment below 1,000 ft (piston) [10 knot CAS]"""
            self.__V_D_DSE_7 = GPF[32][5]                           
            """Descent speed increment below 1,500 ft (piston) [20 knot CAS]"""

            # Holding speeds
            self.__V_HOLD_1 = GPF[33][5]                            
            """Holding speed below FL140 [230 knot CAS]"""
            self.__V_HOLD_2 = GPF[34][5]                            
            """Holding speed between FL140 and FL220 [240 knot CAS]"""
            self.__V_HOLD_3 = GPF[35][5]                            
            """Holding speed between FL220 and FL340 [265 knot CAS]"""
            self.__V_HOLD_4 = GPF[36][5]                            
            """Holding speed above FL340 [0.83 Mach]"""
            
            # Ground speed
            self.__V_BACKTRACK = GPF[37][5]                         
            """Runway backtrack speed [35 knot CAS]"""
            self.__V_TAXI = GPF[38][5]                              
            """Taxi speed [15 knot CAS]"""
            self.__V_APRON = GPF[39][5]                             
            """Apron speed [10 knot CAS]"""
            self.__V_GATE = GPF[40][5]                              
            """Gate speed [5 knot CAS]"""

            # Reduced power coefficient
            self.__C_RED_TURBO = GPF[42][5]                         
            """Maximum reduction in power for turboprops [0.25] (postition different between GPF and user menu)"""
            self.__C_RED_PISTON = GPF[41][5]                        
            """Maximum reduction in power for pistons [0.0] (postition different between GPF and user menu)"""
            self.__C_RED_JET = GPF[43][5]                           
            """Maximum reduction in power for jets [0.15]"""

            # Delete variable to free memory
            del GPF

        else: 
            print("BADA.GPF File does not exit")


        # ----------------------------  Atmosphere model section 3.1 -----------------------------------------
        # MSL Standard atmosphere condition (section 3.1.1)
        self.__T_0 = 288.15                                     
        """Standard atmospheric temperature at MSL [K]"""
        self.__P_0 = 101325                                     
        """Standard atmospheric pressure at MSL [Pa]"""
        self.__RHO_0 = 1.225                                    
        """Standard atmospheric density at MSL [kg/m^3]"""
        self.__A_0 = 340.294                                    
        """Speed of sound [m/s]"""

        # Expression (section 3.1.2)
        self.__KAPPA = 1.4                                      
        """Adiabatic index of air [dimensionless]"""
        self.__R = 287.05287                                    
        """Real gas constant of air [m^2/(K*s^2)]"""
        self.__G_0 = 9.80665                                    
        """Gravitational acceleration [m/s^2]"""
        self.__BETA_T_BELOW_TROP = -0.0065                      
        """ISA temperature gradient with altitude below the tropopause [K/m]"""

        # Tropopause (separation between troposphere (below) and stratosphere (above))
        self.__H_P_TROP = 11000                                 
        """Geopotential pressure altitude [m]"""


        # ----------------------------  SYNONYM FILE FORMAT (SYNONYM.NEW) section 6.3 -----------------------------------------
        # | 'CD' | SUPPORT TYPE (-/*) | AIRCRAFT Code | MANUFACTURER | NAME OR MODEL | FILE NAME | ICAO (Y/N) |
        self.__SYNONYM = np.genfromtxt(Path(__file__).parent.parent.parent.parent.resolve().joinpath('./data/BADA/SYNONYM.NEW'), delimiter=[3,2,7,20,25,8,5], names=['CD','ST','ACCODE','MANUFACTURER','MODEL','FILENAME','ICAO'], dtype="U2,U1,U4,U18,U25,U6,U1", comments="CC", autostrip=True, skip_footer=1, encoding= 'unicode_escape')


    def add_aircraft(self, icao, n, mass_class=2):
        """
        Add one specific aircraft performance data to the performance array according to index.

        Parameters
        ----------
        self: Performance class instance
            Used to add data to the performance array.

        ICAO: string
            ICAO code of the specific aircraft.

        n: int
            Index of array.

        mass_class: int
            Aircraft mass for specific flight. To be used for APF. 1 = LO, 2 = AV, 3 = HI TODO: useful?

        Returns
        -------
        TODO:
        """

        # Get file name by searching in SYNONYM.NEW
        row = np.where(self.__SYNONYM['ACCODE'] == icao)[0][0]      # Get row index
        file_name = self.__SYNONYM[row][5]

        if(not file_name):
            print("No aircraft in SYNONYM.NEW")

        # Get data from Operations Performance File (Section 6.4)
        OPF = np.genfromtxt(Path(__file__).parent.parent.parent.parent.resolve().joinpath('./data/BADA/', file_name+'.OPF'), delimiter=[3,2,2,13,13,13,13,11], dtype="U2,U1,U2,f8,f8,f8,f8,f8", comments="CC", autostrip=True, skip_header=16, skip_footer=1)

        # 'CD', 3X, A6, 9X, I1, 12X, A9, 17X, A1 - aircraft type block - 1 data line
        # | 'CD' | ICAO | # of engine | 'engines' | engine type ( Jet,  Turboprop  or  Piston) | wake category ( J (jumbo), H (heavy), M (medium) or L (light))
        OPF_Actype = np.genfromtxt(Path(__file__).parent.parent.parent.parent.resolve().joinpath('./data/BADA/', file_name+'.OPF'), delimiter=[5,15,1,12,26,1], dtype="U2,U6,i1,U7,U9,U1", comments="CC", autostrip=True, max_rows=1)
        self.__n_eng[n] = OPF_Actype.item()[2]
        self.__engine_type[n] = {'Jet':1, 'Turboprop':2, 'Piston':3}.get(OPF_Actype.item()[4])
        self.__wake_category[n] = {'J': 1, 'H':2, 'M':3, 'L': 4}.get(OPF_Actype.item()[5])
        
        # 'CD', 2X, 5 (3X, E10.5) - mass block - 1 data line
        self.__m_ref[n] = OPF[0][3]
        self.__m_min[n] = OPF[0][4]
        self.__m_max[n] = OPF[0][5]
        self.__m_pyld[n] = OPF[0][6]
        self.__g_w[n] = OPF[0][7]

        # 'CD', 2X, 5 (3X, E10.5) - flight envelope block - 1 data line
        self.__v_mo[n] = OPF[1][3]
        self.__m_mo[n] = OPF[1][4]
        self.__h_mo[n] = OPF[1][5]
        self.__h_max[n] = OPF[1][6]
        self.__g_t[n] = OPF[1][7]

        # 'CD', 2X, 4 (3X, E10.5) - aerodynamic block - 12 data lines
        self.__S[n] = OPF[2][3]
        self.__c_lbo[n] = OPF[2][4]
        self.__k[n] = OPF[2][5]
        # __c_m16 is removed from drag expression

        self.__v_stall_cr[n] = OPF[3][4]
        self.__c_d0_cr[n] = OPF[3][5]
        self.__c_d2_cr[n] = OPF[3][6]

        self.__v_stall_ic[n] = OPF[4][4] 
        # self.__c_d0_ic[n] = OPF[3][5]     TODO: Initial climb not used?
        # self.__c_d2_ic[n] = OPF[3][6]     TODO: Initial climb not used?

        self.__v_stall_to[n] = OPF[5][4]
        # self.__c_d0_to[n] = OPF[5][5]     TODO: Initial climb not used?
        # self.__c_d2_to[n] = OPF[5][6]     TODO: Initial climb not used?

        self.__v_stall_ap[n] = OPF[6][4]
        self.__c_d0_ap[n] = OPF[6][5]
        self.__c_d2_ap[n] = OPF[6][6]

        self.__v_stall_ld[n] = OPF[7][4]
        self.__c_d0_ld[n] = OPF[7][5]
        self.__c_d2_ld[n] = OPF[7][6]

        self.__c_d0_ldg[n] = OPF[11][5]

        # 'CD', 2X, 5 (3X, E10.5) - engine thrust block - 3 data lines
        self.__c_tc_1[n] = OPF[14][3]
        self.__c_tc_2[n] = OPF[14][4]
        self.__c_tc_3[n] = OPF[14][5]
        self.__c_tc_4[n] = OPF[14][6]
        self.__c_tc_5[n] = OPF[14][7]

        self.__c_tdes_low[n] = OPF[15][3]
        self.__c_tdes_high[n] = OPF[15][4]
        self.__h_p_des[n] = OPF[15][5]
        self.__c_tdes_app[n] = OPF[15][6]
        self.__c_tdes_ld[n] = OPF[15][7]

        self.__v_des_ref[n] = OPF[16][3]
        self.__m_des_ref[n] = OPF[16][4]

        # 'CD', 2X, 2 (3X, E10.5) - fuel consumption block - 3 data lines
        self.__c_f1[n] = OPF[17][3]
        self.__c_f2[n] = OPF[17][4]

        self.__c_f3[n] = OPF[18][3]
        self.__c_f4[n] = OPF[18][4]

        self.__c_fcr[n] = OPF[19][3]
        
        # 'CD', 2X, 4 (3X, E10.5) - ground movement block - 1 data line
        self.__tol[n] = OPF[20][3]
        self.__ldl[n] = OPF[20][4]
        self.__span[n] = OPF[20][5]
        self.__length[n] = OPF[20][6]

        # Delete variable to free memory
        del OPF_Actype
        del OPF

        # Get data from Airlines Procedures File (Section 6.5)
        # 'CD', 25X, 2(I3, 1X), I2, 10X, 2(Ix, 1X), I2, 2X, I2, 2(1X, I3) - procedures specification block - 3 dataline
        APF = np.genfromtxt(Path(__file__).parent.parent.parent.parent.resolve().joinpath('./data/BADA/', file_name+'.APF'), delimiter=[6,8,9,4,4,4,3,5,4,4,4,4,3,4,4,5,4,4,4,5,7], dtype="U2,U7,U7,U2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,U6", comments="CC", autostrip=True)
        self.__v_cl_1[n] = APF[mass_class][4]
        self.__v_cl_2[n] = APF[mass_class][5]
        self.__m_cl[n] = APF[mass_class][6]/100
        self.__v_cr_1[n] = APF[mass_class][9]
        self.__v_cr_2[n] = APF[mass_class][10]
        self.__m_cr[n] = APF[mass_class][11]/100
        self.__m_des[n] = APF[mass_class][12]/100
        self.__v_des_2[n] = APF[mass_class][13]
        self.__v_des_1[n] = APF[mass_class][14]

        # Delete variable to free memory
        del APF


    def del_aircraft(self, n):
        """
        Delete one specific aircraft performance data to the performance array according to index. This is done by setting all parameters to 0 for reuse in future.

        Parameters
        ----------
        self: Performance class instance
            Used to delete data to the performance array.

        n: int
            Index of array.

        Returns
        -------
        TODO:
        """
        self.__m_ref[n] = 0
        self.__m_min[n] = 0
        self.__m_max[n] = 0
        self.__m_pyld[n] = 0
        self.__g_w[n] = 0
        self.__v_mo[n] = 0
        self.__m_mo[n] = 0
        self.__h_mo[n] = 0
        self.__h_max[n] = 0
        self.__g_t[n] = 0
        self.__S[n] = 0
        self.__c_lbo[n] = 0
        self.__k[n] = 0
        # __c_m16 is removed from drag expression
        self.__v_stall_cr[n] = 0
        self.__c_d0_cr[n] = 0
        self.__c_d2_cr[n] = 0
        self.__v_stall_ic[n] = 0.
        # self.__c_d0_ic[n] = 0.0           TODO: Initial climb not used?
        # self.__c_d2_ic[n] = 0.0           TODO: Initial climb not used?
        self.__v_stall_to[n] = 0
        # self.__c_d0_to[n] = 0.0           TODO: Initial climb not used?
        # self.__c_d2_to[n] = 0.0           TODO: Initial climb not used?
        self.__v_stall_ap[n] = 0
        self.__c_d0_ap[n] = 0
        self.__c_d2_ap[n] = 0
        self.__v_stall_ld[n] = 0
        self.__c_d0_ld[n] = 0
        self.__c_d2_ld[n] = 0
        self.__c_d0_ldg[n] = 0
        self.__c_tc_1[n] = 0
        self.__c_tc_2[n] = 0
        self.__c_tc_3[n] = 0
        self.__c_tc_4[n] = 0
        self.__c_tc_5[n] = 0
        self.__c_tdes_low[n] = 0
        self.__c_tdes_high[n] = 0
        self.__h_p_des[n] = 0
        self.__c_tdes_app[n] = 0
        self.__c_tdes_ld[n] = 0
        self.__v_des_ref[n] = 0
        self.__m_des_ref[n] = 0
        self.__c_f1[n] = 0
        self.__c_f2[n] = 0
        self.__c_f3[n] = 0
        self.__c_f4[n] = 0
        self.__c_fcr[n] = 0
        self.__tol[n] = 0
        self.__ldl[n] = 0
        self.__span[n] = 0
        self.__length[n] = 0
        self.__v_cl_1[n] = 0
        self.__v_cl_2[n] = 0
        self.__m_cl[n] = 0
        self.__v_cr_1[n] = 0
        self.__v_cr_2[n] = 0
        self.__m_cr[n] = 0
        self.__m_des[n] = 0
        self.__v_des_2[n] = 0
        self.__v_des_1[n] = 0


    def update_fuel(self, flight_phase, tas, thrust, alt):
        """
        Calculate fuel burn

        Parameters
        ----------
        flight_phase : float[]
            Flight phase from Traffic class [Flight_phase enum]
        tas : float[]
            True airspeed [kt]
        thrust : float[]
            Thrust [N]
        alt : _type_
            Altitude [ft]

        Returns
        -------
        Fuel burn : float[]
            Fuel burn [kg/s]

        TODO: Thrust mode -> idle descent
        """
        a = self.__cal_nominal_fuel_flow(tas, thrust)/60.0
        return np.select(
                condlist=[
                        flight_phase == Flight_phase.CRUISE,
                        flight_phase == Flight_phase.DESCENT,
                        flight_phase == Flight_phase.APPROACH,
                        flight_phase == Flight_phase.LANDING
                        ], 
                choicelist=[
                        self.__cal_cruise_fuel_flow(tas, thrust)/60000.0,                      # cruise
                        self.__cal_minimum_fuel_flow(alt)/60000.0,                             # Idle descent
                        self.__cal_approach_landing_fuel_flow(tas, thrust, alt)/60000.0,       # Approach
                        self.__cal_approach_landing_fuel_flow(tas, thrust, alt/60000.0)        # Landing
                        ],                                 
                default=self.__cal_nominal_fuel_flow(tas, thrust)/60000.0                      # Others
            )

    
    def cal_thrust(self, vertical_mode, configuration, H_p, V_tas, d_T, drag, ap_speed_mode):
        """
        Calculate thrust given flight phases.

        Parameters
        ----------
        vertical_mode : float[]
            Vertical mode from Traffic class [Vertical_mode enum]

        configuration : float[] 
            Configuration from Traffic class [Configuration enum]

         H_p : float[]
            Geopotential pressuer altitude [ft]

        V_tas : float[]
            True airspeed [kt]

        d_T : float[]
            Temperature differential from ISA [K]_

        drag : float[]
            Drag forces [N]

        ap_speed_mode : AP_speed_mode enum []
            Autopilot speed mode [1: Constant CAS, 2: Constant Mach, 3: Acceleration, 4: Deceleration]

        Returns
        -------
        _type_
            _description_
        """
        return np.select(
                    condlist=[
                            (vertical_mode == Vertical_mode.CLIMB) | ((vertical_mode == Vertical_mode.LEVEL) & (ap_speed_mode == AP_speed_mode.ACCELERATE)),
                            (vertical_mode == Vertical_mode.LEVEL) & ((ap_speed_mode == AP_speed_mode.CONSTANT_CAS) | (ap_speed_mode == AP_speed_mode.CONSTANT_MACH)),
                            (vertical_mode == Vertical_mode.DESCENT) | ((vertical_mode == Vertical_mode.LEVEL) & (ap_speed_mode == AP_speed_mode.DECELERATE))],
                    choicelist=[
                        self.__cal_max_climb_to_thrust(H_p, V_tas, d_T),                                                       
                        np.minimum(drag, self.__cal_max_cruise_thrust(self.__cal_max_climb_to_thrust(H_p, V_tas, d_T))),         #max climb thrust when acceleration, T = D at cruise, but limited at max cruise thrust
                        self.__cal_descent_thrust(H_p, self.__cal_max_climb_to_thrust(H_p, V_tas, d_T), configuration)])


    # -----------------------------------------------------------------------------------------------------
    # ----------------------------- BADA Implementation----------------------------------------------------
    # -----------------------------------------------------------------------------------------------------


    # ----------------------------  Atmosphere model section 3.1 -----------------------------------------
    def cal_temperature(self, H_p, d_T):
        """
        Calculate Temperature (Equation 3.1-12~16)

        Parameters
        ----------
        H_p: float[]
            Geopotential pressuer altitude [m]

        d_T: float[]
            Temperature differential at MSL [K]

        Returns
        -------
        T_< if below tropopause: float[]
            Temperature [K]

        T_trop or T_> if equal to or above tropopause: float[]
            Temperature [K]
        """
        return np.where(H_p < self.__H_P_TROP,
                        # If below Geopotential pressure altitude of tropopause
                        self.__T_0 + d_T + self.__BETA_T_BELOW_TROP * H_p,
                        # If equal or above Geopotential pressure altitude of tropopause
                        self.__T_0 + d_T + self.__BETA_T_BELOW_TROP * self.__H_P_TROP)

    
    def cal_air_pressure(self, H_p, T, d_T):
        """
        Calculate Air Pressure (Equation 3.1-17~20)

        Parameters
        ----------
        H_p: float[]
            Geopotential pressuer altitude [m]

        T: float[]
            Temperature from cal_temperature()[K]

        d_T: float[]
            Temperature differential at MSL [K]

        Returns
        -------
        p_< or p_trop if below or equal to tropopause: float[]
            Pressure [Pa]

        p_> if above tropopause: float[]
            Pressure [Pa]
        """
        return np.where(H_p <= self.__H_P_TROP,
                        # If below or equal Geopotential pressure altitude of tropopause (Equation 3.1-18)
                        self.__P_0 * np.power((T - d_T) / self.__T_0, -self.__G_0/(self.__BETA_T_BELOW_TROP * self.__R)),
                        # If above Geopotential pressure altitude of tropopause (Equation 3.1-20)
                        self.__P_0 * np.power((self.cal_temperature(self.__H_P_TROP, d_T) - d_T) / self.__T_0, -self.__G_0/(self.__BETA_T_BELOW_TROP * self.__R)) \
                            * np.exp(-self.__G_0/(self.__R * self.cal_temperature(self.__H_P_TROP, 0.0)) * (H_p - self.__H_P_TROP))
                        )

    
    def cal_air_density(self, p, T):
        """
        Calculate Air Density (Equation 3.1-21)

        Parameters
        ----------
        p: float[]
            Pressure [Pa]

        T: float[]
            Temperature [K]
        
        Returns
        -------
        rho: float[]
            Density [kg/m^3]
        """
        return p / (self.__R * T)

    
    def cal_speed_of_sound(self, T):
        """
        Calculate speed of sound. (Equation 3.1-22)

        Parameters
        ----------
        T: float[]
            Temperature [K]

        Returns
        -------
        a: float[]
            Speed of sound [m/s]
        """
        return np.sqrt(self.__KAPPA * self.__R * T)

    
    def cas_to_tas(self, V_cas, p, rho):
        """
        Convert Calibrated air speed to True air speed. (Equation 3.1-23)

        Parameters
        ----------
        V_cas: float[]
            Calibrated air speed [m/s]

        p: float[]
            Pressure [Pa] 

        rho: float[]
            Density [kg/m^3]
        
        Returns
        -------
        V_tas : float[]
            True air speed [m/s]
        """
        mu = (self.__KAPPA - 1)/ self.__KAPPA
        return np.power(2.0/mu * p/rho * (np.power(1.0 + self.__P_0/p * (np.power(1.0 + mu/2.0 * self.__RHO_0/self.__P_0 * np.square(V_cas), 1.0/mu) -1), mu)-1), 0.5)


    def tas_to_cas(self, V_tas, p, rho):
        """
        Convert True air speed to Calibrated air speed. (Equation 3.1-24)

        Parameters
        ----------
        V_tas: float[]
            True air speed [m/s]

        p: float[]
            Pressure [Pa] 

        rho: float[]
            Density [kg/m^3]
        
        Returns
        -------
        V_cas : float[]
            Calibrated air speed [m/s]
        """
        mu = (self.__KAPPA - 1)/ self.__KAPPA
        return np.power(2/mu * self.__P_0/self.__RHO_0 * (np.power(1.0 + p/self.__P_0 * (np.power(1 + mu/2 * rho/p * np.square(V_tas), 1.0/mu) - 1.0), mu) - 1.0), 0.5)


    def mach_to_tas(self, M, T):
        """
        Convert Mach number to True Air speed (Equation 3.1-26)

        Parameters
        ----------
        M: float[]
            Mach number [dimensionless]

        T: float[]
            Temperature [K]

        Returns
        -------
        V_tas: float[]
            True air speed [m/s]
        """
        return M * np.sqrt(self.__KAPPA * self.__R * T)


    def tas_to_mach(self, V_tas, T):
        """
        Convert True Air speed to Mach number (Equation 3.1-26)

        Parameters
        ----------
        V_tas: float[]
            True air speed [m/s]

        T: float[]
            Temperature [K]

        Returns
        -------
        M: float[]
            Mach number [dimensionless]
        """
        return V_tas / np.sqrt(self.__KAPPA * self.__R * T)

    
    def cal_transition_alt(self, V_cas, M, d_T):
        """
        Calculate Mach/CAS transition altitude. (Equation 3.1-27~28)

        Parameters
        ----------
        V_cas: float[]
            Calibrated air speed [m/s]

        M: float[]
            Mach number [dimensionless]

        d_T: float[]
            Temperature differential at MSL [K]

        Returns
        -------
        H_p_trans: float[]
            Transition altitude [m]

        Note
        ----
        Transition altitude is defined to be the geopotential pressure altitude at which V_CAS and M represent the same TAS value.
        """
        p_trans = self.__P_0 * (np.power(1.0 + (self.__KAPPA-1.0)/2.0 * np.square(V_cas/self.__A_0), self.__KAPPA/(self.__KAPPA-1.0)) - 1.0) \
                    / (np.power(1.0 + (self.__KAPPA-1.0)/2.0 * np.square(M), self.__KAPPA/(self.__KAPPA-1.0)) - 1.0)       #Equation 3.1-28
        p_trop = self.cal_air_pressure(self.__H_P_TROP, self.cal_temperature(self.__H_P_TROP, d_T),d_T)

        return np.where(p_trans >= p_trop,
                # If __p_trans >= __p_trop
                self.__T_0/self.__BETA_T_BELOW_TROP * (np.power(p_trans/self.__P_0, -self.__BETA_T_BELOW_TROP*self.__R/self.__G_0) - 1.0),
                # __p_trans < __p_trop
                self.__H_P_TROP - self.__R*self.cal_temperature(self.__H_P_TROP,0.0)/self.__G_0 * np.log(p_trans/p_trop))


    # ----------------------------  Total-Energy Model Section 3.2 -----------------------------------------
    def cal_energy_share_factor(self, H_p, T, d_T, M, ap_speed_mode, vertical_mode):
        """
        Calculate energy share factor (Equation 3.2-5, 8~11)

        Parameters
        ----------
        H_p: float[]
            Geopotential pressuer altitude [m]

        T: float[]
            Temperature [K]

        d_T: float[]
            Temperature differential at MSL [K]

        M: float[]
            Mach number [dimensionless]

        ap_speed_mode: float[]
            Speed mode from Autopilot class [AP_speed_mode enum]

        vertical_mode: float[]
            Vertical mode from Traffic class [Vertical_mode enum]

        Returns
        -------
        f{M}: float[]
            Energy share factor [dimenesionless]
        """
        return np.select(condlist=[
                            ap_speed_mode == AP_speed_mode.CONSTANT_MACH, 
                            ap_speed_mode == AP_speed_mode.CONSTANT_CAS, 
                            ap_speed_mode == AP_speed_mode.ACCELERATE, 
                            ap_speed_mode == AP_speed_mode.DECELERATE],

                        choicelist=[
                            # Constant Mach
                            np.where(H_p > self.__H_P_TROP,
                                # Conditiona a: Constant Mach number in stratosphere (Equation 3.2-8)
                                1.0,
                                # Condition b: Constant Mach number below tropopause (Equation 3.2-9)
                                np.power(1.0 + self.__KAPPA*self.__R*self.__BETA_T_BELOW_TROP/2.0/self.__G_0 * np.square(M) * (T-d_T)/T, -1.0)),

                            # Constnt CAS
                            np.where(H_p <= self.__H_P_TROP,
                                # Condition c: Constant Calibrated Airspeed (CAS) below tropopause (Equation 3.2-10)
                                np.power(1.0 + self.__KAPPA*self.__R*self.__BETA_T_BELOW_TROP/2.0/self.__G_0 * np.square(M) * (T-d_T)/T \
                                    + np.power(1.0 + (self.__KAPPA-1.0)/2.0 * np.square(M), -1.0/(self.__KAPPA-1.0)) \
                                        * (np.power(1.0 + (self.__KAPPA-1.0)/2.0 * np.square(M), self.__KAPPA/(self.__KAPPA-1.0)) - 1.0), -1.0),
                                # Condition d: Constant Calibrated Airspeed (CAS) above tropopause (Equation 3.2-11)
                                np.power(1.0 + np.power(1.0 + (self.__KAPPA-1.0)/2.0 * np.square(M), -1.0/(self.__KAPPA-1)) \
                                    * (np.power(1.0 + (self.__KAPPA-1.0)/2.0 * np.square(M), self.__KAPPA/(self.__KAPPA-1.0)) - 1.0), -1.0)),
                            
                            # Acceleration in climb + Acceleration in descent
                            (vertical_mode == Vertical_mode.CLIMB) * 0.3 + (vertical_mode == Vertical_mode.DESCENT) * 1.7,

                            # Deceleration in descent + Deceleration in climb
                            (vertical_mode == Vertical_mode.DESCENT) * 0.3 + (vertical_mode == Vertical_mode.CLIMB) * 1.7
                        ])


    def cal_tem_rocd(self, T, d_T, m, D, f_M, Thr, V_tas, C_pow_red):
        """
        Total Energy Model. Speed and Throttle Controller. (Equation 3.2-1a and 3.2-7)
        Calculate Rate of climb or descent given velocity(constant) and thrust (max climb thrust/idle descent).
        
        Parameters
        ----------
        T: float[]
            Temperature [K]

        d_T: float[]
            Temperature differential at MSL [K]

        m: float[]
            Aircraft mass [kg]
        
        D: float[]
            Aerodynamic drag [N]

        f{M}: float[]
            Energy share factor [dimenesionless]
        
        Thr: float[]
            Thrust acting parallel to the aircraft velocity vector [N]

        V_tas: float[]
            True airspeed [m/s]

        C_pow_red: float[]
            Reduced climb power coefficient [dimensionless]

        Returns
        -------
        rocd: float[]
            Rate of climb or descent [m/s]
            Defined as variation with time of the aircraft geopotential pressure altitude H_p
        """
        return (T-d_T)/T * (Thr-D)*V_tas*C_pow_red/m/self.__G_0 * f_M


    def cal_tem_accel(self, T, d_T, m, D, rocd, Thr, V_tas):
        """
        Total Energy Model. ROCD and Throttle Controller. (Equation 3.2-1b and 3.2-7) NOTE: changed to equation  3.2-1
        Calculate accel given ROCD and thrust.
        
        Parameters
        ----------
        T: float[]
            Temperature [K]

        d_T: float[]
            Temperature differential at MSL [K]

        m: float[]
            Aircraft mass [kg]
        
        D: float[]
            Aerodynamic drag [N]    

        rocd: float[]
            Rate of climb or descent [m/s]

        Thr: float[]
            Thrust acting parallel to the aircraft velocity vector [N]

        V_tas: float[]
            True airspeed [m/s]

        Returns
        -------
        accel: float[]
            Acceleration of tur air speed [m/s^2]
        """
        # return rocd / f_M / ((T-d_T)/T) * m*self.__G_0 / (Thr-D)
        return (Thr - D) / m - self.__G_0 / V_tas * rocd*T/(T-d_T)


    def cal_tem_thrust(self, T, d_T, m, D, f_M, rocd, V_tas):
        """
        Total Energy Model. Speed and ROCD Controller. (Equation 3.2-1c and 3.2-7) TODO: change to equation  3.2-1
        Calculate thrust given ROCD and speed.
        
        Parameters
        ----------
        T: float[]
            Temperature [K]

        d_T: float[]
            Temperature differential at MSL [K]
        
        D: float[]
            Aerodynamic drag [N]

        m: float[]
            Aircraft mass [kg]

        f{M}: float[]
            Energy share factor [dimenesionless]

        rocd: float[]
            Rate of climb or descent [m/s]

        V_tas: float[]
            True airspeed [m/s]

        Returns
        -------
        Thr: float[]
            Thrust acting parallel to the aircraft velocity vector [N]
        """
        return rocd / f_M / ((T-d_T)/T) * m*self.__G_0 / V_tas + D


    # ----------------------------  Mass section 3.4 -----------------------------------------
    def __cal_operating_speed(self, m, V_ref):
        """
        Calculate operating speed given mass (Equation 3.4-1)

        Parameters
        ----------
        m: float[]
            Aircraft mass [kg]

        v_ref: float[]
            Velocity reference (e.g. v_stall) [m/s] 

        Returns
        -------
        V: float[]
            Operating velocity [m/s]
        """
        return V_ref * np.sqrt(m/self.__m_ref)

    
    # ----------------------------  Flight envelope section 3.5 -----------------------------------------
    def cal_maximum_altitude(self, d_T, m):
        """
        Calculate flight envelope (Section 3.5-1)

        Parameters
        ----------
        d_T: float[]
            Temperature differential from ISA [K]

        m: float[]
            Aircraft mass [kg]

        Returns
        -------
        h_max/act: float[]
            Actual maximum altitude for any given mass [ft]
        """
        return np.where(self.__h_max == 0, 
            # If h_max in OPF file is zero, maximum altitude is always h_MO
            self.__h_mo,
            # Else Equation 3.5-1
            np.minimum(self.__h_mo, self.__h_max + self.__g_t*(d_T-self.__c_tc_4) + self.__g_w*(self.__m_max-m)))
    

    def cal_minimum_speed(self, flight_phase):
        """
        Calculate minimum speed for aircraft (3.5-2~3)

        Parameters
        ----------
        flight_phase: float[]
            Flight phase from Traffic class [Flight_phase enum]

        Returns
        -------
        v_min: float[]
            Minimum at speed at specific configuration [m/s] TODO: need to consider mass using __calculate_operating_speed?
        """

        return np.select([flight_phase == Flight_phase.TAKEOFF, 
                          flight_phase == Flight_phase.INITIAL_CLIMB, 
                          flight_phase == Flight_phase.CLIMB & flight_phase == Flight_phase.CRUISE & flight_phase == Flight_phase.DESCENT,
                          flight_phase == Flight_phase.APPROACH,
                          flight_phase == Flight_phase.LANDING],
                             
                         [self.__C_V_MIN_TO * self.__v_stall_to,
                          self.__C_V_MIN * self.__v_stall_ic,
                          self.__C_V_MIN * self.__v_stall_cr,
                          self.__C_V_MIN * self.__v_stall_ap,
                          self.__C_V_MIN* self.__v_stall_ld])


    # ----------------------------  Aerodynamic section 3.6 -----------------------------------------
    def cal_aerodynamic_drag(self, V_tas, bank_angle, m, rho, configuration, c_des_exp):
        """
        Calculate Aerodynamic drag (Section 3.6.1)

        Parameters
        ----------
        V_tas: float[]
            True airspeed [m/s]

        bank_angles: float[]
            Bank angles from Traffic class [deg]

        m: float[]
            Aircraft mass [kg]

        rho: float[]
            Density [kg/m^3]

        configuration: float[]
            Configuration from Traffic class [Configuration enum]

        c_des_exp: float[]
            Coefficient of expedited descent factor [dimensionless]

        Returns
        -------
        D: float[]
            Drag force [N]
        """
        # Lift coefficient (Equation 3.6-1)
        c_L = 2.0 * m * self.__G_0 / rho / np.square(V_tas) / self.__S / np.cos(np.deg2rad(bank_angle))
        
        # Drag coefficient (Equation3.6-2~4)
        c_D = np.select(condlist=[
                            configuration == Configuration.APPROACH, 
                            configuration == Configuration.LANDING
                        ],
                        choicelist=[
                            np.where(self.__c_d2_ap != 0,                                               # Approach config
                                self.__c_d0_ap + self.__c_d2_ap * np.square(c_L),                           # If c_d0_ap / c_d2_ap are NOT set to 0 (Equation 3.6-3)
                                self.__c_d0_cr + self.__c_d2_cr * np.square(c_L)),                          # If c_d0_ap / c_d2_ap are  set to 0 (Equation 3.6-2)
                            np.where(self.__c_d2_ld != 0,                                               # Landing config
                                self.__c_d0_ld + self.__c_d0_ldg + self.__c_d2_ld * np.square(c_L),         # If c_d0_ld / c_d2_ld are NOT set to 0 (Equation 3.6-4)
                                self.__c_d0_cr + self.__c_d2_cr * np.square(c_L))                           # If c_d0_ld / c_d2_ld are set to 0 (Equation 3.6-2)
                        ],
                        default=self.__c_d0_cr + self.__c_d2_cr * np.square(c_L),                   # All configs except for approach and landing. (Equation 3.6-2)
                )

        # Drag force
        return c_D * rho * np.square(V_tas) * self.__S / 2.0 * c_des_exp


    def cal_low_speed_buffeting_limit(self, p, M, m):
        """
        Low speed buffeting limit for jet and turboprop aircraft. It is expressed as Mach number. (Equation 3.6-6)
        TODO: Appendix B

        Parameters
        ----------
        p: float[]
            Pressure [Pa] 

        M: float[]
            Mach number [dimensionless]

        m: float[]
            Aircraft mass [kg]

        Returns
        -------
        M: float[]
            Mach number [dimensionless]

        Notes
        -----
        TODO: Calculate minimum speed for Jet and Turboprop when H_p >= 15000. V_min = MAX(V_min_stall, M_b) (<- same unit)
              If H_p < 15000, V_min = V_min_stall
        """
        Q = (-np.square(-self.__c_lbo/self.__k)/9.0)
        R = (-27.0*(m*self.__G_0/self.__S)/0.583/p/self.__k - 2.0*np.power(-self.__c_lbo/self.__k, 3)) / 54.0
        theta = np.arccos(R/np.sqrt(-np.power(Q,3)))

        X_1 = 2.0 * np.sqrt(-Q) * np.cos(np.deg2rad(theta/3)) + (self.__c_lbo/self.__k)/3.0
        X_2 = 2.0 * np.sqrt(-Q) * np.cos(np.deg2rad(theta/3 + 120)) + (self.__c_lbo/self.__k)/3.0
        X_3 = 2.0 * np.sqrt(-Q) * np.cos(np.deg2rad(theta/3 + 240)) + (self.__c_lbo/self.__k)/3.0

        arr = np.array([X_1, X_2, X_3])
        return np.max(np.where(arr <= 0, np.inf, arr), axis=0)
         

    # ----------------------------  Engine Thrust section 3.7 ----------------------------------------- 
    def __cal_max_climb_to_thrust(self, H_p, V_tas, d_T):
        """
        Calculate maximum climb thrust for both take-off and climb phases (Section 3.7.1)

        Parameters
        ----------
        H_p: float[]
            Geopotential pressuer altitude [ft] TODO: Different unit

        V_tas: float[]
            True airspeed [kt] TODO: Different unit

        d_T: float[]
            Temperature differential from ISA [K]

        Returns
        -------
        Thr_max_climb: float[]
            Maximum climb thrust [N]
        """
        # Maximum climb thrust at standard atmosphere conditions (Equations 3.7-1~3)
        thr_max_climb_isa = np.select([self.__engine_type == Engine_type.JET, 
                                       self.__engine_type == Engine_type.TURBOPROP, 
                                       self.__engine_type == Engine_type.PISTON],

                                      [self.__c_tc_1 * (1.0 - H_p/self.__c_tc_2 + self.__c_tc_3 * np.square(H_p)),
                                       self.__c_tc_1/V_tas * (1.0 - H_p/self.__c_tc_2) + self.__c_tc_3,
                                       self.__c_tc_1 * (1.0 - H_p/self.__c_tc_2) + self.__c_tc_3/V_tas
                                      ])

        # Corrected for temperature deviation from ISA
        return thr_max_climb_isa * (1.0 - np.clip(np.clip(self.__c_tc_5, 0.0, None) * (d_T-self.__c_tc_4), 0.0, 0.4))


    def __cal_max_cruise_thrust(self, Thr_max_climb):
        """
        Calculate maximum cruise thrust (Equation 3.7-8)

        Parameters
        ----------
        Thr_max_climb: float[]
            Maximum climb thrust [N] (obtained from cal_max_climb_to_thrust())
        
        Returns
        -------
        thr_cruise_max: float[]
            Maximum cruise thrust [N]

        Notes
        -----
        The normal cruise thrust is by definition set equal to drag (Thr=D). However, the maximum amount of thrust available in cruise situation is limited.
        """
        return self.__C_TCR * Thr_max_climb

    
    def __cal_descent_thrust(self, H_p, Thr_max_climb, configuration):
        """
        Calculate descent thrust (Section 3.7.3)

        Parameters
        ----------
        H_p: float[]
            Geopotential pressuer altitude [m]

        Thr_max_climb: float[]
            Maximum climb thrust [N]

        Configuration: float[]
            Configuration from Traffic class [Configuration enum]

        Returns
        -------
        Thr_des: float[]
            Descent thrust [N]
        """
        # When “non-clean” data (see Section 3.6.1) is available, H_p,des cannot be below H_max,AP. 
        return np.where(H_p > np.where(self.__c_d2_ap != 0, np.clip(self.__h_p_des, self.__H_MAX_AP, None), self.__h_p_des),
                        # If H_p > H_p_des
                        self.__c_tdes_high * Thr_max_climb,     # Equation 3.7-9
                        # Else
                        np.select([configuration == Configuration.CLEAN, 
                                   configuration == Configuration.APPROACH, 
                                   configuration == Configuration.LANDING],

                                  [self.__c_tdes_low * Thr_max_climb,       # Equation 3.7-10
                                   self.__c_tdes_app * Thr_max_climb,       # Equation 3.7-11
                                   self.__c_tdes_ld * Thr_max_climb]))      # Equation 3.7-12
    

    # ----------------------------  Reduced climb power section 3.8 ----------------------------------------- 
    def cal_reduced_climb_power(self, m, H_p, H_max):
        """
        Calculate reduced climb power (section 3.8)

        Parameters
        ----------
        m: float[]
            Aircraft mass [kg]

        H_p: float[]
            Geopotential pressuer altitude [m]

        H_max: float[]
            Actual maximum altitude for any given mass [kg] (obtained from __cal_maximum_altitude())

        Returns
        -------
        C_pow,red: float[]
            Coefficient of reduced climb power [dimensionless]

        Notes
        -----
        The result can be applied in the calculation of ROCD during climb phase TODO:
        """
        c_red = np.where(H_p < 0.8*H_max,
                        # If (H_p < 0.8*H_max) section 5.11
                        np.select([self.__engine_type == Engine_type.TURBOPROP, self.__engine_type == Engine_type.PISTON, self.__engine_type == Engine_type.JET],
                                  [self.__C_RED_TURBO, self.__C_RED_PISTON, self.__C_RED_JET]),
                        # Else
                        0.0)

        return 1.0 - c_red * (self.__m_max - m/1000.0) / (self.__m_max - self.__m_min)     # Equation 3.8-1


    # ----------------------------  Fuel consumption section 3.9 ----------------------------------------- 
    def __cal_nominal_fuel_flow(self, V_tas, Thr):
        """
        Calculate nominal fuel flow (except idle descent and cruise) (equations 3.9-1~3 and 3.9-7)

        Parameters
        ----------
        V_tas: float[]
            True airspeed [kt] TODO: Different unit

        Thr: float[]
            Thrust acting parallel to the aircraft velocity vector [N]

        Returns
        -------
        f_norm: float[]
            Nominal fuel flow [kg/min]
        """
        return np.select([self.__engine_type == Engine_type.JET, 
                          self.__engine_type == Engine_type.TURBOPROP, 
                          self.__engine_type == Engine_type.PISTON],

                         [self.__c_f1 * (1.0 + V_tas/self.__c_f2) * Thr,                    # Equation 3.9-1 and 3.9-3
                          self.__c_f1 * (1.0 - V_tas/self.__c_f2) * (V_tas/1000.0) * Thr,   # Equation 3.9-2 and 3.9-3
                          self.__c_f1])                                                     # Equation 3.9-7


    def __cal_minimum_fuel_flow(self, H_p):
        """
        Calculate fuel flow for idle descent (equations 3.9-4 and 3.9-8)

        Parameters
        ----------
        H_p: float[]
            Geopotential pressuer altitude [ft] TODO: Different uni

        Returns
        -------
        f_min: float[]
            Minimum fuel flow [kg/min]
        """
        return np.where(self.__engine_type != Engine_type.PISTON,
                    # Non piston
                    self.__c_f3 * (1.0 - H_p/self.__c_f4),      # Equation 3.9-4
                    # Piston
                    self.__c_f3)                                # Equation 3.9-8


    def __cal_approach_landing_fuel_flow(self, V_tas, Thr, H_p):
        """
        Calculate fuel flow for approach and landing (equations 3.9-5 and 3.9-8)

        Parameters
        ----------
        V_tas: float[]
            True airspeed [kt] TODO: Different unit

        Thr: float[]
            Thrust acting parallel to the aircraft velocity vector [N]

        H_p: float[]
            Geopotential pressuer altitude [ft] TODO: Different uni

        Returns
        -------
        f_app/ld: float[]
            Approach and landing fuel flow [kg/min]
        """
        return np.where(self.__engine_type != Engine_type.PISTON, 
                    # Non piston
                    np.maximum(self.__cal_nominal_fuel_flow(V_tas, Thr), self.__cal_minimum_fuel_flow(H_p)),    # Equation 3.9-5
                    # Piston
                    self.__cal_minimum_fuel_flow(H_p))                                                          # Equation 3.9-8

    def __cal_cruise_fuel_flow(self, V_tas, Thr):
        """
        Calculate fuel flow for cruise (equations 3.9-6 and 3.9-9)

        Parameters
        ----------
        V_tas: float[]
            True airspeed [kt] TODO: Different unit

        Thr: float[]
            Thrust acting parallel to the aircraft velocity vector [N]

        Returns
        -------
        f_cr: float[]
            Cruise fuel flow [kg/min]
        """
        return np.select([self.__engine_type == Engine_type.JET, 
                          self.__engine_type == Engine_type.TURBOPROP, 
                          self.__engine_type == Engine_type.PISTON],

                         [self.__c_f1 * (1.0 + V_tas/self.__c_f2) * Thr * self.__c_fcr,                     # Equation 3.9-6
                          self.__c_f1 * (1.0 - V_tas/self.__c_f2) * (V_tas/1000.0) * Thr * self.__c_fcr,    # Equation 3.9-6
                          self.__c_f1 * self.__c_fcr])                                                      # Equation 3.9-9

    
    # ----------------------------  Airline Procedure Models section 4 ----------------------------------------- 
    def init_procedure_speed(self, m, n):
        """
        Initialize standard air speed schedule for all flight phases (Section 4.1-4.3)

        Parameters
        ----------
        m: float[]
            Aircraft mass [kg]

        n: int
            Index of performance array.
        """
        # Actual stall speed for takeoff
        v_stall_to_act = self.__cal_operating_speed(m, self.__v_stall_to)[n]
        # Standard climb schedule
        if (self.__engine_type[n] == Engine_type.JET):
            # If Jet (Equation 4.1-1~5)
            self.__climb_schedule[n] = [self.__C_V_MIN * v_stall_to_act + self.__V_D_CL_1, self.__C_V_MIN * v_stall_to_act + self.__V_D_CL_2, self.__C_V_MIN * v_stall_to_act + self.__V_D_CL_3,
                                        self.__C_V_MIN * v_stall_to_act + self.__V_D_CL_4, self.__C_V_MIN * v_stall_to_act + self.__V_D_CL_5, np.minimum(self.__v_cl_1[n], 250), self.__v_cl_2[n], self.__m_cl[n]]
        else:
            # Else if turboprop and piston (Equation 4.1-6~8)
            self.__climb_schedule[n] = [self.__C_V_MIN * v_stall_to_act + self.__V_D_CL_6, self.__C_V_MIN * v_stall_to_act + self.__V_D_CL_7, self.__C_V_MIN * v_stall_to_act + self.__V_D_CL_8,
                                        np.minimum(self.__v_cl_1[n], 250), self.__v_cl_2[n], self.__m_cl[n], 0.0, 0.0]

        # Standard cruise schedule
        if (self.__engine_type[n] == Engine_type.JET):
            # If Jet
            self.__cruise_schedule[n] = [np.minimum(self.__v_cr_1[n], 170), np.minimum(self.__v_cr_1[n], 220), np.minimum(self.__v_cr_1[n], 250), self.__v_cr_2[n], self.__m_cr[n]]
        else:
            # Else if turboprop and piston
            self.__cruise_schedule[n] =  [np.minimum(self.__v_cr_1[n], 150), np.minimum(self.__v_cr_1[n], 180), np.minimum(self.__v_cr_1[n], 250), self.__v_cr_2[n], self.__m_cr[n]]

        # Actual stall speed for landing TODO: consider fuel mass?
        v_stall_ld_act = self.__cal_operating_speed(m, self.__v_stall_ld)[n]
        # Standard descent schedule
        if (self.__engine_type[n] != Engine_type.PISTON):
            # If Jet and Turboprop (Equation 4.3-1~4)
            self.__descent_schedule[n] = [self.__C_V_MIN * v_stall_ld_act + self.__V_D_DSE_1, self.__C_V_MIN * v_stall_ld_act + self.__V_D_DSE_2, self.__C_V_MIN * v_stall_ld_act + self.__V_D_DSE_3,
                                          self.__C_V_MIN * v_stall_ld_act + self.__V_D_DSE_4, np.minimum(self.__v_des_1[n], 220), np.minimum(self.__v_des_1[n], 250), self.__v_des_2[n], self.__m_des[n]]
        else:
            # Else if Piston (Equation 4.3-5~7)
            self.__descent_schedule[n] = [self.__C_V_MIN * v_stall_ld_act + self.__V_D_DSE_5, self.__C_V_MIN * v_stall_ld_act + self.__V_D_DSE_6, self.__C_V_MIN * v_stall_ld_act + self.__V_D_DSE_7,
                                          self.__v_des_1[n], self.__v_des_2[n], self.__m_des[n], 0.0, 0.0]



    def get_procedure_speed(self, H_p, H_p_trans, flight_phase):
        """
        Get the standard air speed schedule

        Parameters
        ----------
        H_p: float[]
            Geopotential pressuer altitude [m]

        H_p_trans: float[]
            Transition altitude [m]

        m: float[]
            Aircraft mass [kg]

        flight_phase: float[]
            Flight phase from Traffic class [Flight_phase enum]

        Returns
        -------
        v_std: float[]
            Standard CAS [kt]
        -or-
        M_std: float[]
            Standard Mach [dimensionless] 

        Notes
        -----
        TODO: Recommended to determine the speed schedule from the highest altitude to the lowest one, 
        and to use at each step the speed of the higher altitude range as a ceiling value for the lower altitude range.

        TODO: Bound the speed schedule form the minimum and maximum speed.
        """
        return np.select([
            flight_phase == Flight_phase.CLIMB,
            flight_phase == Flight_phase.CRUISE,
            flight_phase == Flight_phase.DESCENT
        ],[
            # If climb
            np.where(self.__engine_type == Engine_type.JET,
                # If jet
                np.select([H_p < 1500, H_p >= 1500 & H_p < 3000, H_p >= 3000 & H_p < 4000, H_p >= 4000 & H_p < 5000, H_p >= 5000 & H_p < 6000, H_p >= 6000 & H_p < 10000, H_p >= 10000 & H_p < H_p_trans, H_p >= H_p_trans],
                          [self.__climb_schedule[:,0], self.__climb_schedule[:,1], self.__climb_schedule[:,2], self.__climb_schedule[:,3], self.__climb_schedule[:,4], self.__climb_schedule[:,5], self.__climb_schedule[:,6], self.__climb_schedule[:,7]]),
                # If turboprop and piston
                np.select([H_p < 500, H_p >= 500 & H_p < 1000, H_p >= 1000 & H_p < 1500, H_p >= 1500 & H_p < 10000, H_p >= 10000 & H_p < H_p_trans, H_p >= H_p_trans],
                          [self.__climb_schedule[:,0], self.__climb_schedule[:,1], self.__climb_schedule[:,2], self.__climb_schedule[:,3], self.__climb_schedule[:,4], self.__climb_schedule[:,5]])
            ),
            # If cruise
            np.where(self.__engine_type == Engine_type.JET,
                # If jet
                np.select([H_p < 3000, H_p >= 3000 & H_p < 6000, H_p >= 6000 & H_p < 14000, H_p >= 14000 & H_p < H_p_trans, H_p >= H_p_trans],
                          [self.__cruise_schedule[:,0], self.__cruise_schedule[:,1], self.__cruise_schedule[:,2], self.__cruise_schedule[:,3], self.__cruise_schedule[:,4]]),
                # If turboprop and piston
                np.select([H_p < 3000, H_p >= 3000 & H_p < 6000, H_p >= 6000 & H_p < 10000, H_p >= 10000 & H_p < H_p_trans, H_p >= H_p_trans],
                          [self.__cruise_schedule[:,0], self.__cruise_schedule[:,1], self.__cruise_schedule[:,2], self.__cruise_schedule[:,3], self.__cruise_schedule[:,4]])
            ),
            # If descent
            np.where(self.__engine_type != Engine_type.PISTON,
                # If jet and turboprop
                np.select([H_p < 999, H_p >= 1000 & H_p < 1500, H_p >= 1500 & H_p < 2000, H_p >= 2000 & H_p < 3000, H_p >= 3000 & H_p < 6000, H_p >= 6000 & H_p < 10000, H_p >= 10000 & H_p < H_p_trans, H_p >= H_p_trans],
                          [self.__descent_schedule[:,0], self.__descent_schedule[:,1], self.__descent_schedule[:,2], self.__descent_schedule[:,3], self.__descent_schedule[:,4], self.__descent_schedule[:,5], self.__descent_schedule[:,6], self.__descent_schedule[:,7]]),
                # If piston
                np.select([H_p < 500, H_p >= 500 & H_p < 1000, H_p >= 1000 & H_p < 1500, H_p >= 1500 & H_p < 10000, H_p >= 10000 & H_p < H_p_trans, H_p >= H_p_trans],
                          [self.__descent_schedule[:,0], self.__descent_schedule[:,1], self.__descent_schedule[:,2], self.__descent_schedule[:,3], self.__descent_schedule[:,4], self.__descent_schedule[:,5]])
            )
        ])

    
    # ----------------------------  Global aircraft parameters section 5 -----------------------------------------
    def cal_max_d_tas(self, d_t):
        """
        Calculate maximum delta true air speed (equation 5.2-1)

        Parameters
        ----------
        d_t: float[]
            Timestep [s]

        Returns
        -------
        d_v: float[]
            Max delta velocity for time step [m/s]
        """
        return self.__A_L_MAX_CIV * d_t
    
    def cal_max_d_rocd(self, d_t, d_v, V_tas, rocd):
        """
        Calculate maximum delta rate of climb or descend (equation 5.2-2)

        Parameters
        ----------
        d_t: float[]
            Timestep [s]

        d_v: float[]
            Delta velocity [m/s]

        V_tas: float[]
            True air speed [m/s]

        rocd: float[]
            Current rate of climb/descend [m/s]

        Returns
        -------
        d_rocd: float[]
            Delta rate of climb or descent [m/s]
        """
        return np.sin(np.arcsin(rocd/V_tas) - self.__A_N_MAX_CIV * d_t / V_tas) * (V_tas+d_t)


    def cal_rate_of_turn(self, bank_angle, V_tas):
        """
        Calculate rate of turn (Equation 5.3-1)

        Parameters
        ----------
        bank_angle: float[]
            Bank angle [deg]

        V_tas: float[]
            True air speed [m/s]
        
        Returns
        -------
        Rate of turn : float[]
            Rate of turn [deg/s]
        """
        return np.rad2deg(self.__G_0 / V_tas * np.tan(np.deg2rad(bank_angle)))


    def cal_bank_angle(self, rate_of_turn, V_tas):
        """
        Calculate rate of turn (Equation 5.3-1)

        Parameters
        ----------
        Rate of turn : float[]
            Rate of turn [deg/s]

        V_tas: float[]
            True air speed [m/s]
        
        Returns
        -------
        bank_angle: float[]
            Bank angle [deg]
        """
        return np.rad2deg(np.arctan(np.deg2rad(rate_of_turn) * V_tas / self.__G_0))

    def get_nominal_bank_angles(self, flight_phase):
        """
        Get standard nominal bank angles (Session 5.3)

        Parameters
        ----------
        flight_phase: float[]
            Flight phase from Traffic class [Flight_phase enum]

        Returns
        -------
        bank_angles :float 
            Bank angles [deg]
        """
        return np.where((flight_phase == Flight_phase.TAKEOFF) | (flight_phase == Flight_phase.LANDING), self.__PHI_NORM_CIV_TOLD, self.__PHI_NORM_CIV_OTHERS)

    def cal_expedite_descend_factor(self, expedite_descent):
        """
        Calculate expedited descent factor for drag multiplication. (Equation 5.4-1)

        Parameters
        ----------
        expedite_descent: bool[]
            Autopilot setting of whether expedite descent is activated

        Returns
        -------
        c_des_exp: float[]
            Coefficient of expedited descent factor [dimensionless]
        """
        return np.where(expedite_descent, self.__C_DES_EXP, 1.0)
