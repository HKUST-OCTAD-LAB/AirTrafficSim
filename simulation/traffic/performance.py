"""Aircraft performance class calculation using BADA 3.15"""
from pathlib import Path
import numpy as np

class Performance:
    """
    Performance class 

    Attributes
    ----------

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
        self.__n_eng = np.zeros([N])                            # number of engines
        self.__engine_type = np.zeros([N])                      # engine type, either Jet (1), Turboprop (2), or Piston (3)
        self.__wake_category = np.zeros([N])                    # wake category, either J (1), H (2), M (3), L(4)

        # Mass
        self.__m_ref = np.zeros([N])                            # reference mass [tones]
        self.__m_min = np.zeros([N])                            # minimum mass [tones]
        self.__m_max = np.zeros([N])                            # maximum mass [tones]
        self.__m_pyld = np.zeros([N])                           # maximum payload mass [tones]

        # Flight envelope
        self.__v_mo = np.zeros([N])                             # maximum operating speed [knots (CAS)]
        self.__m_mo = np.zeros([N])                             # maximum operating Mach number [dimensionless]
        self.__h_mo = np.zeros([N])                             # maximum opearting altitude [feet]
        self.__h_max = np.zeros([N])                            # maximum altitude at MTOW and ISA [feet]
        self.__g_w = np.zeros([N])                              # weight gradient on maximum altitude [feet/kg]
        self.__g_t = np.zeros([N])                              # temperature gradient on maximum altitude [feet/K]

        # Aerodynamics
        self.__s = np.zeros([N])                                # reference wing surface area [m^2]
        self.__c_d0_cr = np.zeros([N])                          # parasitic drag coefficient (cruise) [dimensionless]
        self.__c_d2_cr = np.zeros([N])                          # induced drag coefficient (cruise) [dimensionless]
        self.__c_d0_ap = np.zeros([N])                          # parasitic drag coefficient (approach) [dimensionless]
        self.__c_d2_ap = np.zeros([N])                          # induced drag coefficient (approach) [dimensionless]
        self.__c_d0_ld = np.zeros([N])                          # parasitic drag coefficient (landing) [dimensionless]
        self.__c_d2_ld = np.zeros([N])                          # induced drag coefficient (landing) [dimensionless]
        self.__c_d0_ldg = np.zeros([N])                         # parasite darg coefficient (landing gear) [dimensionless]
        self.__v_stall_to = np.zeros([N])                       # stall speed (TO) [knots (CAS)]
        self.__v_stall_ic = np.zeros([N])                       # stall speed (IC) [knots (CAS)]
        self.__v_stall_cr = np.zeros([N])                       # stall speed (CR) [knots (CAS)]
        self.__v_stall_ap = np.zeros([N])                       # stall speed (AP) [knots (CAS)]
        self.__v_stall_ld = np.zeros([N])                       # stall speed (LD) [knots (CAS)]
        self.__c_lbo = np.zeros([N])                            # buffet onset lift coefficient (jet and TBP only) [dimensionless]
        self.__k = np.zeros([N])                                # buffeting gradient (Jet & TBP only) [dimensionless]

        # Engine thrust
        self.__c_tc_1 = np.zeros([N])                           # 1st maximum climb thrust coefficient [Newton (jet/piston) knot-Newton (turboprop)]
        self.__c_tc_2 = np.zeros([N])                           # 2nd maximum climb thrust coefficient [feet]
        self.__c_tc_3 = np.zeros([N])                           # 3rd maximum climb thrust coefficient [1/feet^2 (jet) Newton (turboprop) knot-Newton (piston)]
        self.__c_tc_4 = np.zeros([N])                           # 1st thrust temperature coefficient [K]
        self.__c_tc_5 = np.zeros([N])                           # 2nd thrust temperature coefficient [1/K]
        self.__c_tdes_low = np.zeros([N])                       # low altitude descent thrust coefficient [dimensionless]
        self.__c_tdes_high = np.zeros([N])                      # high altitude descent thrust coefficient [dimensionless]
        self.__h_p_des = np.zeros([N])                          # transition altitude for calculation of descent thrust [feet]
        self.__c_tdes_app = np.zeros([N])                       # approach thrust coefficient [dimensionless]
        self.__c_tdes_id = np.zeros([N])                        # landing thrust coefficient [dimensionless]
        self.__v_des_ref = np.zeros([N])                        # reference descent speed [knots (CAS)]
        self.__m_des_ref = np.zeros([N])                        # reference descent Mach number [dimensionless]

        # Fuel flow
        self.__c_f1 = np.zeros([N])                             # 1st thrust specific fuel consumption coefficient [kg/(min*kN) (jet) kg/(min*kN*knot) (turboprop) kg/min (piston)]
        self.__c_f2 = np.zeros([N])                             # 2nd thrust specific fuel consumption coefficient [knots]
        self.__c_f3 = np.zeros([N])                             # 1st descent fuel flow coefficient [kg/min]
        self.__c_f4 = np.zeros([N])                             # 2nd descent fuel flow coefficient [feet]
        self.__c_fcr = np.zeros([N])                            # cruise fuel flow correction coefficient [dimensionless]

        # Ground movement
        self.__tol = np.zeros([N])                              # take-off length
        self.__ldl = np.zeros([N])                              # landing length
        self.__span = np.zeros([N])                             # wingspan
        self.__length = np.zeros([N])                           # length


        # ----------------------------  Airline Procedure Models (APF) section 4 -----------------------------------------
        # Climb
        self.__v_cl_1 = np.zeros([N])                           # standard climb CAS [knots] between 1,500/6,000 and 10,000 ft
        self.__v_cl_2 = np.zeros([N])                           # standard climb CAS [knots] between 10,000 ft and Mach transition altitude
        self.__m_cl = np.zeros([N])                             # standard climb Mach number above Mach transition altitude

        # Cruise
        self.__v_cr_1 = np.zeros([N])                           # standard cruise CAS [knots] between 3,000 and 10,000 ft
        self.__v_cr_2 = np.zeros([N])                           # standard cruise CAS [knots] between 10,000 ft and Mach transition altitude
        self.__m_cr = np.zeros([N])                             # standard cruise Mach number above Mach transition altitude

        # Descent
        self.__v_des_1 = np.zeros([N])                          # standard descent CAS [knots] between 3,000/6,000 and 10,000 ft
        self.__v_des_2 = np.zeros([N])                          # standard descent CAS [knots] between 10,000 ft and Mach transition altitude
        self.__m_des = np.zeros([N])                            # standard descent Mach number above Mach transition altitude


        # ----------------------------  Global Aircraft Parameters (GPF) section 5 -----------------------------------------
        # Read data from GPF file (section 6.8)
        # 'CD', 1X, A15, 1X, A7, 1X, A16, 1x, A29, 1X, E10.5
        if Path('simulation/data/BADA/BADA.GPF').is_file():
            GPF = np.genfromtxt(Path('simulation/data/BADA/BADA.GPF'), delimiter=[3,16,8,17,29,12], dtype="U2,U15,U7,U16,U29,f8", comments="CC", autostrip=True, skip_footer=1)
        else: 
            print("BADA.GPF File does not exit")

        # Maximum acceleration
        self.__A_L_MAX_CIV = GPF[0][5]                          # Maximum longitudinal acceleration for civil flights [2 ft/s^2]
        self.__A_N_MAX_CIV = GPF[1][5]                          # Maximum normal acceleration for civil flights [5 ft/s^2]

        # Bank angles
        self.__PHI_NORM_CIV_TOLD = GPF[2][5]                    # Nominal bank angles fpr civil flight during TO and LD [15 deg]
        self.__PHI_NORM_CIV_OTHERS = GPF[3][5]                  # Nominal bank angles for civil flight during all other phases [30 deg]
        self.__PHI_NORM_MIL = GPF[4][5]                         # Nominal bank angles for military flight (all phases) [50 deg]
        self.__PHI_MAX_CIV_TOLD = GPF[5][5]                     # Maximum bank angles for civil flight during TO and LD [25 deg]
        self.__PHI_MAX_CIV_HOLD = GPF[6][5]                     # Maximum bank angles for civil flight during HOLD [35 deg]
        self.__PHI_MAX_CIV_OTHERS = GPF[7][5]                   # Maximum bank angles for civil flight during all other phases [45 deg]
        self.__PHI_MAX_MIL = GPF[8][5]                          # Maximum bank angles for military flight (all phases) [70 deg]

        # Expedited descent (drag multiplication factor during expedited descent to simulate use of spoilers)
        self.__C_DES_EXP = GPF[9][5]                            # Expedited descent factor [1.6]

        # Thrust factors
        self.__C_CR = GPF[11][5]                                # Maximum cruise thrust coefficient [0.95] (postition different between GPF and user menu)
        self.__C_TH_TO = GPF[10][5]                             # Take-off thrust coefficient [1.2] (no longer used since BADA 3.0) (postition different between GPF and user menu)

        # Configuration altitude threshold
        self.__H_MAX_TO = GPF[12][5]                            # Maximum altitude threshold for take-off [400 ft]
        self.__H_MAX_IC = GPF[13][5]                            # Maximum altitude threshold for initial climb [2,000 ft]
        self.__H_MAX_AP = GPF[14][5]                            # Maximum altitude threshold for approach [8,000 ft]
        self.__H_MAX_LD = GPF[15][5]                            # Maximum altitude threshold for landing [3,000 ft]

        # Minimum speed coefficient
        self.__C_V_MIN = GPF[16][5]                             # Minimum speed coefficient (all other phases) [1.3]
        self.__C_V_MIN_TO = GPF[17][5]                          # Minimum speed coefficient for take-off [1.2]

        # Speed schedules
        self.__V_D_CL_1 = GPF[18][5]                            # Climb speed increment below 1,500 ft (jet) [5 knot CAS]
        self.__V_D_CL_2 = GPF[19][5]                            # Climb speed increment below 3,000 ft (jet) [10 knot CAS]
        self.__V_D_CL_3 = GPF[20][5]                            # Climb speed increment below 4,000 ft (jet) [30 knot CAS]
        self.__V_D_CL_4 = GPF[21][5]                            # Climb speed increment below 5,000 ft (jet) [60 knot CAS]
        self.__V_D_CL_5 = GPF[22][5]                            # Climb speed increment below 6,000 ft (jet) [80 knot CAS]
        self.__V_D_CL_6 = GPF[23][5]                            # Climb speed increment below 500 ft (turbo/piston) [20 knot CAS]
        self.__V_D_CL_7 = GPF[24][5]                            # Climb speed increment below 1,000 ft (turbo/piston) [30 knot CAS]
        self.__V_D_CL_8 = GPF[25][5]                            # Climb speed increment below 1,500 ft (turbo/piston) [35 knot CAS]
        self.__V_D_DSE_1 = GPF[26][5]                           # Descent speed increment below 1,000 ft (jet/turboprop) [5 knot CAS]
        self.__V_D_DSE_2 = GPF[27][5]                           # Descent speed increment below 1,500 ft (jet/turboprop) [10 knot CAS]
        self.__V_D_DSE_3 = GPF[28][5]                           # Descent speed increment below 2,000 ft (jet/turboprop) [20 knot CAS]
        self.__V_D_DSE_4 = GPF[29][5]                           # Descent speed increment below 3,000 ft (jet/turboprop) [50 knot CAS]
        self.__V_D_DSE_5 = GPF[30][5]                           # Descent speed increment below 500 ft (piston) [5 knot CAS]
        self.__V_D_DSE_6 = GPF[31][5]                           # Descent speed increment below 1,000 ft (piston) [10 knot CAS]
        self.__V_D_DSE_7 = GPF[32][5]                           # Descent speed increment below 1,500 ft (piston) [20 knot CAS]

        # Holding speeds
        self.__V_HOLD_1 = GPF[33][5]                            # Holding speed below FL140 [230 knot CAS]
        self.__V_HOLD_2 = GPF[34][5]                            # Holding speed between FL140 and FL220 [240 knot CAS]
        self.__V_HOLD_3 = GPF[35][5]                            # Holding speed between FL220 and FL340 [265 knot CAS]
        self.__V_HOLD_4 = GPF[36][5]                            # Holding speed above FL340 [0.83 Mach]
        
        # Ground speed
        self.__V_BACKTRACK = GPF[37][5]                         # Runway backtrack speed [35 knot CAS]
        self.__V_TAXI = GPF[38][5]                              # Taxi speed [15 knot CAS]
        self.__V_APRON = GPF[39][5]                             # Apron speed [10 knot CAS]
        self.__V_GATE = GPF[40][5]                              # Gate speed [5 knot CAS]

        # Reduced power coefficient
        self.__C_RED_TURBO = GPF[42][5]                         # Maximum reduction in power for turboprops [0.25] (postition different between GPF and user menu)
        self.__C_RED_PISTON = GPF[41][5]                        # Maximum reduction in power for pistons [0.0] (postition different between GPF and user menu)
        self.__C_RED_JET = GPF[43][5]                           # Maximum reduction in power for jets [0.15]       

        # Delete variable to free memory
        del GPF


        # ----------------------------  SYNONYM FILE FORMAT (SYNONYM.NEW) section 6.3 -----------------------------------------
        # | 'CD' | SUPPORT TYPE (-/*) | AIRCRAFT Code | MANUFACTURER | NAME OR MODEL | FILE NAME | ICAO (Y/N) |
        self.__SYNONYM = np.genfromtxt(Path('simulation/data/BADA/SYNONYM.NEW'), delimiter=[3,2,7,20,25,8,5], names=['CD','ST','ACCODE','MANUFACTURER','MODEL','FILENAME','ICAO'], dtype="U2,U1,U4,U18,U25,U6,U1", comments="CC", autostrip=True, skip_footer=1)


    def add_aircraft_performance(self, icao, n, mass=2):
        """
        Append one specific aircraft performance data to the performance array.

        Parameters
        ----------
        self: Performance class instance
            Used to append data to the performance array.
        ICAO: string
            ICAO code of the specific aircraft.
        n: int
            Index of array.
        mass: int
            Aircraft mass for specific flight. To be used for APF. 1 = LO, 2 = AV, 3 = HI

        Returns
        -------
        """

        # Get file name by searching in SYNONYM.NEW
        try:
            row = np.where(self.__SYNONYM['ACCODE'] == icao)[0][0]      # Get row index
        except:
            print("No aircraft in SYNONYM.NEW")

        file_name = self.__SYNONYM[row][5]

        # Get data from Operations Performance File (Section 6.4)
        OPF = np.genfromtxt(Path('simulation/data/BADA/',file_name+'.OPF'), delimiter=[3,2,2,13,13,13,13,11], dtype="U2,U1,U2,f8,f8,f8,f8,f8", comments="CC", autostrip=True, skip_header=16, skip_footer=1)

        # 'CD', 3X, A6, 9X, I1, 12X, A9, 17X, A1 - aircraft type block - 1 data line
        # | 'CD' | ICAO | # of engine | 'engines' | engine type ( Jet,  Turboprop  or  Piston) | wake category ( J (jumbo), H (heavy), M (medium) or L (light))
        OPF_Actype = np.genfromtxt(Path('simulation/data/BADA/',file_name+'.OPF'), delimiter=[5,15,1,12,26,1], dtype="U2,U6,i1,U7,U9,U1", comments="CC", autostrip=True, max_rows=1)
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
        self.__s[n] = OPF[2][3]
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
        self.__c_tdes_id[n] = OPF[15][7]

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
        APF = np.genfromtxt(Path('simulation/data/BADA/',file_name+'.APF'), delimiter=[6,8,9,4,4,4,3,5,4,4,4,4,3,4,4,5,4,4,4,5,7], dtype="U2,U7,U7,U2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,i2,U6", comments="CC", autostrip=True)
        self.__v_cl_1[n] = APF[mass][4]
        self.__v_cl_2[n] = APF[mass][5]
        self.__m_cl[n] = APF[mass][6]/100
        self.__v_cr_1[n] = APF[mass][9]
        self.__v_cr_2[n] = APF[mass][10]
        self.__m_cr[n] = APF[mass][11]/100
        self.__m_des[n] = APF[mass][12]/100
        self.__v_des_2[n] = APF[mass][13]
        self.__v_des_1[n] = APF[mass][14]

        # Delete variable to free memory
        del APF


    def calculate_performance(self):
        """
        Calculate aircraft performance according to BADA.

        Parameters
        ----------
        self:

        Aircrafts: Aircrafts() class
            To obtain and update aircrafts' present states.

        """

        # Section 3.1.1 MSL Standard atmosphere condition
        self.__T_0 = 288.15                 # Standard atmospheric temperature at MSL [K]
        self.__p_0 = 101325                 # Standard atmospheric pressure at MSL [Pa]
        self.__rho_0 = 1.225                # Standard atmospheric density at MSL [kg/m^3]
        self.__a_0 = 340.294                # Speed of sound [m/s]

        self.__K = 1.4                      # Adiabatic index of air [dimensionless]
        self.__R = 287.05287                # Real gas constant of air [m^2/(K*s^2)]
        self.__g_0 = 9.80665                # Gravitational acceleration [m/s^2]
        self.__beta_T = -0.0065             # ISA temperature gradient with altitude below the tropopause [K/m]


        # Total energy model (section 3.2)


        # Aerodynamic (3.6)
        


        pass
