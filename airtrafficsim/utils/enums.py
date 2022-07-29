from enum import IntEnum

class EngineType(IntEnum):
    JET = 1,
    TURBOPROP = 2,
    PISTON = 3


class WakeCat(IntEnum):
    J = 1,
    H = 2,
    M = 3,
    L = 4


class FlightPhase(IntEnum):
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


class Config(IntEnum):
    TAKEOFF = 1,
    INITIAL_CLIMB = 2,
    CLEAN = 3,
    APPROACH = 4,
    LANDING = 5


class SpeedMode(IntEnum):
    CAS = 1,
    MACH = 2


class VerticalMode(IntEnum):
    LEVEL = 1,
    CLIMB = 2,
    DESCENT = 3


class APSpeedMode(IntEnum):
    CONSTANT_MACH = 1,
    CONSTANT_CAS = 2,
    ACCELERATE = 3,
    DECELERATE = 4


class APThrottleMode(IntEnum):
    AUTO = 1,
    SPEED = 2


class APVerticalMode(IntEnum):
    ALT_HOLD = 1,
    VS = 2,
    FLC = 3

class APLateralMode(IntEnum):
    HEADING = 1,
    LNAV = 2