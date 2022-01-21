from enum import Enum

class Flight_phase(Enum):
    AT_GATE_ORIGIN = 1,
    TAXI_ORIGIN = 2,
    TAKEOFF = 3,
    INITIAL_CLIMB = 4,
    CLIMB = 5,
    CRUISE = 6,
    DESCENT = 7,
    APPROACH = 8,
    LANDING = 9,
    TAXI_DEsT = 10,
    AT_GATE_DEST = 11

class Engine_type(Enum):
    JET = 1,
    TURBOPROP = 2,
    PISTON = 3

class Wake_category(Enum):
    J = 1,
    H = 2,
    M = 3,
    L = 4