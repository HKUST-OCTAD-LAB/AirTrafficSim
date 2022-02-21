from enum import IntEnum

class Flight_phase(IntEnum):
    """Flight configuration"""
    AT_GATE_ORIGIN = 1,
    TAXI_ORIGIN = 2,
    TAKEOFF = 3,
    INITIAL_CLIMB = 4,
    CLIMB = 5,
    CRUISE = 6,
    DESCENT = 7,
    APPROACH = 8,
    LANDING = 9,
    TAXI_DEST = 10,
    AT_GATE_DEST = 11


class Engine_type(IntEnum):
    JET = 1,
    TURBOPROP = 2,
    PISTON = 3


class Wake_category(IntEnum):
    J = 1,
    H = 2,
    M = 3,
    L = 4


class Traffic_speed_mode(IntEnum):
    CAS = 1,
    MACH = 2

class AP_speed_mode(IntEnum):
    CONSTANT_MACH = 1,
    CONSTANT_CAS = 2,
    ACCELERATE = 3,
    DECELERATE = 4


class AP_throttle_mode(IntEnum):
    SPEED = 1,
    THRUST = 2


class AP_vertical_mode(IntEnum):
    ALT_HOLD = 1,
    VS = 2,
    FLC = 3